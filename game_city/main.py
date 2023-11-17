import wikipediaapi
import requests
import cities.cities_directory as cities_dir


class StopGameError(Exception):

    __message = '[+] Игра окончена'

    def __str__(self):
        return self.__message


class BaseGame:

    def __init__(self):
        self._wiki = wikipediaapi.Wikipedia('CoolBot/0.0 (https://example.org/coolbot/;'
                                            ' coolbot@example.org) generic-library/0.0', 'ru')

    _used_city = []

    _russian_language = ["а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й",
                         "к", "л", "м", "н", "о", "п", "р", "с", "т", "у", "ф",
                         "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь", "э", "ю", "я"]

    def get_used_city(self):
        return self._used_city


class Game(BaseGame):

    def __city_search(self, user_answer):  # поиск нового города
        letter = user_answer[-1]
        for char in user_answer[::-1]:
            if char != 'ь' and char != 'ъ' and char != ' ':
                letter = char
                break
        for city in cities_dir.cities_data_base():
            if city[0] == letter.upper() and city not in self._used_city:
                return city

    def __city_verification(self, user_answer):  # проверка города на его наличие в википедии
        try:
            page = self._wiki.page(user_answer)
            if page.exists() and 'город' in page.text.lower():
                return True
            else:
                return False
        except requests.exceptions.ConnectionError:
            print("🤖 Не удалось подключиться к Википедии. Проверьте подключение к Интернету.")
            return False

    def play(self, count=0, err=0):
        ai_answers = []
        print('[+] Добро пожаловать в игру "Города"')

        while True:

            count += 1
            user_answer = input('[+] Пожалуйста, введите город (для выхода введите: 1): ')

            if user_answer == '1':
                print('🤖 Спасибо за игру!')
                break

            if not user_answer:
                print("🤖 Вы не ввели город!")
                err += 1
                continue

            if user_answer in self._used_city:
                print("🤖 Этот город уже был!")
                err += 1
                continue

            if user_answer[0].lower() not in self._russian_language:
                print('🤖 Напишите на русском пожалуйста')
                err += 1
                continue

            ai_answer = Game.__city_search(self, user_answer)

            if count > (err + 1):
                if ai_answers[-1][-1] == 'ь' or ai_answers[-1][-1] == 'ъ':
                    if user_answer[0] != ai_answers[-1][-2].upper():
                        print('[+] Ваш город начинается не с последней буквы предыдущего города')
                        continue
                else:
                    if user_answer[0] != ai_answers[-1][-1].upper():
                        print('[+] Ваш город начинается не с последней буквы предыдущего города')
                        continue

            if ai_answer is None:
                user_new_city = input(f'🤖 Я не знаю города на эту букву, '
                                      f'предложите свой ответ (для выхода введите 1) ')
                if user_new_city == '1':
                    raise StopGameError

                elif self.__city_verification(user_new_city):
                    cities_dir.add_city_to_db(user_new_city)
                    print(f'🤖 Спасибо, теперь я знаю город {user_new_city}')
                    raise StopGameError

                else:
                    print(f'[+] {user_new_city} не город или его невозможно найти в Википедии.')
                    raise StopGameError

            else:
                if Game.__city_verification(self, user_answer):
                    self._used_city.append(user_answer)
                    self._used_city.append(ai_answer)
                    print('🤖  Мой ответ: ', ai_answer)
                    ai_answers.append(ai_answer)
                else:
                    print(f"[+] {user_answer} не город или его невозможно найти в Википедии.")
                    err += 1


try:
    i = Game()
    i.play()
except StopGameError:
    print(StopGameError(), '\n[+] Вы победили!!!')

