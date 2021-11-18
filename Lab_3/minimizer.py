import re
import numpy
import itertools, functools

from utils import (
        TYPE_OF_FUNC,
        ImplicantIsNecessary,
        find_type_of_function,
        split_function,
        joining_rule,
        find_kernel,
        build_KMap,
        find_surrounding,
        translate_to_implicant,
        convert_to_eval,
        convert_to_human
)


def to_end_form(function):
    print("Joining rule: ", joining_rule(function))
    print("minimize computation: ", str(find_odd(function)))
    print("minimize Quine", minimize_Quine(function))
    print("minimize Map", minimize_KMap(function))



'''
A function that will check if the implicant is unnecessary
(computational method for minimizing functions)
Algorithm:
1. Find all variables used by the function
2. For each implicant:
3. check variables used in the implicant
4. Check on which valueset_implicant implicant will be equal to 1 (disjunctive)|0 (conjunctive)
5. Generate array of valueset_function (valueset_implicant + all combinations of remaining variables) 
6. if for every such valueset_function remainder of function (function - implicant checked) 
   is equal to 1 (disjunctive)|0 (conjunctive), the checked implicant is unnecessary
'''
def find_odd(function):
    function = joining_rule(function)
    function_splitted = split_function(function)
    function_type = find_type_of_function(function)

    #Determining the number of variables in the function (by searching for every unique letter)
    function_variables = set(re.findall(r'[a-z]',function))

    for implicant in function_splitted:
        try:
        #find all variables used by an implicant
            implicant_variables = set(re.findall(r'[a-z]',"".join(implicant)))
            function_remainder = function_splitted[:]
            function_remainder.remove(implicant)

            #generate valuesets for the implicant to
            implicant_combinations = itertools.product(range(2), repeat=len(implicant_variables))

            #convert them to a dict for eval (looks like {"var1": value_1, "var2": value_2} )
            # implicant_valuesets = []
            # for combination in implicant_combinations:
            #     implicant_valuesets.insert
            implicant_valuesets = [{list(implicant_variables)[ind]: val for ind,val in enumerate(combination)} for combination in implicant_combinations]
                

            #finding the valueset when implicant is equal to 0|1
            control_valueset = {}
            for valueset in implicant_valuesets:
                if (eval(convert_to_eval([implicant], function_type), valueset) == function_type.value):
                    control_valueset = valueset
            
            #if the remaining function is still 0|1 on this valueset, it means that the implicant is unnecessary
            #let's complete the valueset we're checking to all combinations of variables in the remaining function
            variables_to_complete = function_variables - implicant_variables
            #generate combinations
            combinations_for_completion = itertools.combinations(range(2), len(variables_to_complete))

            #for each combination of remaining variables, create a valueset of control_valueset (implicant) + variables_to_complete combination
            combinations_for_completion = [{ list(variables_to_complete)[ind]: val for ind,val in enumerate(valueset)} for valueset in combinations_for_completion]
            

            # valueset = completion variables, control_valueset = valueset when implicant is equal to 1|0, | is the "+" for dicts, basically (merge)
            for valueset in combinations_for_completion:
                #if on any valueset we generated the value is not the same as on implicant, the implicant is NOT unnecessary
                if (eval(convert_to_eval(function_remainder, function_type), {**valueset, **control_valueset}) is not function_type.value): 
                    raise ImplicantIsNecessary()

            #this code is unaccessable unless the previous check shown that implicant is UNnecessary
            function_splitted.remove(implicant)

        except ImplicantIsNecessary: 
            continue
    return convert_to_human(function_splitted,function_type)









        




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
                    elif surrounding[row_iter + 1][1] == valuable_number:
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
                    elif surrounding[row_iter - 1][1] == valuable_number:
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
