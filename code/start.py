import sys
import os
from pandas import DataFrame

#       Define system and set encoding

if sys.platform == "linux" or sys.platform == "linux2":
    encoding = "utf-8"
elif sys.platform == "darwin":
    encoding = "utf-8"
elif sys.platform == "win32":
    encoding = "cp1251"
else:
    encoding = "utf-8"


# print('\n'*3, 'Its a Test of args work.', sep='', end='\n'*2)

args = sys.argv[1:]
print('Input arguments:', args, end='\n'*2)


assert args != [], "args is empty"

dirs, files, not_exist = [], [], []
#
#       Separate input dirs and .tex files.
#      if find mistakes in args, will report.
#
for argument in args:
    if os.path.isdir(argument):
        dirs.append(os.path.abspath(argument))
    elif os.path.isfile(argument) and argument.endswith('.tex'):
        files.append(os.path.abspath(argument))
    else:
        not_exist.append(argument)
#
#       Report about not exist files or paths in input args.
if not_exist != []:

    print('\n'*2, '#'*64, sep='', end='\n'*2)
    print('In input files find not exist files or directories.\n\n')

    for i in not_exist:
        print(i)

    # print('\n\nCheck it and restart script with right arguments'
    # \ or continue without them.')
    print('\n', '#'*64, sep='', end='\n'*2)

    #
    #   Здесь диалоговое сообщение
    #
    user_solution = input('Continue without them?  [Y/n]\n\n').lower().strip()
    if user_solution in ['n', 'not']:
        quit()

# del user_solution, not_exist, args

for directory in dirs:
    # r, d, f is a root, directories, files
    for r, d, f in os.walk(directory, topdown=False):
        for name in f:
            if name.endswith('.tex'):
                files.append(os.path.join(r, name))

# Remove duplicate files
files = list(set(files))

print('In the end, files we have', len(files), 'files:\n')
# for name in files:
#    print(name)

print('\nStart read files:')

data = {}
# Count of $
count_inline_formulas = 0
# Count of $$
count_formulas = 0
# Count of procent char %
count_procent_char = 0
# Count of hash char #
count_hash_char = 0


def append_if_exist(hashtable, command):
    """ Increment frequency counter in hashtable
    or create new field if find new command
    """
    if command in hashtable.keys():
        hashtable[command] += 1
    else:
        hashtable[command] = 1
    pass


def separate(hashtable, line):
    """ Fix command syntax, before write in hash table.
    Input line is already without spaces.
    """
    for command in words:
        if command[0] == "\\":
            if command[-1] == "{":
                append_if_exist(hashtable, command + "}")
            else:
                append_if_exist(hashtable, command)


def find_formulas(command, count_formulas, count_inline_formulas,
                  count_procent_char=0, count_hash_char=0
                  ):
    """
    Search specific char in phrase.
    """
    # В будущем можно добавить анализ длины
    # This function could be improved to count other specific characters
    # Also, calculation of lengths of formulas may be added in the future
    previous_char = ""
    for char in command:
        if char == "$":
            if previous_char == "$":
                count_formulas += 1
            else:
                count_inline_formulas += 1
        elif char == "%":
            count_procent_char += 1
        elif char == "#":
            count_hash_char += 1
        previous_char = char


for file in files:
    with open(file, "r", encoding=encoding) as f:
        for line in f:
            words = line.split("\\")
            if len(words) == 1:
                find_formulas(words[0], count_formulas, count_inline_formulas)
                continue
            # Now working with phrases, which began with \ symbol
            # for clarity, we will write commands with \, so return \ symbol
            words = list(map(lambda x: "\\" + x, words))
            #
            # Split words by spaces and pack all in list
            comma = []
            for word in words:
                comma += word.split()
            words = comma

            for command in words:
                if command[0] == "\\":
                    separate(data, command)
                else:
                    find_formulas(command, count_formulas,
                                  count_inline_formulas)

count_formulas = count_formulas/2
count_inline_formulas = count_inline_formulas/2

print('\n'*3, 'Ok')
#
#
# #print("See tex files:\n\n")
# #
# #for filename, text in src.items():
# #   print(filename, ":\n")
# #   print(text, end='\n\n\n')
# #   next = input("\nNext?").lower().strip()
# #   if next not in ['', 'y', 'yes']:
# #       break
#
#
# # Start search special comands in src
# # Dictionary:       command - frequency
# commands = {}
# CR = "\n"
# spaces = [' ', '\t', '\n']
# for text in src.values():
#     previous_char = ""
#     current_command = ""
#     for char in text:
#         if pevious_char = "\\":
#           while char != "{"


#       Export in csv
#
# DataFrame.from_dict(data, orient="index", columns=["Command", "No"])


# Try rewrite dictionary without \
#
# new_dict = {}
# for command, count in data.items():
#     # print(count, ":\t", command, end="\n\n")
#     new_dict[command[1:]] = count
#
#
# DataFrame.from_dict(data, orient="index", columns=["Command", "No"])
