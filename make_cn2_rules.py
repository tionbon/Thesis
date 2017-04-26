import Orange
import os, sys
import datetime
import csv
import ast
from collections import defaultdict
import itertools 
import pandas as pd
import _pickle
import random


path_to_datatables = "/usr/local/lib/python3.5/dist-packages/Orange/datasets/"


def make_cn2_rules(orig_data, merged, output, beam_width, min_covered_examples, max_rule_length, scores, tag, k=None):
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
		# set the maximum number of selectors (conditions) found rules may combine
	learner_orig.rule_finder.general_validator.max_rule_length = max_rule_length
	# Calculate discrimination score
	learner_orig.rule_finder.scores = scores

	# find auditied rule complements
	learner_orig.rule_finder.search_strategy.complement = False

	# produce rules from unrepaired data
	classifier_orig = learner_orig(original_data)

	#test_data = Orange.data.Table.from_file(merged)
	#res = Orange.evaluation.TestOnTestData(original_data, test_data, [learner_orig])
	#print("Accuracy:", Orange.evaluation.scoring.CA(res))
	#print("AUC:", Orange.evaluation.scoring.AUC(res))

	#print("storing rules")
	#with open(r"{}.pickle".format(output), "wb") as output_file:     
	#	_pickle.dump(classifier_orig.rule_list, output_file)

	dataset = str(merged)
	print("Writing rules to file")
	# write rules to file
	with open("Rules/"+output+".csv", 'w') as csvfile:
		rules = csv.writer(csvfile)
		# Create rules file from repaired data
		rules.writerow(["Label","Rules","Quality","Score"])
		for rule_num, rule in enumerate(classifier_orig.rule_list):
			rules.writerow([rule_num, str(rule), rule.quality, rule.score])
			if False:
				if rule.selectors:
					print("Expanding rule {}".format(rule_num))
					complement_rules = find_and_evaluate_complement_rules(rule, dataset, scores, tag, k)
					print("Writing expanded rules for rule {}".format(rule_num))
					for cr in complement_rules:
						rules.writerow([rule_num, cr[0], cr[1], cr[2]])
	# Open files
	os.system('gedit Rules/'+output+".csv")


def learn_and_test(orig_data, beam_width, min_covered_examples, max_rule_length):
	# split into test and train
	orig = csv.reader(open(orig_data, 'r'), delimiter='\t')
	header = next(orig)
	feature_domains = next(orig)
	meta_data = next(orig)

	print(header, feature_domains, meta_data)
	orig_copy = [row for row in orig]
	print(orig_copy[0])

	train_file = "Data/train.tab"
	test_file = "Data/test.tab"

	train = open(train_file, 'w')
	test = open(test_file, 'w')
	train.write('\t'.join(header)+'\n')
	train.write('\t'.join(feature_domains)+'\n')
	train.write('\t'.join(meta_data)+'\n')
	test.write('\t'.join(header)+'\n')
	test.write('\t'.join(feature_domains)+'\n')
	test.write('\t'.join(meta_data)+'\n')

	random.shuffle(orig_copy)
	train_split = len(orig_copy)*0.8

	for i, row in enumerate(orig_copy):
		if i < train_split:
			train.write("\t".join(row)+"\n")
		else:
			test.write("\t".join(row)+"\n")

	train.close()
	test.close()


	print("Learning rules from unrepaired file")
	# format data for classification
	training_data = Orange.data.Table.from_file(train_file)
	# set the learner
	learner = Orange.classification.rules_backup.CN2Learner()
	# set the number of solution steams considered at one time
	learner.rule_finder.search_algorithm.beam_width = beam_width
	# continuous value space is constrained to reduce computation time
	learner.rule_finder.search_strategy.constrain_continuous = True
	# set the minimum number of examples a found rule must cover to be considered
	learner.rule_finder.general_validator.min_covered_examples = min_covered_examples

	# find auditied rule complements
	learner.rule_finder.search_strategy.complement = False

	# produce rules from unrepaired data
	classifier = learner(training_data)	

	test_data = Orange.data.Table.from_file(test_file)
	res = Orange.evaluation.TestOnTestData(training_data, test_data, [learner])
	print("Accuracy:", Orange.evaluation.scoring.CA(res))
	print("AUC:", Orange.evaluation.scoring.AUC(res))

"""
-find obscure column name, find all combination of attributes, find all values for each combo, calculate laplace and discrimination score, write rules
"""
def expand_and_write_rules(pickle_rule_list, merged, test_set, output, summary, tag, start = 0, k=None):
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
			for rule_num, rule in enumerate(rule_list):
				if rule_num < start:
					continue    
				rules.writerow([rule_num, str(rule), rule.quality, rule.score])
				if rule.selectors:
					print("Expanding rule {}".format(rule_num))
					complement_rules = find_and_evaluate_complement_rules(rule, dataset, test_set, scores, tag, k)
					print("Writing expanded rules for rule {}".format(rule_num))
					for cr in complement_rules:
						rules.writerow([rule_num, cr[0], cr[1], cr[2]])
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
	group_values = []
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
		group_values.append((selector[0],rule_structure, op, val))

	rule_query = rule_query[:-3]
	full_rule_query = full_rule_query[:-3]
	return rule_query, full_rule_query, parsed_outcome, group_values

def find_and_evaluate_complement_rules(rule, dataset, test_set, scores, tag, k):
	# gather the features of the rule and their respective obscured feature names
	attributes = rule.domain.attributes
	original = [attributes[s.column].name for s in rule.selectors]
	rule_form = sorted(original)
	# parse rule into format for querying
	rule_query, full_rule_query, parsed_outcome, group_values = parse_rule(rule)
	
	print("\tQuerying Dataset based on rule")	
	# find the section of data covered by the original rule
	df = pd.read_csv(dataset)
	df.columns = df.columns.str.replace('-', '_')
	df_test = pd.read_csv(test_set)
	df_test.columns = df.columns.str.replace('-', '_')
	covered_data = df.query(full_rule_query)


	print("\tGathering expanded selectors")
	# find values for each feature
	selectors_per_feature = []
	#print(obscured_and_original_cols)
	for group_value in group_values:
		col = group_value[0]
		specific_covered_data = covered_data.query(group_value[1])
		col_val_combinations = [(col, group_value[3])] + [(col+tag, val) for val in specific_covered_data[col].unique()]
		op = group_value[2]
		selectors = []
		for comb in col_val_combinations:
			col_name = comb[0]
			unique_val = comb[1]
			try:
				int(unique_val)
				query = "{} {} {}".format(col_name, op, unique_val)
			except:
				try:
					float(unique_val)
					query = "{} {} {}".format(col_name, op, unique_val)
				except:
					query = "{} {} '{}'".format(col_name, op, unique_val)
			selectors.append((col, query, op))
		selectors_per_feature.append(selectors)

	print("\tCombining selectors into new rules")
	# find all valid combinations of selectors
	valid_combinations = [comb for comb in itertools.product(*selectors_per_feature)]

	print("\tEvaluating new rules")
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
		Nclass = len(df_test.query(comb_query_with_outcome))
		Ntotal = len(df_test.query(comb_query))
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

	#make_cn2_rules(orig_data, repaired_data, output, beam_width, min_covered_examples, max_rule_length, scores, tag)
	learn_and_test(orig_data, beam_width, min_covered_examples, max_rule_length)

"""
python3 -c "import make_cn2_rules as foo; foo.expand_and_write_rules('compas_race_j48.pickle', './Data/compas2/race_j48.csv', 'compas_race_j48', './Data/compas2/compas_j48_summary.txt','_norace')"

"""
