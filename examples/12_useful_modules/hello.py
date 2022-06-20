#!/usr/bin/env python3

def my_func():
        print('hello world')
        
# this variable will be callable in other modules
name='Olga'

# defining a class

class Student:
        def __init__(self,name,course):
                self.course=course
                self.name=name

        def get_student_details(self):
                print('Your name is ' + self.name + '.')
                print('You are studing ' + self.course)

                
if __name__ == "__main__":
        # не выполнять при импорте 
        print('this is core file')
        print('data (veriables, def etc. are imported from this one')
