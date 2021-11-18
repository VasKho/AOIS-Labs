import minimizer
import parser

print("~((b+c)*~(a*c))")

function = "~((b+c)*~(a*c))"

print(parser.build_truth_table(parser.to_disjunctive_normal_form(function)))

pdnf = parser.make_pdnf(parser.build_truth_table(parser.to_disjunctive_normal_form(function)))

print("PDNF: ", pdnf)

print("Calculation\n")

print("Calculation-table\n", minimizer.minimize_Quine(pdnf))

print("Kmaps\n", minimizer.minimize_KMap(pdnf))
