import numpy
from enum import Enum
import re


class READING_STATE(Enum):
    READING_SIMPLE = 0
    READING_INVERSION = 1

def check_input(function):
    allowed_symbols = "abc+*~()"
    for i in function:
        if allowed_symbols.find(i) == -1:
            raise Exception('Invalid Input!')
    

def find_inversion(function):
    check = re.search(r"~\(.+\)", function)
    if check is None: return function
    parenthesis_number = 0
    reading_state = READING_STATE.READING_SIMPLE
    start_index = 0
    end_index = start_index
    inversion = ''
    for i in range(len(function)):
        if function[i] == '~':
            if function[i + 1] != '(':
                inversion += function[i]
                i += 1
                continue
            reading_state = READING_STATE.READING_INVERSION
            start_index = i
            end_index = start_index
            parenthesis_number = 0
            inversion = ''
        if function[i] == '(': parenthesis_number += 1
        if function[i] == ')': 
            parenthesis_number -= 1
            if parenthesis_number == 0 and reading_state == READING_STATE.READING_INVERSION:
                reading_state = READING_STATE.READING_SIMPLE
                inversion += function[i]
                end_index = i
                break
        inversion += function[i]
    transformed_inversion = de_Morgan_rule(inversion)
    if len(inversion) == len(function):
        function = function[ : start_index] + transformed_inversion + function[end_index + 1 : ]
        return function
    else:
        function = function[ : start_index] + '(' + transformed_inversion + ')' + function[end_index + 1 : ]
    return function


def de_Morgan_rule(inversion):
    buffer = inversion[2: len(inversion) - 1]
    parenthesis_number = 0
    for i in range(len(buffer)):
        if buffer[i] == '(': parenthesis_number += 1
        if buffer[i] == ')': parenthesis_number -= 1
        if buffer[i] == '*' and parenthesis_number == 0:
            buffer = buffer[ : i] + '+' + buffer[i+1:]
        elif buffer[i] == '+' and parenthesis_number == 0:
            buffer = buffer[ : i] + '*' + buffer[i+1:]
    buffer = '~' + buffer
    for i in range(len(buffer)):
        if buffer[i] == '(': parenthesis_number += 1
        if buffer[i] == ')': parenthesis_number -= 1
        if (buffer[i] == '+' or buffer[i] == '*') and parenthesis_number == 0:
            buffer = buffer[:i+1] + '~' + buffer[i+1:]
    return buffer


def resolve_inversions(function):
    function = find_inversion(function)
    temp = function
    while True:
        temp = find_inversion(function)
        if temp == function: break
        else: function = temp
    function = normalize(function)
    return function


def normalize(function):
    find_something = re.search(r"(~~)+\w", function)
    while find_something is not None:
        replace_char = find_something.group()
        replace_char = replace_char.replace('~', '')
        function = re.sub(r"(~~)+\w", replace_char, function, 1)
        find_something = re.search(r"(~~)+\w", function)
    return function


def build_truth_table(function):
    function = re.sub(r'\+', ' | ', function)
    function = re.sub(r'\*', ' & ', function)
    table = numpy.zeros(shape=(4, 8))
    solved = function
    i = 0
    for a in range(2):
        a_value = str(a)
        a = re.sub(r'a', a_value, solved)
        for b in range(2):
            b_value = str(b)
            b = re.sub(r'b', b_value, a)
            for c in range(2):
                c_value = str(c)
                c = re.sub(r'c', c_value, b)
                c = re.sub(r'~1', 'False', c)
                c = re.sub(r'~0', 'True', c)
                c = re.sub(r'0', 'False', c)
                c = re.sub(r'1', 'True', c)
                table[0][i] = a_value
                table[1][i] = b_value
                table[2][i] = c_value
                table[3][i] = eval(c)
                i += 1
    return table


def print_truth_table(table):
    args = ['a  ', 'b  ', 'c  ', 'res']
    args_iter = 0
    for i in table:
        row = numpy.array2string(i)
        row = row.replace('[', '')
        row = row.replace('.', '')
        row = row.replace(']', '')
        print(args[args_iter] + ' |' + row)
        print('--------------------')
        args_iter += 1


def make_pcnf(table):
    j = 0
    function = []
    for i in table[3]:
        if i == 0:
            a = b = c = 0
            if table[0][j] == 0:
                a = 'a'
            else:
                a = '~a'
            if table[1][j] == 0:
                b = 'b'
            else:
                b = '~b'
            if table[2][j] == 0:
                c = 'c'
            else:
                c = '~c'
            function.append(a + '+' + b + '+' + c)
        j += 1
    # function = " * ".join(function)
    result = ""
    for elem in function:
        result += '(' + elem + ')' + ' * '
    return result[: len(result) - 3]


def make_pdnf(table):
    j = 0
    function = []
    for i in table[3]:
        if i == 1:
            a = b = c = 0
            if table[0][j] == 1:
                a = 'a'
            else:
                a = '~a'
            if table[1][j] == 1:
                b = 'b'
            else:
                b = '~b'
            if table[2][j] == 1:
                c = 'c'
            else:
                c = '~c'
            function.append(a + '*' + b + '*' + c)
        j += 1
    function = " + ".join(function)
    return function


def to_number_form(table):
    row = numpy.array2string(table[3])
    row = row.replace('[', '')
    row = row.replace('.', '')
    row = row.replace(']', '')
    row = row.replace(' ', '')
    return int(row, 2)
