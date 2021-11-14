import numpy


from utils import (
        TYPE_OF_FUNC,
        find_type_of_function,
        split_function,
        represent_in_values,
        joining_rule,
        find_kernel,
        build_KMap,
        find_surrounding,
        translate_to_implicant
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


def minimize_KMap(perfect_form):
    KMap_template = build_KMap(perfect_form)
    valuable_number = 1
    type_of_func = find_type_of_function(perfect_form)
    if type_of_func == TYPE_OF_FUNC.CONJUNCTIVE:
        valuable_number = 0
    minimized = set()
    col_iter, row_iter = 0, 0
    while row_iter < KMap_template.shape[0]:
        while col_iter < KMap_template.shape[1]:
            surrounding = find_surrounding(KMap_template, (row_iter, col_iter))
            if row_iter == 0:
                if surrounding[row_iter][1] == valuable_number:
                    if surrounding[row_iter][2] == valuable_number:
                        if surrounding[row_iter + 1][1] == valuable_number and surrounding[row_iter + 1][2] == valuable_number:
                            minimized.add(translate_to_implicant((row_iter, col_iter), 3))
                        else:
                            minimized.add(translate_to_implicant((row_iter, col_iter), 0))
                    elif surrounding[row_iter][0] == valuable_number:
                        if surrounding[row_iter + 1][1] == valuable_number and surrounding[row_iter + 1][0] == valuable_number:
                            minimized.add(translate_to_implicant((row_iter, col_iter), 4))
                        else:
                            minimized.add(translate_to_implicant((row_iter, col_iter), 1))
                    elif surrounding[row_iter + 1][col_iter] == valuable_number:
                        minimized.add(translate_to_implicant((row_iter, col_iter), 2))
                    elif surrounding[row_iter][1] == valuable_number:
                        minimized.add(translate_to_implicant((row_iter, col_iter), 5))
            elif row_iter == 1:
                if surrounding[row_iter][1] == valuable_number:
                    if surrounding[row_iter][2] == valuable_number:
                        if surrounding[row_iter - 1][1] == valuable_number and surrounding[row_iter - 1][2] == valuable_number:
                            minimized.add(translate_to_implicant((row_iter, col_iter), 3))
                        else:
                            minimized.add(translate_to_implicant((row_iter, col_iter), 0))
                    elif surrounding[row_iter][0] == valuable_number:
                        if surrounding[row_iter - 1][1] == valuable_number and surrounding[row_iter - 1][0] == valuable_number:
                            minimized.add(translate_to_implicant((row_iter, col_iter), 4))
                        else:
                            minimized.add(translate_to_implicant((row_iter, col_iter), 1))
                    elif surrounding[row_iter - 1][col_iter] == valuable_number:
                        minimized.add(translate_to_implicant((row_iter, col_iter), 2))
                    elif surrounding[row_iter][1] == valuable_number:
                        minimized.add(translate_to_implicant((row_iter, col_iter), 5))
            col_iter += 1
        col_iter = 0
        row_iter += 1
    minimal_form = ""
    minimized = list(minimized)
    if type_of_func == TYPE_OF_FUNC.DISJUNCTIVE:
        for implicant in range(len(minimized)):
            if isinstance(minimized[implicant], tuple):
                minimized[implicant] = "*".join(minimized[implicant])
            minimal_form += minimized[implicant] + ' + '
    else:
        for implicant in range(len(minimized)):
            if isinstance(minimized[implicant], tuple):
                minimized[implicant] = "+".join(minimized[implicant])
            minimal_form += '(' + minimized[implicant] + ')' + ' * '
    return minimal_form[:len(minimal_form) - 3]


print(minimize_KMap('~a*~b*~c + ~a*b*~c + a*~b*c + a*~b*~c + a*b*~c'))
