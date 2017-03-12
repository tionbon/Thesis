import numpy as np
import csv
import math
import numpy.linalg as LA
import scipy.optimize as optimize
import datetime
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


# probability distribution of protected attributes appearing in data
protected = ["B M", "W M", "B F", "W F"]

# probability distribution for education
edu = ["Masters","Bachelors","Highschool"]
p_edu = {"Masters": .3, "Bachelors": .5, "Highschool": .2}
p_pos_given_edu = {"Masters": 0.8, "Bachelors": 0.55, "Highschool": 0.3}
p_edu_given_group = {"B M":[.05,.15,.80], "B F":[.35,.50,.15], "W M":[.30,.50,.20], "W F":[.30,.45,.25]}


# probability distribution for working 1 to 6 years
years = ["<3", "3-6", ">6"]
p_years = {"<3": .2, "3-6": .3, ">6": .5}
p_pos_given_years = {"<3": .1, "3-6": .3,">6": .7}

# probability distribution for getting 1 to 10 warning
warnings = ["low", "medium", "high"]
p_warnings = {"low": .60, "medium": .3, "high": .1}
p_pos_given_warnings = {"low": .8, "medium": .5, "high": .05}

# Class
class_ = ["yes", "no"]
p_pos = .4

# Start Script
fname = "Data/bonus_indirect.csv"
size = 5000
# create file for writing
dataset = csv.writer(open(fname, 'w'))
# add header to dataset
dataset.writerow(["Race","Gender","Education","Years","Warnings","Bonus"])

# generate protected cols
protected_cols = np.random.choice(protected, size, p=[.25, .25, .25, .25])
protected_groups_cols = [protected_group.split(' ') for protected_group in protected_cols]

# generate education col based on protected col
edu_col = [np.random.choice(edu, 1, p=p_edu_given_group[grp])[0] for grp in protected_cols]

# generate class based on education
class_col = [np.random.choice(class_, 1, p=[p_pos_given_edu[i], 1-p_pos_given_edu[i]])[0] for i in edu_col]

# add rest of information by case 
for i in range(size):
	# P(some_year|+) = (P(+|that_year)*P(that_year))/P(+)
	p_year_given_pos = [(p_pos_given_years[yr]*p_years[yr])/float(p_pos) for yr in years]
	p_year_given_neg = [1-p for p in p_year_given_pos]
	year = [str(num) for num in np.random.choice(years,1,p_year_given_pos if class_col[i]=='yes' else p_year_given_neg)]

	# P(some_num_warnings|+) = (P(+|num_warning)*P(num_warnings))/P(+)
	p_warnings_given_pos = [(p_pos_given_warnings[w]*p_warnings[w])/float(p_pos) for w in warnings]
	p_warnings_given_neg = [1-p for p in p_warnings_given_pos]
	warning = [str(num) for num in np.random.choice(warnings,1,p_warnings_given_pos if class_col[i]=='yes' else p_warnings_given_neg)]

	# write completed row to dataset
	dataset.writerow(protected_groups_cols[i]+[edu_col[i]]+year+warning+[class_col[i]])

Data = pd.read_csv(fname)
size = len(Data)

pos = Data.query("Bonus == 'yes'")
num_pos = len(pos)

B = Data.query("Race == 'B'")
W = Data.query("Race == 'W'")
M = Data.query("Gender == 'M'")
F = Data.query("Gender == 'F'")

BF = Data.query("Race == 'B' & Gender == 'F'")
BM = Data.query("Race == 'B' & Gender == 'M'")
WF = Data.query("Race == 'W' & Gender == 'F'")
WM = Data.query("Race == 'W' & Gender == 'M'")

# Proportions of Positive Outcomes by Race and Gender
B_pos = Data.query("Race == 'B' & Bonus == 'yes'")
B_prop = len(B_pos)/float(len(B))

W_pos = Data.query("Race == 'W' & Bonus == 'yes'")
W_prop = len(W_pos)/float(len(W))

M_pos = Data.query("Gender == 'M' & Bonus == 'yes'")
M_prop = len(M_pos)/float(len(M))

F_pos = Data.query("Gender == 'F' & Bonus == 'yes'")
F_prop =  len(F_pos)/float(len(F))
print ("P(+ and B), P(+ and W), P(+ and M), P(+ and F)")
print (B_prop, W_prop, M_prop, F_prop)


# Proportions of Groups with Positive Outcomes
BF_pos = Data.query("Race == 'B' & Gender == 'F' & Bonus == 'yes'")
BF_prop = len(BF_pos)/float(len(BF))

BM_pos = Data.query("Race == 'B' & Gender == 'M' & Bonus == 'yes'")
BM_prop = len(BM_pos)/float(len(BM))

WF_pos = Data.query("Race == 'W' & Gender == 'F' & Bonus == 'yes'")
WF_prop = len(WF_pos)/float(len(WF))

WM_pos = Data.query("Race == 'W' & Gender == 'M' & Bonus == 'yes'")
WM_prop =  len(WM_pos)/float(len(WM))
print ("P(+ and BF), P(+ and BM), P(+ and WF), P(+ and WM)")
print (BF_prop, BM_prop, WF_prop, WM_prop)