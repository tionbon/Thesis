import Orange
import os, sys
import datetime
import csv
from collections import defaultdict

path_to_datatables = "/usr/local/lib/python3.5/dist-packages/Orange/datasets/"


def make_rules(orig_data, repaired_files, output, beam_width, min_covered_examples, max_rule_length):
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
	# produce rules from unrepaired data
	classifier_orig = learner_orig(original_data)
	
	print("Setting initial counts")
	# Set initial rule counts
	rule_counts = {}
	og_rulelist = classifier_orig.rule_list
	for id, rule in enumerate(og_rulelist):
		rule.ID = id
		rule_counts[rule.ID] = 0 

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
		learner_repaired.filter = True
		learner_repaired.rule_filter = classifier_orig.rule_list

		# Produce rules for Repaired Data
		classifier_repaired = learner_repaired(repaired_data)

		for rule in classifier_repaired.rule_list:
			for og_rule in og_rulelist:
				if rule.equals(og_rule):
					rule.ID = og_rule.ID
			rule_counts[rule.ID] = i
		print("Rules produced for {} and rule scores updated".format(repaired_file))

		# Save rules from this iteration
		rules_produced[i] = classifier_repaired.rule_list
		i += 1

	
		#Create rules file from repaired data
		#with open("Rules/"+output+"-repaired", 'a+') as rules:
		#	rules.write("******** {} ********\n".format(repaired_file))
		#	rules.write("Rules\n")
		#	for rule in classifier_repaired.rule_list:
		#		rules.write("{}\n".format(rule))
		#	rules.write("\n\n")
		#	rules.close()
	print("Writing rules to file")
	# write rules to file
	with open("Rules/"+output+"-repaired", 'a+') as rules:
		# Create rules file from repaired data
		for j, repaired_file in enumerate(repaired_files):
			rules.write("******** {} ********\n".format(repaired_file))
			rules.write("Rules\tScore\n")
			for rule in rules_produced[j]:
				rules.write("{}\t{}\n".format(rule, [rule_counts[rule.ID]]))
			rules.write("\n\n")
	rules.close()	

	
	# Update log file
	t = datetime.datetime.now()
	log = open("log.txt", 'a')
	log.write("{}-{}-{} {}:{}:{}\n".format(t.year,t.month,t.day,t.hour,t.minute,t.second))
	log.write("Data: {}\tBeam Width: {}\tmin_covered_examples: {}\t max_rule_length: {}\n".format(orig_data, beam_width, min_covered_examples, max_rule_length))
	log.close()

	# Open files
	os.system('xdg-open Rules/'+output+"-repaired")


if __name__ == "__main__":
	if len(sys.argv) != 6:
		print("make_rules.py: <original data> <repaired data> <beam width> <minimum covered examples> <maximum rule length>\n")

		if len(sys.argv) > 1 and sys.argv[1] == '-dir':
			for dataset in os.listdir(path_to_datatables):
				print(dataset)

		sys.exit()

	orig_data = sys.argv[1]
	repaired_data = sys.argv[2]
	beam_width = int(sys.argv[3])
	min_covered_examples = int(sys.argv[4])
	max_rule_length = int(sys.argv[5])

	repaired_files = sorted([repaired_data+file for file in os.listdir(repaired_data)])

	# Add timestamp identifier to output file
	t = datetime.datetime.now()
	output = "{}-{}.{}H{}".format(t.month,t.day,t.hour,t.minute)

	make_rules(orig_data, repaired_files, output, beam_width, min_covered_examples, max_rule_length)
