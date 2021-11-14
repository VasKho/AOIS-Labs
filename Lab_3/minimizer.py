import numpy
from parser import (
        build_truth_table,
        print_truth_table
)

from utils import (
        TYPE_OF_FUNC,
        find_type_of_function,
        split_function,
        represent_in_values,
        joining_rule,
        find_kernel
)


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


def minimize_Quine(perfect_form):
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
            minimal_form += '(' + result[implicant] + ')' + ' * '
    return minimal_form[: len(minimal_form) - 3]


def minimize_KMap(perfect_from):
    truth_table = build_truth_table(perfect_from)
    print_truth_table(truth_table)
    KMap_template = numpy.zeros(shape=(2, 4))
    KMap_template[0][0] = truth_table[3][0]
    KMap_template[0][1] = truth_table[3][1]
    KMap_template[0][3] = truth_table[3][2]
    KMap_template[0][2] = truth_table[3][3]
    KMap_template[1][0] = truth_table[3][4]
    KMap_template[1][1] = truth_table[3][5]
    KMap_template[1][3] = truth_table[3][6]
    KMap_template[1][2] = truth_table[3][7]
    print(KMap_template)
    col_iter, row_iter = 0, 0
    while row_iter < KMap_template.shape[0]:
        while col_iter < KMap_template.shape[1]:
            print(col_iter, row_iter)
            col_iter += 1
        row_iter += 1


minimize_KMap('~a*~b*~c + ~a*b*~c + a*~b*c + a*~b*~c + a*b*~c')
