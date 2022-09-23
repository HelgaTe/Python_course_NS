import re
import sqlite3
import yaml
from datetime import datetime, timedelta

"""
when bd is created >>> add last_active column by the following command into terminal:
    dhcp_snooping.db> alter table dhcp add column 'last_active' 'datetime'
and then you can add data into db by running add_data_status.py 
"""


def add_data(connection, query, data):  # общая функция для записи данных в БД
    # connection - переменная, которая создается в нижестоящих функциях (add_dhcp_data & add_sw_data)
    for row in data:
        try:
            with connection:
                connection.execute(query, row)
        except sqlite3.IntegrityError as err:
            print("При добавлении данных:", row, "Возникла ошибка:", err)


def parse_dhcp_snoop(filename):  # с помощью regex отобрать информацию для записи в бд
    regex = re.compile("(\S+) +(\S+) +\d+ +\S+ +(\d+) +(\S+)")  # regex for <sw*_dhcp_snooping> file content
    sw = re.search("(\w+)_dhcp_snooping.txt", filename).group(1)  # получить номер switch из названия файла
    with open(filename) as f:
        result = [match.groups() + (sw,) for match in
                  regex.finditer(f.read())]  # прочитать содержимое файла и получить данные в виде кортежа
    return result


def add_dhcp_data(db_name, data_files):
    connection = sqlite3.connect(db_name)  # подклчиться к конкретной бд
    connection.execute("update dhcp set active = 0")  # отметить замененые данные,как неактивные
    query = "replace into dhcp values (?, ?, ?, ?, ?, ?, datetime('now'))"  # добавление/замена (нарушение условия уникальности поля) данных в табл
    # при добавлении записи, для которой не возникает нарушения уникальности поля, REPLACE работает как обычный INSERT
    for filename in data_files:
        result = parse_dhcp_snoop(filename)
        updated_result = (row + (1,) for row in result)  # <row + (1,)> добавить стоблец с значением (1)
        add_data(connection, query, updated_result)
    connection.close()


def add_sw_data(db_name, sw_data_file):  # записать данные о коммутаторах, находятся в файле switches.yml
    connection = sqlite3.connect(db_name)
    query_switches = "insert into switches values (?,?)"  # запрос для записи данных
    with open(sw_data_file) as f:
        switches = yaml.safe_load(f)  # считать файл - данные в виде сложенного словаря
    sw_data = list(switches["switches"].items())  # получить данные в виде кортежа
    add_data(connection, query_switches, sw_data)  # записать данные из файла в БД
    connection.close()


def delete_old_data(db_name):
    connection = sqlite3.connect(db_name)
    now = datetime.today().replace(microsecond=0)
    week_ago = str(now - timedelta(days=7))  # apply str type, because <last_active> type(data)=str
    for row in connection.execute('select mac, last_active from dhcp'):
        last_active = str(row[1]).strip() # date from dhcp has white space <' 2022-09-22 18:47:32'> >>> provoke failure
        mac = str(row[0])
        status = last_active < week_ago # True, False
        query = 'delete from dhcp where mac = ?'
        if status:
            connection.execute(query, (mac,))
        connection.commit()


if __name__ == "__main__":
    db_filename = "dhcp_snooping.db"
    delete_old_data(db_filename)
"""
before def delete_old_data testing:
- copy db from task 25_5
- UPDATE dhcp set last_active = ' 2022-08-22 18:47:32' >>> change last_active date
- UPDATE dhcp set last_active = ' 2022-09-22 18:47:32' where vlan = '10' >>>back changes for vlan 10
upon running def delete_old_data >>> dhcp tab includes 4 rows (where vlan = 10)
"""
