import re

text='0xf,0xa,0x5' # цифры в шестнадцатеричной системе
match=re.findall(r'0x[\da-fA-F]',text) #

print(match)


text2='Olha Telizhuk : Kyiv, 1991'
match2=re.findall(r'\S',text2) # для лучшего понимания поиграться с короткими формулировками символьного класса

print(match2)


line1='+380958023959, Kyiv'
phone_num=re.findall(r"[+]38\d{10}", line1) # выбрать последовательность символов, которые записаны как номер телефона

print(phone_num)







