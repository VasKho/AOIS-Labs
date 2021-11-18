import parser
import minimizer

# def solve(function):
# 
#     print('Function:\n' + function)
# 
#     parser.check_input(function)
# 
#     function = parser.to_disjunctive_normal_form(function)
# 
#     print('Simplified function:\n' + function)
# 
#     table = parser.build_truth_table(function)
# 
#     print('Truth table:')
# 
#     parser.print_truth_table(table)
# 
#     pdnf = parser.make_pdnf(table)
# 
#     print('Perfect disjunctive normal from:\n' + pdnf)
# 
#     pcnf = parser.make_pcnf(table)
# 
#     print('Perfect conjunctive normal form:\n' + pcnf)
# 
#     index = parser.to_number_form(table)
# 
#     print('Number form:\n' + str(index))
# 
# 
# def test(function, vector_function):
# 
#     parser.check_input(function)
# 
#     dnf = parser.to_disjunctive_normal_form(function)
# 
#     table = parser.build_truth_table(dnf)
# 
#     index = parser.to_number_form(table)
# 
#     if index == vector_function: print("Test passed for " + function)
#     else: print("Test failed for " + function)


# solve("~((b+c)*~(a*c))")

# print("\n")


# test("~((~a+~b)*~(~a*~c))", 163)
# test("~((~a+~b)*~(~a*c))", 172)
# test("~((~a+b)*~(~a*~c))", 172)
# test("~((~a+b)*~(~a*c))", 92)
# test("~((a+~b)*~(a*~c))", 58)
# test("~((a+~b)*~(a*c))", 53)
# test("~((a+b)*~(a*~c))", 202)
# test("~((a+b)*~(a*c))", 197)
# test("~((~a+~b)*~(~b*~c))", 139)
# test("~((~a+~b)*~(~b*c))", 71)
# test("~((~a+b)*~(b*~c))", 46)
# test("~((~a+b)*~(b*c))", 29)
# test("~((a+~b)*~(~b*~c))", 184)
# test("~((a+~b)*~(~b*c))", 116)
# test("~((a+b)*~(b*~c))", 226)
# test("~((a+b)*~(b*c))", 209)
# test("~((~b+~c)*~(~a*~c))", 177)
# test("~((~b+c)*~(~b*c))", 6)
# test("~((b+~c)*~(~b*~c))", 12)
# test("~((b+c)*~(~a*c))", 216)
# test("~((~b+~c)*~(a*~c))", 27)
# test("~((~b+c)*~(a*~c))", 42)
# test("~((b+~c)*~(a*c))", 69)
# test("~((b+c)*~(a*c))", 141)
# test("~((~a+~c)*~(~b*~c))", 141)
# test("~((~a+c)*~(~b*c))", 78)
# test("~((~a+~c)*~(b*~c))", 39)
# test("~((~a+c)*~(b*c))", 27)
# test("~((a+~c)*~(~b*~c))", 216)
# test("~((a+c)*~(~b*c))", 228)
# test("~a*b+c", 117)

def test(function):
    print()
    print("function: ", function)
    
    print()
    pdnf = parser.make_pdnf(parser.build_truth_table(parser.resolve_inversions(function)))
    print("pdnf", pdnf)
    minimizer.to_end_form(pdnf)
    
    pcnf = parser.make_pcnf(parser.build_truth_table(parser.resolve_inversions(function)))
    print()
    print("pcnf: ", pcnf)
    minimizer.to_end_form(pcnf)

# test("~((a+b)*~(b*~c))") 

# test("~((~a+~b)*~(~a*~c))")
# test("~((~a+~b)*~(~a*c))")
# test("~((~a+b)*~(~a*~c))")
# test("~((~a+b)*~(~a*c))")
# test("~((a+~b)*~(a*~c))")
# test("~((a+~b)*~(a*c))")
# test("~((a+b)*~(a*~c))")
# test("~((a+b)*~(a*c))")
# test("~((~a+~b)*~(~b*~c))")
# test("~((~a+~b)*~(~b*c))")
# test("~((~a+b)*~(b*~c))")
# test("~((~a+b)*~(b*c))")
# test("~((a+~b)*~(~b*~c))")
# test("~((a+~b)*~(~b*c))")
# test("~((a+b)*~(b*~c))")
# test("~((a+b)*~(b*c))")
# test("~((~b+~c)*~(~a*~c))")
# test("~((~b+c)*~(~b*c))")
# test("~((b+~c)*~(~b*~c))")
# test("~((b+c)*~(~a*c))")
# test("~((~b+~c)*~(a*~c))")
# test("~((~b+c)*~(a*~c))")
# test("~((b+~c)*~(a*c))")
# test("~((b+c)*~(a*c))")
# test("~((~a+~c)*~(~b*~c))")
# test("~((~a+c)*~(~b*c))")
# test("~((~a+~c)*~(b*~c))")
# test("~((~a+c)*~(b*c))")
# test("~((a+~c)*~(~b*~c))")
# test("~((a+c)*~(~b*c))")
# test("~a*b+c")
