import parser
import minimizer


def test(function):
    pdnf = parser.make_pdnf(parser.build_truth_table(parser.to_disjunctive_normal_form(function)))
    index = parser.to_number_form(parser.build_truth_table(pdnf))
    func = minimizer.minimize_Quine(pdnf)
    index_of_minimized = parser.to_number_form(parser.build_truth_table(func))
    if index == index_of_minimized:
        print(function, " |||| ", func, " |||| ", "Test passed")
    else:
        print(function, " |||| ", func, " |||| ", "Test failed")


test("~((~a+~b)*~(~a*~c))")
test("~((~a+~b)*~(~a*c))")
test("~((~a+b)*~(~a*~c))")
test("~((~a+b)*~(~a*c))")
test("~((a+~b)*~(a*~c))")
test("~((a+~b)*~(a*c))")
test("~((a+b)*~(a*~c))")
test("~((a+b)*~(a*c))")
test("~((~a+~b)*~(~b*~c))")
test("~((~a+~b)*~(~b*c))")
test("~((~a+b)*~(b*~c))")
test("~((~a+b)*~(b*c))")
test("~((a+~b)*~(~b*~c))")
test("~((a+~b)*~(~b*c))")
test("~((a+b)*~(b*~c))")
test("~((a+b)*~(b*c))")
test("~((~b+~c)*~(~a*~c))")
test("~((~b+c)*~(~b*c))")
test("~((b+~c)*~(~b*~c))")
test("~((b+c)*~(~a*c))")
test("~((~b+~c)*~(a*~c))")
test("~((~b+c)*~(a*~c))")
test("~((b+~c)*~(a*c))")
test("~((b+c)*~(a*c))")
test("~((~a+~c)*~(~b*~c))")
test("~((~a+c)*~(~b*c))")
test("~((~a+~c)*~(b*~c))")
test("~((~a+c)*~(b*c))")
test("~((a+~c)*~(~b*~c))")
test("~((a+c)*~(~b*c))")
test("~a*b+c")
