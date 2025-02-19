# -*- coding: utf-8 -*-
"""
Задание 25.5a

Для заданий 25 раздела нет тестов!

После выполнения задания 25.5, в таблице dhcp есть новое поле last_active.

Обновите скрипт add_data_status.py, таким образом, чтобы он удалял все записи,
которые были активными более 7 дней назад.

Для того, чтобы получить такие записи, можно просто вручную обновить поле last_active
в некоторых записях и поставить время 7 или более дней.

В файле задания описан пример работы с объектами модуля datetime.
Показано как получить дату 7 дней назад.
С этой датой надо будет сравнивать время last_active.

Обратите внимание, что строки с датой, которые пишутся в БД, можно сравнивать
между собой.

"""

from datetime import datetime, timedelta

now = datetime.today().replace(microsecond=0)
week_ago = now - timedelta(days=7)

# print(now)
# print(week_ago)
# print(now > week_ago)
# print(str(now) > str(week_ago)) # last_active contains type(data)=str
# print(str(now) < str(week_ago)) # last_active contains type(data)=str

date1 = ' 2022-09-22 18:47:32'
date2 = '2022-09-16 12:13:05'
print(date1<date2)