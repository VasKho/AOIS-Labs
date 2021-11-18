import parser
import minimizer


def test(function):
    print()
    print("function: ", function)
    
    print()
    pdnf = parser.make_pdnf(parser.build_truth_table(parser.resolve_inversions(function)))
    print("pdnf", pdnf)
    index_pdnf = parser.to_number_form(parser.build_truth_table(pdnf))
    minimized_pdnf = minimizer.minimize_Quine(pdnf)
    index_of_minimized_pdnf = parser.to_number_form(parser.build_truth_table(minimized_pdnf))
    if (index_pdnf == index_of_minimized_pdnf):
        print("Test passed:")
    else: print("Test failed:")
    minimizer.to_end_form(pdnf)

    
    pcnf = parser.make_pcnf(parser.build_truth_table(parser.resolve_inversions(function)))
    print()
    print("pcnf: ", pcnf)


    index_pcnf = parser.to_number_form(parser.build_truth_table(pdnf))
    minimized_pcnf = minimizer.minimize_Quine(pdnf)

    index_of_minimized_pcnf = parser.to_number_form(parser.build_truth_table(minimized_pcnf))

    if (index_pcnf == index_of_minimized_pcnf):
        print("Test passed:")
    else: print("Test failed:")
    minimizer.to_end_form(pcnf)


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