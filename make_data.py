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
# Desired Protected Marginals and Conditionals
p_B = .5
p_W = .5
p_M = .5
p_F = .5
p_pos_given_F = .5
p_pos_given_M = .5
p_pos_given_B = .5
p_pos_given_W = .5
p_pos_given_BF = .19
p_pos_given_WF = .27
p_pos_given_BM = .27
p_pos_given_WM = .27
p_pos_given_group = {"B M": p_pos_given_BM, "W M": p_pos_given_WM, "B F": p_pos_given_BF, "W F": p_pos_given_WF}

# probability distribution for education
edu = ["Masters","Bachelors","Highschool"]
p_edu = {"Masters": .3, "Bachelors": .5, "Highschool": .2}
p_pos_given_edu = {"Masters": 0.8, "Bachelors": 0.55, "Highschool": 0.3}


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
p_pos = .5


# Start Script
fname = "Data/bonus_small.csv"
size = 50
# create file for writing
dataset = csv.writer(open(fname, 'w'))
# add header to dataset
dataset.writerow(["Race","Gender","Education","Years","Warnings","Bonus"])

# calculate group marginals based on desired probabilities 
A = np.array([[0, p_pos_given_WM*(1-p_pos_given_WM), 0, p_pos_given_WF*(1-p_pos_given_WF)], 
				[p_pos_given_BM*(1-p_pos_given_BM), 0, p_pos_given_BF*(1-p_pos_given_BF), 0], 
				[p_pos_given_BM*(1-p_pos_given_BM), p_pos_given_WM*(1-p_pos_given_WM), 0, 0], 
				[0, 0, p_pos_given_BF*(1-p_pos_given_BF), p_pos_given_WF*(1-p_pos_given_WF)]])
b = np.array([p_W, p_B, p_M, p_F])
#x = LA.solve(A, b)

def calculate_group_marginals(vars):
	(p_BM, p_WM, p_BF, p_WF) = vars
	# by the law of total probabilities
	a = p_pos_given_WM*p_WM + (1-p_pos_given_WM)*p_WM + \
			p_pos_given_WF*p_WF + (1-p_pos_given_WF)*p_WF - p_W
	b = p_pos_given_BM*p_BM + (1-p_pos_given_BM)*p_BM + \
			p_pos_given_BF*p_BF + (1-p_pos_given_BF)*p_BF - p_B
	c = p_pos_given_WM*p_WM/float(p_pos) + (1-p_pos_given_WM)*p_WM + \
			p_pos_given_BM*p_BM + (1-p_pos_given_BM)*p_BM - p_M
	d = p_pos_given_WF*p_WF + (1-p_pos_given_WF)*p_WF + \
			p_pos_given_BF*p_BF + (1-p_pos_given_BF)*p_BF - p_F
	return [a,b,c,d]
x = optimize.fsolve(calculate_group_marginals,(0,0,0,0))

def f(x):
    y = np.dot(A, x) - b
    return np.dot(y, y)

# subject to the constraint cons:
cons = ({'type': 'eq', 'fun': lambda x: x.sum() - 1},
		{'type':'ineq', 'fun':lambda x: x})
bnds = ((.27,.3), (.22,.3), (.24,.3), (.2,.28))
res = optimize.minimize(f, [0, 0, 0, 0], method='SLSQP',bounds=bnds, constraints=cons, 
                        options={'disp': False})
# best calculation of marginals
p_protected = res['x']
print(p_protected)
p_group = {"B M": p_protected[0], "W M":p_protected[1], "B F":p_protected[2], "W F":p_protected[3]}
# generate protected groups using group marginal probabililities
protected_cols = np.random.choice(protected, size, p=p_protected)

# generate protected groups columns
protected_groups_cols = [protected_group.split(' ') for protected_group in protected_cols]
# generate class column
#class_col = np.random.choice(class_, size, p=[p_pos, 1-p_pos])
class_col = [np.random.choice(class_, 1, p=[p_pos_given_group[i], 1-p_pos_given_group[i]])[0] for i in protected_cols]
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

	# P(some_num_edu|+) = (P(+|num_warning)*P(num_warnings))/P(+)
	p_edu_given_pos = [(p_pos_given_edu[e]*p_edu[e])/float(p_pos) for e in edu]
	p_edu_given_neg = [1-p for p in p_edu_given_pos]
	education = [str(num) for num in np.random.choice(edu,1,p_edu_given_pos if class_col[i]=='yes' else p_edu_given_neg)]
	
	# write completed row to dataset
	dataset.writerow(protected_groups_cols[i]+education+year+warning+[class_col[i]])

Data = pd.read_csv(fname)
size = len(Data)

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

# Write to log
t = datetime.datetime.now()
log = open("Data/log.txt", 'a')
log.write("{}-{}-{} {}:{}:{}\n".format(t.year,t.month,t.day,t.hour,t.minute,t.second))
log.write("Data: {}\tsize: {}\n".format(fname, size))
log.write("P(B): {}\tP(W): {}\tP(M): {}\tP(F): {}\n".format(p_B, p_W, p_M, p_F)) 
log.write("P(+|B): {}\tP(+|W): {}\tP(+|M): {}\tP(+|F): {}\n".format(p_pos_given_B, p_pos_given_W, p_pos_given_M, p_pos_given_F)) 
log.write("P(+|BM): {}\tP(+|WM): {}\tP(+|BF): {}\tP(+|WF): {}\n".format(p_pos_given_BM, p_pos_given_WM, p_pos_given_BF, p_pos_given_WF)) 
log.write("P(BM): {}\tP(WM): {}\tP(BF): {}\tP(WF): {}\n".format(p_protected[0], p_protected[1], p_protected[2], p_protected[3]))
#log.write("Calculations from dataset:\n")

#ax = sns.countplot(x="Bonus",data=Data)

