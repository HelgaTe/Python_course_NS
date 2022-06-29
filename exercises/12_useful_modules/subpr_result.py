# import subprocess
#
# def subpr_result(command, filename):
#     with open(filename, 'w') as f:
#         subpr_result = subprocess.run(command, stdout=f, text=True)
#
# # if __name__ == "__main__":
#
# subpr_result('ls', 'my_test.txt')


import subprocess

def subpr_result(command, file):
    """
    collect the results of the command in a file
    :param command: command executed
    :param file: input file name to write the result down
    """
    with open(file, 'w') as f:
        subpr_result = subprocess.run(command, stdout=f, text=True)

subpr_result('ls','my_test_py.txt')

if __name__ == "__main__":
    subpr_result('ls', 'my_test.txt')
