import Orange
import os, sys
import datetime
import csv
import ast
from collections import defaultdict
from itertools import combinations
import pandas as pd
import seaborn as sns


path_to_datatables = "/usr/local/lib/python3.5/dist-packages/Orange/datasets/"


def make_repaired_rules(orig_data, repaired_files, output, beam_width, min_covered_examples, max_rule_length, scores, tag):
	print("Learning rules from unrepaired file")
	# format data for classification
	original_data = Orange.data.Table.from_file(orig_data)
	# set the learner
	learner_orig = Orange.classification.rules.CN2SDLearner()
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

	# produce rules from unrepaired data
	classifier_orig = learner_orig(original_data)
	
	print("Setting initial counts")
	# Set initial rule counts
	rule_counts = {}
	og_rulelist = classifier_orig.rule_list
	for id, rule in enumerate(og_rulelist):
		rule.ID = id
		rule_counts[rule.ID] = 0 

	print("Writing original rules to file")
	# write rules to file
	with open("Rules/"+output, 'w') as rules:
		# Create rules file from repaired data
		rules.write("******** {} ********\n".format(orig_data))
		rules.write("Rules\tScore\n")
		rl = []
		for rule in classifier_orig.rule_list:
			rl.append((str(rule), rule.score))

		rl.sort(key=lambda x: x[0])
		for rule in rl:
			#rules.write("{}\t{}\n".format(rule, [rule_counts[rule.ID]]))
			rules.write("{}\t{}\n".format(rule[0], rule[1]))
		rules.write("\n\n")
	rules.close()	

	print("How did this do?:", classifier_orig.predict(orig_data))

	# store rules for each interations
	i = 0
	rules_produced = {}
	print("Beginning learning process for repaired files")
	for repaired_file in repaired_files:
		print("Learning rules for {}".format(repaired_file))
		# format data for classification
		repaired_data = Orange.data.Table.from_file(repaired_file)
		# set the learner
		learner_repaired = Orange.classification.rules.CN2SDLearner()
		# set the number of solution steams considered at one time
		learner_repaired.rule_finder.search_algorithm.beam_width = beam_width
		# continuous value space is constrained to reduce computation time
		learner_repaired.rule_finder.search_strategy.constrain_continuous = True
		# set the minimum number of examples a found rule must cover to be considered
		learner_repaired.rule_finder.general_validator.min_covered_examples = min_covered_examples
		# set the maximum number of selectors (conditions) found rules may combine
		learner_repaired.rule_finder.general_validator.max_rule_length = max_rule_length

		# filter rule list for repaired data
		learner_repaired.filter = False
		learner_repaired.rule_filter = classifier_orig.rule_list
		learner_repaired.tag = tag

		learner_repaired.rule_finder.weighted_rules = False
		learner_repaired.rule_finder.scores = scores

		# Produce rules for Repaired Data
		classifier_repaired = learner_repaired(repaired_data)

		if False:
			for rule in classifier_repaired.rule_list:
				for og_rule in og_rulelist:
					#if rule.equals(og_rule):
					#	rule.ID = og_rule.ID
					if rule.equals(og_rule):
						rule.ID = og_rule.ID
				rule_counts[rule.ID] = i
			print("Rules produced for {} and rule scores updated".format(repaired_file))

		# Save rules from this iteration
		rules_produced[i] = classifier_repaired.rule_list
		i += 1

	print("Writing rules to file")
	# write rules to file
	with open("Rules/"+output, 'a+') as rules:
		# Create rules file from repaired data
		for j, repaired_file in enumerate(repaired_files):
			rules.write("******** {} ********\n".format(repaired_file))
			rules.write("Rules\tScore\n")
			rl = []
			for rule in rules_produced[j]:
				rl.append((str(rule), rule.score))
			rl.sort(key=lambda x: x[0])
			for rule in rl:
				#rules.write("{}\t{}\n".format(rule, [rule_counts[rule.ID]]))
				rules.write("{}\t{}\n".format(rule[0], rule[1]))

			rules.write("\n\n")
	rules.close()	

	# Update log file
	t = datetime.datetime.now()
	log = open("log.txt", 'a')
	log.write("{}-{}-{} {}:{}:{}\n".format(t.year,t.month,t.day,t.hour,t.minute,t.second))
	log.write("Data: {}\tBeam Width: {}\tmin_covered_examples: {}\t max_rule_length: {}\n".format(orig_data, beam_width, min_covered_examples, max_rule_length))
	log.close()

	# Open files
	os.system('xdg-open Rules/'+output)

def make_repaired_rules_cn2(orig_data, repaired_files, output, beam_width, min_covered_examples, max_rule_length, scores, tag, filter_switch):
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

	# produce rules from unrepaired data
	classifier_orig = learner_orig(original_data)
	
	print("Setting initial counts")
	# Set initial rule counts
	rule_counts = {}
	og_rulelist = classifier_orig.rule_list
	for id, rule in enumerate(og_rulelist):
		rule.ID = id
		rule_counts[rule.ID] = 0 

	print("Writing original rules to file")
	# write rules to file
	with open("Rules/"+output+"-cn2", 'w') as rules:
		# Create rules file from repaired data
		rules.write("******** {} ********\n".format(orig_data))
		rules.write("Rules\tScore\n")
		rl = []
		for rule in classifier_orig.rule_list:
			rl.append((str(rule), rule.score))

		#rl.sort(key=lambda x: x[0])
		for rule in rl:
			#rules.write("{}\t{}\n".format(rule, [rule_counts[rule.ID]]))
			rules.write("{}\t{}\n".format(rule[0], rule[1]))
		rules.write("\n\n")
	rules.close()	

	# store rules for each interations
	i = 0
	rules_produced = {}
	print("Beginning learning process for repaired files")
	for repaired_file in repaired_files:
		print("Learning rules for {}".format(repaired_file))
		# format data for classification
		repaired_data = Orange.data.Table.from_file(repaired_file)
		# set the learner
		learner_repaired = Orange.classification.rules.CN2Learner()
		# set the number of solution steams considered at one time
		learner_repaired.rule_finder.search_algorithm.beam_width = beam_width
		# continuous value space is constrained to reduce computation time
		learner_repaired.rule_finder.search_strategy.constrain_continuous = True
		# set the minimum number of examples a found rule must cover to be considered
		learner_repaired.rule_finder.general_validator.min_covered_examples = min_covered_examples
		# set the maximum number of selectors (conditions) found rules may combine
		learner_repaired.rule_finder.general_validator.max_rule_length = max_rule_length

		# filter rule list for repaired data
		learner_repaired.filter = filter_switch
		learner_repaired.rule_filter = classifier_orig.rule_list
		learner_repaired.tag = tag

		learner_repaired.rule_finder.weighted_rules = filter_switch
		if filter_switch:
			learner_repaired.rule_finder.epsilon = 0.05
		learner_repaired.rule_finder.scores = scores

		# Produce rules for Repaired Data
		classifier_repaired = learner_repaired(repaired_data)

		if False:
			for rule in classifier_repaired.rule_list:
				for og_rule in og_rulelist:
					#if rule.equals(og_rule):
					#	rule.ID = og_rule.ID
					if rule.equals(og_rule):
						rule.ID = og_rule.ID
				rule_counts[rule.ID] = i
			print("Rules produced for {} and rule scores updated".format(repaired_file))

		# Save rules from this iteration
		rules_produced[i] = classifier_repaired.rule_list
		i += 1

	print("Writing rules to file")
	# write rules to file
	with open("Rules/"+output+"-cn2", 'a+') as rules:
		# Create rules file from repaired data
		for j, repaired_file in enumerate(repaired_files):
			rules.write("******** {} ********\n".format(repaired_file))
			rules.write("Rules\tScore\n")
			rl = []
			for rule in rules_produced[j]:
				rl.append((str(rule), rule.score))
			rl.sort(key=lambda x: x[0])
			for rule in rl:
				#rules.write("{}\t{}\n".format(rule, [rule_counts[rule.ID]]))
				rules.write("{}\t{}\n".format(rule[0], rule[1]))

			rules.write("\n\n")
	rules.close()	

	# Update log file
	t = datetime.datetime.now()
	log = open("log.txt", 'a')
	log.write("{}-{}-{} {}:{}:{}\n".format(t.year,t.month,t.day,t.hour,t.minute,t.second))
	log.write("Data: {}\tBeam Width: {}\tmin_covered_examples: {}\t max_rule_length: {}\n".format(orig_data, beam_width, min_covered_examples, max_rule_length))
	log.close()

	# Open files
	os.system('xdg-open Rules/'+output+"-cn2")

def cn2_complements(orig_data, output, beam_width, min_covered_examples, max_rule_length, scores, tag, filter_switch):
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


	print("Writing rules to file")
	# write rules to file
	with open("Rules/"+output+"-cn2", 'w') as rules:
		# Create rules file from repaired data
		rules.write("******** {} ********\n".format(orig_data))
		rules.write("Label\tRules\tQuality\tScore\n")
		for rule in classifier_orig.rule_list:
			rules.write("{}\t{}\t{}\t{}\n".format("**", str(rule), rule.quality, rule.score))
			#or complement_rule in rule.complement_rules:
				#rules.write("{}\t{}\t{}\t{}\n".format("**", str(complement_rule), complement_rule.quality, complement_rule.score))	
	
	rules.close()	

	# Update log file
	t = datetime.datetime.now()
	log = open("log.txt", 'a')
	log.write("{}-{}-{} {}:{}:{}\n".format(t.year,t.month,t.day,t.hour,t.minute,t.second))
	log.write("Data: {}\tBeam Width: {}\tmin_covered_examples: {}\t max_rule_length: {}\n".format(orig_data, beam_width, min_covered_examples, max_rule_length))
	log.close()

	# Open files
	os.system('xdg-open Rules/'+output+"-cn2")
"""
-find obscure column name, find all combination of attributes, find all values for each combo, calculate laplace and discrimination score, write rules
"""
def parse_rule(rule):
	srule = str(rule)
	antecedent = srule.split(" THEN ")[0][3:]
	consequent = srule.split(" THEN ")[1]
	parsed_outcome = consequent.split("==")
	selectors = antecedent.split(" AND ")
	parsed_selectors = [s.split("==") for s in selectors]
	parsed_rule = ""
	group_values = {}
	for ps in parsed_selectors:
		rule_stucture = "{} == '{}'".format(s[0],s[1])
		parsed_rule += rule_structure + " & "
		group_values[ps] = rule_structure
	parsed_rule += "{} == '{}'".format(parsed_outcome[0], parsed_outcome[1])
	return parsed_rule, group_values


def find complement_groups(rule, dataset, tag):
	original = [attributes[s.column].name for s in rule.selectors]
	obscured = original.extend([orig+tag for orig in original])
	complements = [",".join(map(str, comb)) for comb in combinations(obscured, len(original))]
	parsed_rule = parse_rule(rule)
	data = pd.read_csv(dataset)
	relevant_data = Data.query(parsed_rule)
	return complements, relevant_data

"""
A and B
not A.. and B
not A.. and not B...
A and not B...
"""
def find_and_evaluate_complement_rules(complement_groups,relevant_data,outcome)
	df = relevant_data
	size = len(Data) 
	grp_values = {}
	for grp in complement_groups:
		grp_rules = []
		for col in group:
			unique_vals = df.col.unique()
			grp_rules




def make_rules(file, output, beam_width, min_covered_examples, max_rule_length):
	print("Learning rules from file")
	# format data for classification
	data = Orange.data.Table.from_file(file)
	# set the learner
	learner = Orange.classification.rules.CN2SDLearner()
	# set the number of solution steams considered at one time
	learner.rule_finder.search_algorithm.beam_width = beam_width
	# continuous value space is constrained to reduce computation time
	learner.rule_finder.search_strategy.constrain_continuous = True
	# set the minimum number of examples a found rule must cover to be considered
	learner.rule_finder.general_validator.min_covered_examples = min_covered_examples
	# set the maximum number of selectors (conditions) found rules may combine
	learner.rule_finder.general_validator.max_rule_length = max_rule_length
	# produce rules from unrepaired data
	classifier = learner(data)

	print("Writing rules to file")
	# write rules to file
	with open("Rules/"+output, 'a+') as rules:
		rules.write("******** {} ********\n".format(file))
		rules.write("Rules\n")
		# Create rules file from repaired data
		for rule in classifier.rule_list:
			rules.write("{}\n".format(rule))
	rules.close()	

	# Update log file
	t = datetime.datetime.now()
	log = open("log.txt", 'a')
	log.write("{}-{}-{} {}:{}:{}\n".format(t.year,t.month,t.day,t.hour,t.minute,t.second))
	log.write("Data: {}\tBeam Width: {}\tmin_covered_examples: {}\t max_rule_length: {}\n".format(data, beam_width, min_covered_examples, max_rule_length))
	log.close()

	# Open files
	os.system('xdg-open Rules/'+output)


if __name__ == "__main__":
	if len(sys.argv) == 1:
		print("make_rules.py: <original data> <repaired data> <output> <beam width> <minimum covered examples> <maximum rule length> <summary file> <filter: T or F?>\n")

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
		scores[element[0]+tag] = 0

	if os.path.isdir(repaired_data) == True:
		repaired_files = sorted([repaired_data+"/"+file for file in os.listdir(repaired_data)])
	else:
		repaired_files = [repaired_data]

	filter_switch = True if sys.argv[9] == "True" else False
	# Add timestamp identifier to output file
	t = datetime.datetime.now()
	#output = "{}-{}.{}H{}".format(t.month,t.day,t.hour,t.minute)
	#make_repaired_rules_cn2(orig_data, repaired_files, output, beam_width, min_covered_examples, max_rule_length, scores, tag, filter_switch)
	cn2_complements(orig_data, output, beam_width, min_covered_examples, max_rule_length, scores, tag, filter_switch)
"""
Constant_Feature.summary  Feature_C_(-i).summary
Constant_Feature.tab      Feature_C_(-i).tab
Feature_A_(i).summary     original.tab
Feature_A_(i).tab         Random_Feature.summary
Feature_B_(2i).summary    Random_Feature.tab
Feature_B_(2i).tab
"""