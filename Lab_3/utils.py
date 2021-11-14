import re
import numpy
from enum import Enum


class TYPE_OF_FUNC(Enum):
    DISJUNCTIVE = 0
    CONJUNCTIVE = 1


def find_type_of_function(function):
    result_flag = re.search(r"^~?(\w|True|False)(\*~?(\w|True|False))*(\s\+\s~?(\w|True|False)(\*~?(\w|True|False))*)*$", function)
    type_of_func = TYPE_OF_FUNC.DISJUNCTIVE
    if result_flag is None:
        result_flag = re.search(r"^\(?~?\w(\+~?\w\)?)*(\s\*\s\(?~?\w(\+~?\w\)?)*)*$", function)
        type_of_func = TYPE_OF_FUNC.CONJUNCTIVE
    if result_flag is None:
        raise Exception("Invalid input!")
    return type_of_func


def represent_in_values(function, implicant, first_value, second_value):
    char_1 = re.search(r'\w', implicant[0])
    char_1 = char_1.group()
    function = re.sub(char_1, str(first_value), function)
    char_2 = re.search(r'\w', implicant[1])
    char_2 = char_2.group()
    function = re.sub(char_2, str(second_value), function)
    function = re.sub(r'~0', 'True', function)
    function = re.sub(r'~1', 'False', function)
    function = re.sub(r'1', 'True', function)
    function = re.sub(r'0', 'False', function)
    return function


def split_function(function):
    type_of_func = find_type_of_function(function)
    function_splitted = []

    if type_of_func == TYPE_OF_FUNC.DISJUNCTIVE:
        function = function.split(' + ')
        for elem in function:
            function_splitted.append(elem.split('*'))
    else:
        function = function.replace('(', '')
        function = function.replace(')', '')
        function = function.split(' * ')
        for elem in function:
            function_splitted.append(elem.split('+'))
    return function_splitted


def joining_rule(function):
    type_of_func = find_type_of_function(function)
    function_splitted = split_function(function)

    result = set()
    first_elem_index = 0
    while first_elem_index < len(function_splitted):
        second_elem_index = 0
        while second_elem_index < len(function_splitted):
            first_el = function_splitted[first_elem_index]
            second_el = function_splitted[second_elem_index]
            if len(set(first_el) ^ set(second_el)) == 2:
                sum = set(first_el) & set(second_el)
                function_splitted.remove(first_el)
                function_splitted.remove(second_el)
                if type_of_func == TYPE_OF_FUNC.DISJUNCTIVE:
                    result.add("*".join(sum))
                else:
                    result.add("+".join(sum))
                first_elem_index = 0
                second_elem_index = 0
                continue
            second_elem_index += 1
        first_elem_index += 1
    if type_of_func == TYPE_OF_FUNC.DISJUNCTIVE:
        result = " + ".join(result)
    else:
        result = " * ".join(result)
    for remaining in function_splitted:
        if type_of_func == TYPE_OF_FUNC.DISJUNCTIVE:
            result += ' + ' + "*".join(remaining)
        else:
            result += ' * ' + "+".join(remaining)
    return result


def find_kernel(perfect_form):
    type_of_func = find_type_of_function(perfect_form)
    simple_form = joining_rule(perfect_form)
    perfect_form_splitted = split_function(perfect_form)
    simple_form_splitted = split_function(simple_form)

    table = numpy.zeros(shape=(len(simple_form_splitted),
                               len(perfect_form_splitted)))

    for constituent in range(len(perfect_form_splitted)):
        for implicant in range(len(simple_form_splitted)):
            if set(simple_form_splitted[implicant]).issubset(perfect_form_splitted[constituent]):
                table[implicant][constituent] = 1
    kernel = []
    kernel_search_result = numpy.count_nonzero(table == 1, axis=0)
    for index in range(len(kernel_search_result)):
        if kernel_search_result[index] == 1:
            for element in range(len(table[:, index])):
                if table[element][index] == 1:
                    if simple_form_splitted[element] not in kernel:
                        kernel.append(simple_form_splitted[element])
    kernel_result = ""
    if type_of_func == TYPE_OF_FUNC.DISJUNCTIVE:
        for implicant in range(len(kernel)):
            kernel[implicant] = "*".join(kernel[implicant])
            kernel_result += kernel[implicant] + ' + '
    else:
        for implicant in range(len(kernel)):
            kernel[implicant] = "+".join(kernel[implicant])
            kernel_result += '(' + kernel[implicant] + ')' + ' * '
    kernel_result = kernel_result[: len(kernel_result) - 3]
    return kernel_result
