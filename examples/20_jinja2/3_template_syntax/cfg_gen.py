# -*- coding: utf-8 -*-
import os
import sys
# from sys import argv # in this case

import yaml
from jinja2 import Environment, FileSystemLoader

# $ python cfg_gen.py templates/for.txt data_files/for.yml - write into CLI to run the script :
# this scrip is not require any modification to work with other inputs

templates_dir, template_file = os.path.split(sys.argv[1]) # path and filename of template

    # <<testing that split method applied to path works correctly>>
    # tem_dir,temp=os.path.split('templates/for.txt') # template
    # print(temp)
    # print(tem_dir)

    # <<testing that split method applied to path works correctly>>
    # tem_dir,temp=os.path.split('data_files/for.ymlt') #variables
    # print(temp)
    # print(tem_dir)

vars_file = sys.argv[2] # path and filename of file with inputs (variables)

env = Environment(
    loader=FileSystemLoader(templates_dir), # Environment - описания параметров окружения (загрузчик - тут указывается путь к каталогу, где находятся шаблоны)
    trim_blocks=True, # to manage whitespace -> удаляет первую пустую строку после блока конструкции, если его значение равно True
    lstrip_blocks=True) # to manage whitespace -> параметр контролирует будут ли удаляться пробелы и табы от начала строки до начала блока (до открывающейся фигурной скобки).
template = env.get_template(template_file)

with open(vars_file) as f:
    vars_dict = yaml.safe_load(f)

print(template.render(vars_dict))
