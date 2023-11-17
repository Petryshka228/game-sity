import json


def cities_data_base():
    with open('city_db.json', 'r') as db:
        a = json.load(db)
        return a


def add_city_to_db(city):
    with open('city_db.json', 'r') as db:
        r = json.load(db)
        if city not in r:
            r.append(city)
        else:
            return f'Такой город уже есть в моей базе данных'
    with open('city_db.json', 'w') as file:
        w = json.dump(r, file)
    return r


if 'name' == '__main__':
    cities_data_base()
