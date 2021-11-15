import numpy
import re
from minimizer.minimizer import minimize_KMap
from minimizer.parser import make_pdnf


def build_truth_table_4_vars(function):
    function = re.sub(r'\+', ' | ', function)
    function = re.sub(r'\*', ' & ', function)
    table = numpy.zeros(shape=(5, 16))
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
                for d in range(2):
                    d_value = str(d)
                    d = re.sub(r'd', d_value, c)
                    d = re.sub(r'~1', 'False', d)
                    d = re.sub(r'~0', 'True', d)
                    d = re.sub(r'0', 'False', d)
                    d = re.sub(r'1', 'True', d)
                    table[0][i] = a_value
                    table[1][i] = b_value
                    table[2][i] = c_value
                    table[3][i] = d_value
                    table[4][i] = eval(d)
                    i += 1
    return table


def make_pdnf_4_vars(table):
    j = 0
    function = []
    for i in table[4]:
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
            if table[3][j] == 1:
                d = 'd'
            else:
                d = '~d'
            function.append(a + '*' + b + '*' + c + '*' + d)
        j += 1
    function = " + ".join(function)
    return function


adder_table = [
        [0, 0, 0, 0, 1, 1, 1, 1],
        [0, 0, 1, 1, 0, 0, 1, 1],
        [0, 1, 0, 1, 0, 1, 0, 1],
        [0, 1, 1, 0, 1, 0, 0, 1]
        ]

carry_table = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 1, 1],
        [0, 1, 0, 1, 0, 1, 0, 1],
        [0, 0, 0, 1, 0, 1, 1, 1]
        ]


def adder(a, b, c):
    adder_function = minimize_KMap(make_pdnf(adder_table))
    carry_function = minimize_KMap(make_pdnf(carry_table))
    output = (adder_function, carry_function)
    a = bool(a)
    b = bool(b)
    c = bool(c)
    result = []
    for out in output:
        out = re.sub(r"~", "not ", out)
        out = re.sub(r"\*", " and ", out)
        out = re.sub(r"\+", " or ", out)
        result.append(out)
    return (int(eval(result[0])), int(eval(result[1])))


# for i in range(2):
#     for j in range(2):
#         for k in range(2):
#             for z in range(2):
#                 num = "".join(str(i) for i in [i, j, k, z])
#                 num = int(num, 2)
#                 print(bin(num), bin(num + 2))


table = build_truth_table_4_vars("~a*b*c + a*~b*~c")

print(table)

pdnf = make_pdnf_4_vars(table)

print(pdnf)

print(build_truth_table_4_vars(pdnf))
