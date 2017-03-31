import Orange
import os, sys
import datetime
import csv
import ast
from collections import defaultdict
from itertools import combinations
import pandas as pd
import _pickle


path_to_datatables = "/usr/local/lib/python3.5/dist-packages/Orange/datasets/"


def make_cn2_rules(orig_data, merged, output, beam_width, min_covered_examples, max_rule_length, scores, tag):
	print("Learning rules from unrepaired file")
	# format data for classification
	original_data = Orange.data.Table.from_file(orig_data)
	# set the learner
	learner_orig = Orange.classification.rules.CN2Learner()
	# set the number of solution steams considered at one time
	learner_orig.rule_finder.search_algorithm.beam_width = beam_width
	# continuous value space is constrained to reduce computation time
	learner_orig.rule_finder.search_strategy.constrain_continuous = True
	# set the minimum number of examples a found rule must cover to be considered
	learner_orig.rule_finder.general_validator.min_covered_examples = min_covered_examples
	# Calculate discrimination score
	learner_orig.rule_finder.scores = scores

	# find auditied rule complements
	learner_orig.rule_finder.search_strategy.complement = False

	# produce rules from unrepaired data
	classifier_orig = learner_orig(original_data)

	test_data = Orange.data.Table.from_file(merged)
	res = Orange.evaluation.TestOnTestData(original_data, test_data, [learner_orig])
	print("Accuracy:", Orange.evaluation.scoring.CA(res))
	print("AUC:", Orange.evaluation.scoring.AUC(res))

	print("storing rules")
	with open(r"{}.pickle".format(output), "wb") as output_file:     
		_pickle.dump(classifier_orig.rule_list, output_file)

#	dataset = str(merged)
	print("Writing rules to file")
	# write rules to file
	with open("Rules/"+output+".csv", 'w') as csvfile:
		rules = csv.writer(csvfile)
		# Create rules file from repaired data
		rules.writerow(["Label","Rules","Quality","Score"])
		rule_identifier = 0
		for rule_num, rule in enumerate(classifier_orig.rule_list):
			rules.writerow([rule_identifier, str(rule), rule.quality, rule.score])
			if rule.selectors:
				print("Expanding rule {}".format(rule_num))
				complement_rules = find_and_evaluate_complement_rules(rule, dataset, scores, tag)
				print("Writing expanded rules for rule {}".format(rule_num))
				for cr in complement_rules:
					rules.writerow([rule_identifier, cr[0], cr[1], cr[2]])
			rule_identifier += 1
	# Open files
	os.system('gedit Rules/'+output+".csv")

"""
-find obscure column name, find all combination of attributes, find all values for each combo, calculate laplace and discrimination score, write rules
"""
def expand_and_write_rules(pickle_rule_list, merged, output, summary, tag, start = 0, k=None):
	f = open(summary, 'r')
	scores_data = ast.literal_eval(f.readline())
	scores = {}
	for element in scores_data:
		scores[element[0]] = element[1]
		scores[element[0]+tag] = 0.0

	with open(r"{}".format(pickle_rule_list), "rb") as input_file:
		rule_list = _pickle.load(input_file)
		dataset = str(merged)
		print("Writing rules to file")
		# write rules to file
		with open("Rules/"+output+".csv", 'w') as csvfile:
			rules = csv.writer(csvfile)
			# Create rules file from repaired data
			rules.writerow(["Label","Rules","Quality","Score"])
			rule_identifier = 0
			for rule_num, rule in enumerate(rule_list):
				if rule_num < start:
					continue    
				rules.writerow([rule_identifier, str(rule), rule.quality, rule.score])
				if rule.selectors:
					print("Expanding rule {}".format(rule_num))
					complement_rules = find_and_evaluate_complement_rules(rule, dataset, scores, tag, k)
					print("Writing expanded rules for rule {}".format(rule_num))
					for cr in complement_rules:
						rules.writerow([rule_identifier, cr[0], cr[1], cr[2]])
				rule_identifier += 1	
		# Open files
		os.system('gedit Rules/'+output+".csv")

def parse_rule(rule):
	# separate the string representation of the rule 
	# 	into its antecedent and consequent parts
	attributes = rule.domain.attributes
	class_var = rule.domain.class_var
	srule = str(rule)
	antecedent = [(attributes[s.column].name, s.op, 
                                 (str(attributes[s.column].values[int(s.value)])
                                  if attributes[s.column].is_discrete
                                  else str(s.value))) for s in rule.selectors]
	parsed_outcome = [class_var.name, class_var.values[rule.prediction]]
	# format the rule as a query and store the query version per feature
	rule_query = ""
	full_rule_query = ""
	group_values = {}
	for selector in antecedent:
		op = selector[1]
		query_op = "==" if (op==(">=") or op=="<=") else selector[1]
		val = selector[2]
		rule_structure = ""
		full_rule_structure = ""
		try:
			val = int(float(selector[2]))
			rule_structure = "{} {} {}".format(selector[0], query_op, val)
			full_rule_structure = "{} {} {}".format(selector[0], op, val)
		except:
			rule_structure = "{} {} '{}'".format(selector[0], query_op, val)
			full_rule_structure = "{} {} '{}'".format(selector[0], op, val)
		rule_query += rule_structure + " & "
		full_rule_query += full_rule_structure + " & "
		group_values[selector[0]] = (rule_structure, op, val)

	rule_query = rule_query[:-3]
	full_rule_query = full_rule_query[:-3]
	return rule_query, full_rule_query, parsed_outcome, group_values

def find_and_evaluate_complement_rules(rule, dataset, scores, tag, k):
	# gather the features of the rule and their respective obscured feature names
	attributes = rule.domain.attributes
	original = [attributes[s.column].name for s in rule.selectors]
	rule_form = sorted(original)
	obscured_and_original_cols = original + [orig+tag for orig in original]
	# parse rule into format for querying
	rule_query, full_rule_query, parsed_outcome, group_values = parse_rule(rule)
	
	# find the section of data covered by the original rule
	df = pd.read_csv(dataset)
	df.columns = df.columns.str.replace('-', '_')
	covered_data = df.query(rule_query)
	if len(covered_data) == 0:
		covered_data = df.query(full_rule_query)

	# find values for each feature
	selectors = []
	#print(obscured_and_original_cols)
	for col in obscured_and_original_cols:
		split_col = col.split(tag)[0]
		specific_covered_data = covered_data.query(group_values[split_col][0])
		unique_vals = specific_covered_data[col].unique() if col not in original else [group_values[col][2]]
		op = group_values[split_col][1]
		#print(col, unique_vals)
		for unique_val in unique_vals:
			try:
				int(unique_val)
				query = "{} {} {}".format(col, op, unique_val)
			except:
				try:
					float(unique_val)
					query = "{} {} {}".format(col, op, unique_val)
				except:
					query = "{} {} '{}'".format(col, op, unique_val)
			selectors.append((col, query, op))

	# find all combinations of selectors
	# [((A,query), (B,query), (C,query)), ()]
	all_combinations = [eval(str(comb)) for comb in combinations(selectors, len(original))]
	valid_combinations = []
	valid_feature_sets = []
	for comb in all_combinations:
		all_features = [selector[0] for selector in comb]
		# filter out rules with both col and col-tag
		valid = True 
		for feature in all_features:
			if feature+tag in all_features:
				valid = False
		feature_form = [selector[0].split(tag)[0] for selector in comb]
		features = sorted([selector[1] for selector in comb])
		# filter out rules with duplicate selectors, have been counted already, and do not have same form as original
		if (sorted(feature_form) == rule_form and 
			len(set(features)) == len(features) and
			features not in valid_feature_sets and 
			valid == True):
			valid_combinations.append(comb)
			valid_feature_sets.append(features)


	# lapace = (N(covered with predicted class) + 1)/(N(total covered) + k)
	complement_rules = []
	sorted_complement_rules = []
	for comb in valid_combinations:
		comb_query = ""
		for selector in comb:
			comb_query += selector[1] + " & "
		comb_query_with_outcome = comb_query + "{} == '{}'".format(parsed_outcome[0], parsed_outcome[1])
		comb_query = comb_query[:-3] 

		# calculate quality
		Nclass = len(df.query(comb_query_with_outcome))
		Ntotal = len(df.query(comb_query))
		k = k if k is not None else len(df[parsed_outcome[0]].unique())
		laplace = (Nclass + 1)/float(Ntotal + k)

		# calculate discrimination
		discrimination_score = sum([float(scores[s[0]]) for s in comb])

		# format rule for printing:
		formatted_rule_conditions = []
		for selector in comb:	
			op = selector[2]
			elements = selector[1].split(" {} ".format(op))
			formatted_selector = ""
			if len(elements) > 1:
				value = elements[1]
				try:
					int(value)
				except:
					try:
						float(value)
					except:
						value = value[1:-1]
				formatted_selector = "{}{}{}".format(elements[0], op, value)
			else: 
				manual_split = selector[1].split(" ")
				feature = manual_split[0]
				op = manual_split[1]
				value = manual_split[2]
				try:
					int(value)
				except:
					try:
						float(value)
					except:
						value = value[1:-1]
				formatted_selector = "{}{}{}".format(feature, op, value)
			formatted_rule_conditions.append(formatted_selector)

		formatted_rule_antecedent = " AND ".join(formatted_rule_conditions)
		formatted_outcome = "{}=={}".format(parsed_outcome[0], parsed_outcome[1])
		formatted_rule = "IF " + formatted_rule_antecedent + " THEN " + formatted_outcome
		complement_rules.append((formatted_rule, laplace, discrimination_score))

		sorted_complement_rules = sorted(complement_rules, reverse=True, key=lambda x: x[1])

	return sorted_complement_rules





if __name__ == "__main__":
	if len(sys.argv) == 1:
		print("make_rules.py: <original data> <repaired data> <output> <beam width> <minimum covered examples> <maximum rule length> <summary file> \n")

		if len(sys.argv) > 1 and sys.argv[1] == '-dir':
			for dataset in os.listdir(path_to_datatables):
				print(dataset)

		sys.exit()
	
	orig_data = sys.argv[1]
	repaired_data = sys.argv[2]
	output = sys.argv[3]
	beam_width = int(sys.argv[4])
	min_covered_examples = int(sys.argv[5])
	max_rule_length = int(sys.argv[6])

	# convert score
	summary = sys.argv[7]
	tag = sys.argv[8]
	f = open(summary, 'r')
	scores_data = ast.literal_eval(f.readline())
	scores = {}
	for element in scores_data:
		scores[element[0]] = element[1]
		scores[element[0]+tag] = 0.0

	make_cn2_rules(orig_data, repaired_data, output, beam_width, min_covered_examples, max_rule_length, scores, tag)

"""
python3 -c "import make_cn2_rules as foo; foo.expand_and_write_rules('compas_race_j48.pickle', './Data/compas2/race_j48.csv', 'compas_race_j48', './Data/compas2/compas_j48_summary.txt','_norace')"

"""
