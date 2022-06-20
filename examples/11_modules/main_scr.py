#!/usr/bin/env python3

# hello.py & mail.py are located in common catalogue

#import hello

#hello.my_func()
#print(hello.name)

#olga=hello.Student('Olga', 'Python basic')
#olga.get_student_details()


# hello.py & mail.py are located in different catalogue

import sys
sys.path.append('/Users/Olha/Documents/Python_2021/Python_summer2021/examples/12_useful_modules')

import hello

hello.my_func()
print(hello.name)
