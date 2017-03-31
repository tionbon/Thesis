import csv

#"Label","Rules","Quality","Score"]

orig_rulelist = sys.argv[1]
expanded = sys.argv[2]
epsilon = sys.argv[3]
output = sys.argv[4]

# Open original rule list for reading
orig_rules = csv.DictReader(open(orig_rulelist, 'r'))
# Open output file for writing simplified rules
simplified_rules = csv.writer(open(output, 'r'))

with open(expanded, 'rb') as f:
    expanded_rules = csv.DictReader(f)

	# write header to simplified rule list
	simplified_rules.writerow(next(orig_rule))

	# Chose rule within epsilon quality of the original rule but has the lowest influence score
	for rule_ID, orig_rule in enumerate(orig_rules):
		# write original rule
		simplified_rules.writerow(orig_rule):
		quality = orig_rule["Quality"]
		orig_influence = orig_rule["Score"]
		rows = [row for row in expanded_rules if (row['Label'] == rule_ID and row['Quality'] + epsilon >= quality)]

		lowest_influence_score = orig_influence
		best_row = []
		for row in rows:
			score = row[3]
			if score < lowest_influence_score:
				best_row = row
		
	

