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
    if 'a' not in function or 'b' not in function or 'c' not in function: raise Exception('Invalid input!')
    

def find_inversion(function):
    # Find the deepest inversion in func
    check = re.search(r"~\(.+\)", function)
    if check is None: return function
    parenthesis_number = 0
    reading_state = READING_STATE.READING_SIMPLE
    # Start and end indexes show the current inversion, which will be replaced
    start_index = 0
    end_index = start_index
    inversion = ''
    for each_element in range(len(function)):
        # Find inversion like ~(...)
        if function[each_element] == '~':
            if function[each_element + 1] != '(':
                inversion += function[each_element]
                continue
            reading_state = READING_STATE.READING_INVERSION
            start_index = each_element
            end_index = start_index
            parenthesis_number = 0
            inversion = ''
        if function[each_element] == '(': parenthesis_number += 1
        if function[each_element] == ')': 
            parenthesis_number -= 1
            if parenthesis_number == 0 and reading_state == READING_STATE.READING_INVERSION:
                reading_state = READING_STATE.READING_SIMPLE
                inversion += function[each_element]
                end_index = each_element
                break
        inversion += function[each_element]
    # Transforms the function
    transformed_inversion = de_Morgan_rule(inversion)
    if len(inversion) == len(function):
        # Exept the situation of following statement (~a+b)
        function = function[ : start_index] + transformed_inversion + function[end_index + 1 : ]
        return function
    else:
        function = function[ : start_index] + '(' + transformed_inversion + ')' + function[end_index + 1 : ]
    return function


def de_Morgan_rule(inversion):
    buffer = inversion[2: len(inversion) - 1]
    parenthesis_number = 0
    # Find something like (...)*/+(...) and replace sign
    for elem in range(len(buffer)):
        if buffer[elem] == '(': parenthesis_number += 1
        if buffer[elem] == ')': parenthesis_number -= 1
        if buffer[elem] == '*' and parenthesis_number == 0:
            buffer = buffer[ : elem] + '+' + buffer[elem+1:]
        elif buffer[elem] == '+' and parenthesis_number == 0:
            buffer = buffer[ : elem] + '*' + buffer[elem+1:]
    # Add inversion signs
    buffer = '~' + buffer
    for elem in range(len(buffer)):
        if buffer[elem] == '(': parenthesis_number += 1
        if buffer[elem] == ')': parenthesis_number -= 1
        if (buffer[elem] == '+' or buffer[elem] == '*') and parenthesis_number == 0:
            buffer = buffer[:elem+1] + '~' + buffer[elem+1:]
    return buffer


def to_disjunctive_normal_form(function):
    function = find_inversion(function)
    temp = function
    while temp != find_inversion(function):
        temp = find_inversion(function)
        function = temp
    # while True:
    #     temp = find_inversion(function)
    #     if temp == function: break
    #     else: function = temp
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
    elem_in_res_row = 0
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
                table[0][elem_in_res_row] = a_value
                table[1][elem_in_res_row] = b_value
                table[2][elem_in_res_row] = c_value
                table[3][elem_in_res_row] = eval(c)
                elem_in_res_row += 1
    return table


def print_truth_table(table):
    args = ['a  ', 'b  ', 'c  ', 'res']
    args_iter = 0
    for col_value in table:
        row = numpy.array2string(col_value)
        row = row.replace('[', '')
        row = row.replace('.', '')
        row = row.replace(']', '')
        print(args[args_iter] + ' |' + row)
        print('--------------------')
        args_iter += 1


def make_pcnf(table):
    row_index = 0
    function = []
    for col_value in table[3]:
        if col_value == 0:
            a = b = c = 0
            if table[0][row_index] == 0:
                a = 'a'
            else:
                a = '~a'
            if table[1][row_index] == 0:
                b = 'b'
            else:
                b = '~b'
            if table[2][row_index] == 0:
                c = 'c'
            else:
                c = '~c'
            function.append(a + '+' + b + '+' + c)
        row_index += 1
    function = " * ".join(function)
    return function


def make_pdnf(table):
    row_index = 0
    function = []
    for col_value in table[3]:
        if col_value == 1:
            a = b = c = 0
            if table[0][row_index] == 1:
                a = 'a'
            else:
                a = '~a'
            if table[1][row_index] == 1:
                b = 'b'
            else:
                b = '~b'
            if table[2][row_index] == 1:
                c = 'c'
            else:
                c = '~c'
            function.append(a + '*' + b + '*' + c)
        row_index += 1
    function = " + ".join(function)
    return function


def to_number_form(table):
    row = numpy.array2string(table[3])
    row = row.replace('[', '')
    row = row.replace('.', '')
    row = row.replace(']', '')
    row = row.replace(' ', '')
    return int(row, 2)
