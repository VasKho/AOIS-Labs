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
        result_flag = re.search(r"^~?\w(\+~?\w)*(\s\*\s~?\w(\+~?\w)*)*$", function)
        type_of_func = TYPE_OF_FUNC.CONJUNCTIVE
    if result_flag is None:
        raise Exception("Invalid input!")
    return type_of_func


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
    if len(function_splitted) == 1:
        if type_of_func == TYPE_OF_FUNC.DISJUNCTIVE:
            result += ' + ' + "*".join(function_splitted[0])
        else:
            result += ' * ' + "+".join(function_splitted[0])
    return result


def to_end_form(function):
    function = joining_rule(function)
    function = find_odd(function)

# for implicant in expr
#     for set_of_values in implicant
#         if implicant == 1 and expr (without implicant) == 1
#             then expr.remove(implicant)


def find_odd(function):
    type_of_func = find_type_of_function(function)
    function_splitted = split_function(function)
    print(function_splitted)

    for implicant in range(len(function_splitted)):
        print(function_splitted[implicant])
        for first_value in range(2):
            for second_value in range(2):
                form_in_numbers = represent_in_values(function, function_splitted[implicant], first_value, second_value)

                if type_of_func == TYPE_OF_FUNC.DISJUNCTIVE:
                    splitted_form_in_numbers = form_in_numbers.split(' + ')
                    print(splitted_form_in_numbers)
                    implicants = function_splitted
                    if eval(splitted_form_in_numbers[implicant]) == 1:
                        implicants.pop(implicant)
                        result = ''
                        for addendum_iter in range(len(function_splitted[implicants])):
                            result += function_splitted[implicants][addendum_iter][0] + "*" + function_splitted[implicants][addendum_iter][1] + ' + '
                        implicants_in_string = result[: len(result) - 3]
                        try:
                            if eval(represent_in_values(implicants_in_string, function_splitted[implicants][0], first_value, second_value)) == 1:
                                print("YES")
                                function_splitted.pop(implicant)
                        except (NameError):
                            print(function_splitted)
                            for addendum in form_in_numbers:
                                if 'True' in addendum:
                                    addendum.remove('True')
                            pass
                else:
                    print('this func is in conjunctive form')
                    # TODO: add for conjunctive form
    return function_splitted


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


def minimize_in_table(perfect_form):
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
    kernel = find_kernel(perfect_form)
    kernel_splitted = split_function(kernel)
    arr = numpy.count_nonzero(table == 1, axis=1)
    result = []
    for index in range(len(arr)):
        if arr[index] == 1 or simple_form_splitted[index] in kernel_splitted:
            result.append(simple_form_splitted[index])
    minimal_form = ""
    if type_of_func == TYPE_OF_FUNC.DISJUNCTIVE:
        for implicant in range(len(result)):
            result[implicant] = "*".join(result[implicant])
            minimal_form += result[implicant] + ' + '
    else:
        for implicant in range(len(result)):
            result[implicant] = "+".join(result[implicant])
            minimal_form += '( ' + minimal_form[implicant] + ' )' + ' * '
    print(minimal_form[: len(minimal_form) - 3])
    return minimal_form[: len(minimal_form) - 3]


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
            kernel_result += '( ' + kernel[implicant] + ' )' + ' * '
    kernel_result = kernel_result[: len(kernel_result) - 3]
    return kernel_result


def split_function(function):
    type_of_func = find_type_of_function(function)
    function_splitted = []

    if type_of_func == TYPE_OF_FUNC.DISJUNCTIVE:
        function = function.split(' + ')
        for elem in function:
            function_splitted.append(elem.split('*'))
    else:
        function = function.split(' * ')
        for elem in function:
            function_splitted.append(elem.split('+'))
    return function_splitted


# print(find_odd("c*~a + c*~b + ~b*a + ~c*a"))
minimize_in_table("~a*~b*c + a*~b*~c + a*~b*c + a*b*~c + a*b*c")

# minimize_in_table("a+b+~c * a+~b+c * a+~b+~c * ~a+b+~c")
