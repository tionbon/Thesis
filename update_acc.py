import os, sys
import csv
import pandas as pd 

#["Label","Rules","Quality","Score"]

def modify_acc(rule_list, test_data, output):
	with open(output, 'w') as csvfile:
		mod_rules = csv.writer(csvfile)

		df = pd.read_csv(test_data)
		df.columns = df.columns.str.replace('-','_')
		with open(rule_list, 'r') as csvfile2:
			rules = csv.reader(csvfile2)
			# write header
			mod_rules.writerow(next(rules))

			# find new accuracy
			for i, rule in enumerate(rules):
				if rule[1][3:7] != "TRUE":
					rule_mod = rule[1]
					query, query_with_outcome = parse_rule(rule_mod)

					# calculate new quality
					Nclass = len(df.query(query_with_outcome))
					Ntotal = len(df.query(query))
					k = 2
					laplace = (Nclass + 1)/float(Ntotal + k)
					
					rule[2] = laplace 
					mod_rules.writerow(rule)

def parse_rule(rule):
	antecedent = rule.split(" THEN ")[0][3:]
	outcome = rule.split(" THEN ")[1].strip(" ") 
	parsed_outcome = outcome.split("==")
	try:
		parsed_outcome = outcome.split("==")
		parsed_outcome[1]
	except IndexError:
		parsed_outcome = outcome.split("=")

	conditions = antecedent.split(" AND ")
	rule_query = ""
	for cond in conditions:
		# Split on correct operation
		try:
			parsed_cond = cond.split("==")
			op = "=="
			feature = parsed_cond[0].replace('-','_')
			value = parsed_cond[1]
		except IndexError:
			try:
				parsed_cond = cond.split("!=")
				op = "!="
				feature = parsed_cond[0].replace('-','_')
				value = parsed_cond[1]
			except IndexError:
				try:
					parsed_cond = cond.split(">=")
					op = ">="
					feature = parsed_cond[0].replace('-','_')
					value = parsed_cond[1]
				except IndexError:
					parsed_cond = cond.split("<=")
					op = "<="
					feature = parsed_cond[0].replace('-','_')
					value = parsed_cond[1]

		try:
			val = int(float(value))
			rule_structure = "{} {} {}".format(feature, op, val)
			full_rule_structure = "{} {} {}".format(feature, op, val)
		except:
			val = value
			rule_structure = "{} {} '{}'".format(feature, op, val)
			full_rule_structure = "{} {} '{}'".format(feature, op, val)
		
		rule_query += rule_structure + " & "
	
	rule_query_with_outcome = rule_query + "{} == '{}'".format(parsed_outcome[0], parsed_outcome[1])
	rule_query = rule_query[:-3]
	return rule_query, rule_query_with_outcome

if __name__ == "__main__":
	rule_list = sys.argv[1]
	test_data = sys.argv[2]
	output = sys.argv[3]
	modify_acc(rule_list, test_data, output)
