import numpy
import re
from minimizer.minimizer import (minimize_KMap, minimize_Quine)
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
    print("Adder PDNF: ", make_pdnf(adder_table))
    adder_function = minimize_KMap(make_pdnf(adder_table))
    print("Adder minimized: ", adder_function, "\n")
    print("Carry PDNF: ", make_pdnf(carry_table))
    carry_function = minimize_KMap(make_pdnf(carry_table))
    print("Carry minimized: ", carry_function, "\n")
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


out1_table = [
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
        [0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
        [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]
        ]

out2_table = [
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
        [0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
        [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

out3_table = [
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
        [0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
        [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0]
        ]

out4_table = [
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
        [0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
        [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0]
        ]


def convert_8421_2(a, b, c, d):
    out1 = make_pdnf_4_vars(out1_table)
    print("Out 1 ", out1)
    print("Minimized: ", minimize_Quine(out1), '\n')
    out2 = make_pdnf_4_vars(out2_table)
    print("Out 2 ", out2)
    print("Minimized: ", minimize_Quine(out2), '\n')
    out3 = make_pdnf_4_vars(out3_table)
    print("Out 3 ", out3)
    print("Minimized: ", minimize_Quine(out3), '\n')
    out4 = make_pdnf_4_vars(out4_table)
    print("Out 4 ", out4)
    print("Minimized: ", minimize_Quine(out4), '\n')
    output = (out1, out2, out3, out4)
    a = bool(a)
    b = bool(b)
    c = bool(c)
    d = bool(d)
    result = []
    for out in output:
        out = re.sub(r"~", "not ", out)
        out = re.sub(r"\*", " and ", out)
        out = re.sub(r"\+", " or ", out)
        result.append(out)
    return (int(eval(result[0])), int(eval(result[1])), int(eval(result[2])), int(eval(result[3])))


adder(0, 1, 0)
convert_8421_2(0, 0, 1, 1)
