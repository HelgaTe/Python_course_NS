# func can be applied to any template/data files passed
# python parse_output.py templates/sh_ip_int_br.template output/sh_ip_int_br.txt
import sys

import textfsm
from tabulate import tabulate

template = sys.argv[1]
output_file = sys.argv[2]

with open(template) as f, open(output_file) as output: # считать содержимое файлов (template & output data)
    re_table = textfsm.TextFSM(f) # класс обрабатывает шаблон и создает из него объект в TextFSM
    header = re_table.header # отобрать заголовки таблиц
    result = re_table.ParseText(output.read()) # передать содержимое файла с output data в шаблон
    print(result)
    print(tabulate(result, headers=header))
