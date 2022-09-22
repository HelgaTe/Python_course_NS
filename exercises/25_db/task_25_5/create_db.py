import sqlite3
import os

'''
create_db.py - в скрипт вынесена функциональность по созданию БД:
* должна выполняться проверка наличия файла БД
* если файла нет, согласно описанию схемы БД в файле dhcp_snooping_schema.sql,
  должна быть создана БД
* имя файла бд - dhcp_snooping.db

В БД должно быть две таблицы (схема описана в файле dhcp_snooping_schema.sql):
 * switches - в ней находятся данные о коммутаторах
 * dhcp - тут хранится информация полученная из вывода sh ip dhcp snooping binding

Пример выполнения скрипта, когда файла dhcp_snooping.db нет:
$ python create_db.py
Создаю базу данных...

После создания файла:
$ python create_db.py
База данных существует
'''


# inputs

def create_db(db_name, db_schema):
    db_exists = os.path.exists(db_name)
    if db_exists:
        print('База данных существует')
        return
    print("Создаю базу данных...")
    with open(db_schema) as f:
        db_schema = f.read()
        connection = sqlite3.connect(db_name)
        connection.executescript(db_schema)
        connection.close()


if __name__ == '__main__':
    db_filename = 'dhcp_snooping.db'
    schema = 'dhcp_snooping_schema.sql'

    create_db(db_filename, schema)
