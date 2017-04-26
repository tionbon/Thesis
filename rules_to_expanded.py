
# coding: utf-8

# In[63]:

"""
Read rules into a dictionary.
"""

import csv
import ast
import os

# maps rule numbers to dictionaries containing feature to (op, value) tuples lists
# 0 -> {"prior_count" -> [(==, 3), (<=, 6)]}
num_to_ruledict = {}

def is_int(string):
    try:
        int(string)
        return True
    except ValueError:
        return False
    
def is_float(string):
    try: 
        float(string)
        return True
    except ValueError:
        return False
    
def convert_ifnum(string):
    if is_int(string):
        return int(string)
    if is_float(string):
        return float(string)
    return string

def get_rules_from_file(filename):
    f = open(filename, "r")
    reader = csv.DictReader(f)
    for row in reader:
        num = int(row["Label"])
        num_to_ruledict[num] = {}
        
        rules = row["Rules"]
        if_rules, then_rule = rules.split(" THEN ")
        out_var, out_val = then_rule.split("=")
        out_val = out_val[:-1]  # remove trailing space
        num_to_ruledict[num][out_var] = [("=", out_val)]

        rules_list = if_rules.split(" AND ")
        rules_list[0] = rules_list[0][3:]  # remove "IF " on the front of the first rule
        
        for rule in rules_list:
            if '<=' in rule:
                op = '<='
            elif '==' in rule:
                op = '=='
            elif '>=' in rule:
                op = '>='
            elif '!='  in rule:
                op = '!='
            elif 'TRUE' in rule:
                print "Warning: last rule, ignoring rule: " + rule
                continue
            else:
                print "Warning: unrecognized operation " + rule
                
            rule_var, rule_val = rule.split(op)
            rule_val = convert_ifnum(rule_val)
                
            if rule_var in num_to_ruledict[num]:
                num_to_ruledict[num][rule_var].append((op, rule_val))
            else:
                num_to_ruledict[num][rule_var] = [(op, rule_val)]
    return num_to_ruledict

            

# In[64]:

"""
Get the possible values that original features are mapped to in the obscured version.
"""

def get_orig_to_obscured_map(orig_csv, obscured_csv):
    orig_f = open(orig_csv, "r")
    obscured_f = open(obscured_csv, "r")
    
    orig_reader = csv.DictReader(orig_f)
    obscured_reader = csv.DictReader(obscured_f)
    
    # dict mapping from attribute name to orig value to list of obscured values
    # "prior_count" -> { 3.0 -> [1.0, 2.0]}
    orig_to_obscured = {}
    
    # maps row num to the original value at an attribute
    # 2 -> {"prior_count" -> 1.0}
    rownum_to_origval = {}
    
    for i, rowdict in enumerate(orig_reader):
        rownum_to_origval[i] = {}
        for attr in rowdict:
	    attr_val = convert_ifnum(rowdict[attr])
            rownum_to_origval[i][attr] = attr_val
            
            if attr not in orig_to_obscured:
                orig_to_obscured[attr] = {}
            if attr_val not in orig_to_obscured[attr]:
                orig_to_obscured[attr][attr_val] = []

    orig_f.close()
    for i, rowdict in enumerate(obscured_reader):
        for attr in rowdict:
            attr_val = convert_ifnum(rowdict[attr])
     
            if attr not in orig_to_obscured:
                print "Warning: can't find original attribute to match this obscured attribte:" + attr
            orig_val = rownum_to_origval[i][attr]
            
            if attr_val not in orig_to_obscured[attr][orig_val]:
                orig_to_obscured[attr][orig_val].append(attr_val)
    return orig_to_obscured



# In[125]:

"""
Take a single rule and expand it to all the possible versions based on the obscured values.
"""

import itertools

def get_expanded_from_rule(ruledict, orig_to_obscured, outcome_attr, obscured_tag):
    """
    ruledict maps attrnames to a list of op, value tuples assocaited with that attr name in the rule:
    "prior_count" -> [(==, 3), (<=, 6)]
    
    orig_to_obscured is a dict mapping from attribute name to orig value to list of obscured values
    "prior_count" -> { 3.0 -> [1.0, 2.0]}
    
    returns: a list of obscured ruledicts (with ruledicts in the same form as above)
    """
    orig_rule = flatten_ruledict(ruledict)
    obscured_rules = [orig_rule]
    list_of_possible_clauses = []
    
    for i, (attr, op, val) in enumerate(orig_rule):
        obscured_vals = orig_to_obscured[attr][val]
        possible_clauses = make_list_of_clauses(orig_rule[i], obscured_vals, outcome_attr, obscured_tag)
        list_of_possible_clauses.append(possible_clauses)
        
    product = itertools.product(*list_of_possible_clauses)
    for item in product:
        obscured_rules.append(item)

    return obscured_rules

    
def make_list_of_clauses(orig_clause, vals_list, outcome_attr, obscured_tag):
    clauses = [orig_clause]
    attr, op, orig_val = orig_clause
    if attr != outcome_attr:
        for val in vals_list:
            clauses.append((attr + obscured_tag, op, val))
    return clauses

def copy_rule(rule):
    copy = []
    for attr, op, val in rule:
        copy.append((attr, op, val))
    return copy
    
def flatten_ruledict(ruledict):
    """
    ruledict maps attrnames to a list of op, value tuples assocaited with that attr name in the rule:
    "prior_count" -> [(==, 3), (<=, 6)]
    
    returns a list of (attr, op, val) tuples
    """
    rule_tuples = []
    for attr in ruledict:
        for (op, val) in ruledict[attr]:
            rule_tuples.append((attr, op, val))
    return rule_tuples


# In[126]:

"""
Create a dictionary mapping rule nums to the list of lists (rules) containing clauses (tuples).
"""

def expand_all_rules(num_to_ruledict, orig_to_obscured, outcome_attr, obscured_tag):
    expanded_rules = {}
    for num in num_to_ruledict:
        expanded_rules[num] = get_expanded_from_rule(num_to_ruledict[num], orig_to_obscured, outcome_attr, obscured_tag)
        
    return expanded_rules



# In[132]:

"""
Calculate rule quality based on the test data.
"""

def get_test_data(test_filename):
    f = open(test_filename, "r")
    reader = csv.DictReader(f)   
    data = []
    for row in reader:
        row_dict = {}
        for key in row:
            row_dict[key] = convert_ifnum(row[key])
        data.append(row_dict)       
    return data

def get_test_data_rule_covers(rule, test_data, outcome_attr, include_outcome):
    covered_rules = []
    for row in test_data:
        is_valid = True
        #print row
        for clause in rule:
            #print clause
            attr = clause[0]
            if attr != outcome_attr:
                if not satisfies_clause(clause, row):
                    is_valid = False
            else:
                if include_outcome:
                    if not satisfies_clause(clause, row):
                        is_valid = False
        if is_valid:
            covered_rules.append(row)
            #print "included"
    return covered_rules

def satisfies_clause(clause, row):
    attr, op, val = clause
    row_val = row[attr]
    if op == '<=':
        return row_val <= val
    elif op == '==' or op == '=':
        return row_val == val
    elif op == '>=':
        return row_val >= val
    elif op == '!=':
        return row_val != val
    else:
        print "Warning: unknown op:" + op
        return False
    
def calc_rule_quality(rule, test_data, num_classes, outcome_attr):
    covered = get_test_data_rule_covers(rule, test_data, outcome_attr, False)
    correct = get_test_data_rule_covers(rule, test_data, outcome_attr, True)
    num_covered = len(covered)
    num_correct = len(correct)
    return (num_correct + 1.0) / (num_covered + num_classes)

def get_influence_scores(filename):
    #f = open(filename, "r")
    #influence_dict = {}
    #reader = csv.DictReader(f)
    #for row_dict in reader:
    #    for key in row_dict:
    #        influence_dict[key] = convert_ifnum(row_dict[key])
    #    break  # should only be one row
    #return influence_dict
    f = open(filename, "r")
    scores = ast.literal_eval(f.readline())
    influence_dict = {}
    for element in scores:
        influence_dict[element[0]] = element[1]
    return influence_dict

def calc_rule_influence(rule, influence_dict, obscured_by_tag, outcome_attr):
    total = 0.0
    for attr, op, val in rule:
        if not obscured_by_tag in attr and attr != outcome_attr:
            total += influence_dict[attr]
    return total

def rule_as_string(rule, outcome_attr):
    string = "IF "
    for attr, op, val in rule:
        if attr == outcome_attr:
            endclause = (attr, op, val)
        else:
            string += attr + op + str(val) + " AND "
    string = string[:-5]
    string += " THEN "
    attr, op, val = endclause
    string += attr + op + str(val)
    return string

def write_rules_and_scores(outfilename, testdatafile, influencefile, expanded_rules_dict):
    data = get_test_data(testdatafile)
    influence_dict = get_influence_scores(influencefile)

    out_f = open(outfilename, "w")
    headers = ["Label", "Rule", "Quality", "Influence"]
    writer = csv.DictWriter(out_f, fieldnames = headers)
    file_for_best = open(outfilename+"_BEST", 'w')
    
    best_rules = {} 
    for num in expanded_rules_dict:
    	best_quality = 0.0
    	best_influence_score = 0.0
    	best_rule = None
        for rule in expanded_rules_dict[num]:
            quality = calc_rule_quality(rule, data, NUM_CLASSES, OUTCOME_ATTR)
            influence = calc_rule_influence(rule, influence_dict, OBSCURED_TAG, OUTCOME_ATTR)
            rule_str = rule_as_string(rule, OUTCOME_ATTR)
            row_dict = {"Label": num, "Rule":rule_str, "Quality":quality, "Influence":influence}
            writer.writerow(row_dict)
            
            best_influence_score = influence if quality > best_quality else best_influence_score
            best_rule = "{} & {} & {} & {} \\\\ \n".format(num, rule_str, influence, quality) if quality > best_quality else best_rule
            best_quality = quality if quality > best_quality else best_quality

        best_rules[num] = best_rule

        # pick best rule with lowest discrimination of the bunch 
        for rule in expanded_rules_dict[num]:
            quality = calc_rule_quality(rule, data, NUM_CLASSES, OUTCOME_ATTR)
            influence = calc_rule_influence(rule, influence_dict, OBSCURED_TAG, OUTCOME_ATTR)
            rule_str = rule_as_string(rule, OUTCOME_ATTR)
            row_dict = {"Label": num, "Rule":rule_str, "Quality":quality, "Influence":influence}

            if quality + 0.05 >= best_quality and influence < best_influence_score:
                best_rules[num] = "{} & {} & {} & {} \\\\ \n".format(num, rule_str, influence, quality)
                best_influence_score = influence 
    
    for num in best_rules:
        row = best_rules[num]
        file_for_best.write(row)


NUM_CLASSES = 3
OUTCOME_ATTR = "score_text"
OBSCURED_TAG = "_norace" 
num_to_ruledict = get_rules_from_file("./Rules/compas_big_cn2_2.csv")
orig_to_obscured = get_orig_to_obscured_map("./Data/compas2/original.csv", "./Data/compas2/race_j48_unmerged.csv")
expanded_rules_dict = expand_all_rules(num_to_ruledict, orig_to_obscured, OUTCOME_ATTR, OBSCURED_TAG)
write_rules_and_scores("./Rules/compas_big_race_cn2_2", "./Data/compas2/race_j48.csv", "./Data/compas2/compas_j48_summary.txt", expanded_rules_dict)



"""
NUM_CLASSES = 2
OUTCOME_ATTR = "Outcome"
OBSCURED_TAG = "-noFeature_B_(2i)" 
num_to_ruledict = get_rules_from_file("./Rules/Feature_B_cn2_2.csv")
orig_to_obscured = get_orig_to_obscured_map("./Data/sample/original.csv", "./Data/sample/Feature_B_(2i)_unmerged.csv")
expanded_rules_dict = expand_all_rules(num_to_ruledict, orig_to_obscured, OUTCOME_ATTR, OBSCURED_TAG)
write_rules_and_scores("./Rules/sample_Feature_B_cn2_2", "./Data/sample/Feature_B_(2i).csv", "./Data/sample/sample_orig.summary", expanded_rules_dict)



NUM_CLASSES = 2
OUTCOME_ATTR = "Outcome"
OBSCURED_TAG = "-noFeature_A_(i)" 
num_to_ruledict = get_rules_from_file("./Rules/Feature_A_cn2_2.csv")
orig_to_obscured = get_orig_to_obscured_map("./Data/sample/original.csv", "./Data/sample/Feature_A_(i)_unmerged.csv")
expanded_rules_dict = expand_all_rules(num_to_ruledict, orig_to_obscured, OUTCOME_ATTR, OBSCURED_TAG)
write_rules_and_scores("./Rules/sample_Feature_A_cn2_2", "./Data/sample/Feature_A_(i).csv", "./Data/sample/sample_orig.summary", expanded_rules_dict)



NUM_CLASSES = 2
OUTCOME_ATTR = "Bonus"
OBSCURED_TAG = "-noRace" 
num_to_ruledict = get_rules_from_file("./Rules/race_indirect_cn2_2.csv")
orig_to_obscured = get_orig_to_obscured_map("./Data/bonus_indirect.csv", "./Data/Bonus_Repaired_Indirect_Race/Race_1.0.csv")
expanded_rules_dict = expand_all_rules(num_to_ruledict, orig_to_obscured, OUTCOME_ATTR, OBSCURED_TAG)
write_rules_and_scores("./Rules/bonus_race_indirect_cn2_2", "./Data/Race_indirect.csv", "./Data/Race_indirect.summary", expanded_rules_dict)


NUM_CLASSES = 2
OUTCOME_ATTR = "Bonus"
OBSCURED_TAG = "-noGender" 
num_to_ruledict = get_rules_from_file("./Rules/gender_indirect_cn2_2.csv")
orig_to_obscured = get_orig_to_obscured_map("./Data/bonus_indirect.csv", "./Data/Bonus_Repaired_Indirect_Gender/Gender_1.0.csv")
expanded_rules_dict = expand_all_rules(num_to_ruledict, orig_to_obscured, OUTCOME_ATTR, OBSCURED_TAG)
write_rules_and_scores("./Rules/bonus_gender_indirect_cn2_2", "./Data/Gender_indirect.csv", "./Data/Gender_indirect.summary", expanded_rules_dict)
"""

