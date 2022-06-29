import subprocess

res=subprocess.run(
    'echo Hello $USER ',
    shell=True,
    capture_output=True,
    text=True) # command and arguments to the command
print('-'*40)
# dir() возвращает список допустимых атрибутов для указанного объекта
print(*dir(res),sep='\n')
print('-'*40)
print(res.stdout)
print('-'*40)
print(res.stderr)
print('-'*40)
print(res.returncode)



