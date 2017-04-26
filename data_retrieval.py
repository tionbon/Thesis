import os, sys
import datetime
import csv
from collections import defaultdict



def temp():
	repaired_files = []

	#identifier = dir_
	#os.makedirs(identifier)
	
	for i in range(11):
		repair_value = i/10.0

		# Access audited file
		file = open("Data/bonus_indirect.csv", 'rt')
		repaired_reader = csv.reader(file)

		# Process auditied file
		repaired_file = open("Data/bonus_indirect.tab", 'w')
		# convert to tab separated file 
		repaired_file.write("\t".join(next(repaired_reader)) +"\n")
		repaired_file.write("d\td\tHighschool Bachelors Masters\t<3 3-6 >6\tlow medium high\td\n")
		repaired_file.write("\t\t\t\t\tclass\n")
		for row in repaired_reader:
			repaired_file.write("\t".join(row)+"\n")

		repaired_file.close()
		repaired_files.append(repaired_file)

def repaired_data_retrieval(dir_, repaired_dir, repaired_attrib):
	repaired_files = []

	identifier = dir_
	os.makedirs(identifier)
	
	for i in range(11):
		repair_value = i/10.0

		# Access audited file
		file = open(repaired_dir + "/{}.audit.test.repaired_{}.data".format(repaired_attrib, repair_value), 'rt')
		repaired_reader = csv.reader(file)

		# Process auditied file
		repaired_file = open("{}/{}_{}.tab".format(identifier, repaired_attrib, repair_value), 'w')
		# convert to tab separated file 
		repaired_file.write("\t".join(next(repaired_reader)) +"\n")
		repaired_file.write("d\td\tHighschool Bachelors Masters\t<3 3-6 >6\tlow medium high\td\n")
		repaired_file.write("\t\t\t\t\tclass\n")
		for row in repaired_reader:
			repaired_file.write("\t".join(row)+"\n")

		repaired_file.close()
		repaired_files.append(repaired_file)

def retrieval_and_merger(orig_file, dir_, repaired_dir, repaired_attrib):
	repaired_files = []

	identifier = dir_	
	repair_value = 1.0

	# Access original file
	f2 = open(orig_file, 'rt')
	orig_reader = csv.reader(f2)

	# Access audited file
	f1 = open(repaired_dir + "/{}.audit.test.repaired_{}.data".format(repaired_attrib, repair_value), 'rt')
	repaired_reader = csv.reader(f1)

	# Open new file for writing
	repaired_file = open("{}/{}_indirect.tab".format(identifier, repaired_attrib), 'w') 

	# Merge Headers
	orig_header = next(orig_reader)
	repaired_header = [i+'-no{}'.format(repaired_attrib) for i in next(repaired_reader)]
	merged = [None]*(len(orig_header)+len(repaired_header))
	merged[::2] = orig_header
	merged[1::2] = repaired_header
	
	repaired_file.write("\t".join(merged)+"\n")
	repaired_file.write("d\td\td\td\tHighschool Bachelors Masters\tHighschool Bachelors Masters\t<3 3-6 >6\t<3 3-6 >6\tlow medium high\tlow medium high\td\td\n")
	repaired_file.write("\t\t\t\t\t\t\t\t\t\tclass\tignore\n")

	# convert to tab separated file, merge and write
	for orig_row in orig_reader:
		repaired_row = next(repaired_reader)
		merged = [None]*(len(orig_row)+len(repaired_row))
		merged[::2] = orig_row
		merged[1::2] = repaired_row
		repaired_file.write("\t".join(merged)+"\n")

	summary = open("{}/{}_indirect.summary".format(identifier, repaired_attrib), 'w')
	f = open(repaired_dir + "/summary.txt", 'r')
	for line in f:
		if line.startswith('Ranked Features by accuracy:'):
			ds = line.split(':')[1][1:]
 			summary.write(ds)
 			summary.close()

	repaired_file.close()
	repaired_files.append(repaired_file)


def ricci_repaired_data_retrieval():
	repaired_dir = "./Audit/audits/1487655656.76/"
	repaired_files = []

	identifier = "ricci"
	os.chdir("Data")
	os.makedirs(identifier)
	
	for i in range(11):
		repair_value = i/10.0

		# Access audited file
		file = open(repaired_dir + "/Race.audit.test.repaired_{}.data".format(repair_value), 'rt')
		repaired_reader = csv.reader(file)

		# Process auditied file
		repaired_file = open("{}/Race_{}.tab".format(identifier, repair_value), 'w')
		# convert to tab separated file 
		repaired_file.write("\t".join(next(repaired_reader)) +"\n")
		repaired_file.write("d\tc\td\td\tc\td\n")
		repaired_file.write("\t\t\t\t\tclass\n")
		for row in repaired_reader:
			repaired_file.write("\t".join(row)+"\n")

		repaired_file.close()
		repaired_files.append(repaired_file)

def adult_retrieval_and_merger(orig_file, repaired_dir):
	repair_value = 1.0

	# Access original file
	orig = open(orig_file, 'rt')
	orig_reader = csv.reader(orig)

	# Open new file for writing original data
	orig_file = open("./Data/adult/original_dt.tab", 'w') 

	# Get column names 
	orig_cols = [col_name.replace("-", "_") for col_name in next(orig_reader)]
	# convert original file to tab separated file 
	orig_file.write("\t".join(orig_cols) +"\n")
	orig_file.write("continuous\tPrivate Self-emp-not-inc Self-emp-inc Federal-gov Local-gov State-gov Without-pay Never-worked\tcontinuous\tBachelors Some-college 11th HS-grad Prof-school Assoc-acdm Assoc-voc 9th 7th-8th 12th Masters 1st-4th 10th Doctorate 5th-6th Preschool\tcontinuous\tMarried-civ-spouse Divorced Never-married Separated Widowed Married-spouse-absent Married-AF-spouse\tTech-support Craft-repair Other-service Sales Exec-managerial Prof-specialty Handlers-cleaners Machine-op-inspct Adm-clerical Farming-fishing Transport-moving Priv-house-serv Protective-serv Armed-Forces\tWife Own-child Husband Not-in-family Other-relative Unmarried\tWhite Asian-Pac-Islander Amer-Indian-Eskimo Other Black\tFemale Male\tcontinuous\tcontinuous\tcontinuous\tUnited-States Cambodia England Puerto-Rico Canada Germany Outlying-US(Guam-USVI-etc) India Japan Greece South China Cuba Iran Honduras Philippines Italy Poland Jamaica Vietnam Mexico Portugal Ireland France Dominican-Republic Laos Ecuador Taiwan Haiti Columbia Hungary Guatemala Nicaragua Scotland Thailand Yugoslavia El-Salvador Trinadad&Tobago Peru Hong Holand-Netherlands\t>50K <=50K\n")
	orig_file.write("\t\t\t\t\t\t\t\t\t\t\t\t\t\tclass\n")
	for row in orig_reader:
		orig_file.write("\t".join(row)+"\n")

	# Process repaired files
	features = orig_cols[:-1]
	for feature in features:
		orig.seek(0)
		next(orig_reader)

		# Access audited files
		f1 = open(repaired_dir + "/{}.audit.test.repaired_{}.data".format(feature.replace("_","-"), repair_value), 'rt')
		repaired_reader = csv.reader(f1)

		# Open new file for writing merged data
		with open("./Data/adult/{}_dt.csv".format(feature), 'w') as file:
			repaired_file = csv.writer(file)

			# Merge Headers
			header = orig_cols
			repaired_header = [i+'_no{}'.format(feature) for i in header]
			merged = [None]*(len(header)+len(repaired_header))
			merged[::2] = header
			merged[1::2] = repaired_header
			
			repaired_file.writerow(merged)

			# convert to tab separated file, merge and write
			for orig_row in orig_reader:
				repaired_row = next(repaired_reader)
				merged = [None]*(len(orig_row)+len(repaired_row))
				merged[::2] = orig_row
				merged[1::2] = repaired_row
				repaired_file.writerow(merged)

	summary = open("./Data/adult/adult_dt.summary", 'w')
	f = open(repaired_dir + "/summary.txt", 'r')
	for line in f:
		if line.startswith('Ranked Features by accuracy:'):
			ds = line.split(':')[1][1:].replace("-","_")
			summary.write(ds)
			summary.close()

def adult2_retrieval_and_merger(orig_train, predictions_file, repaired_file, feature, learner):
	repair_value = 1.0

	# Access original training file
	orig_train = open(orig_train, 'rt')
	orig_train_reader = csv.reader(orig_train)
	

	predictions = open(predictions_file, 'rt')
	predictions_reader = csv.reader(predictions)
	next(predictions_reader)

	# Open new file for writing original data
	orig_file = open("./Data/adult2/original_{}.tab".format(learner), 'w') 

	# Get column names 
	col_names = next(orig_train_reader) 
	orig_cols = [col_name.replace("-","_") for col_name in col_names]

	# convert original file to tab separated file 
	orig_file.write("\t".join(orig_cols) +"\n")
	orig_file.write("continuous\tPrivate Self-emp-not-inc Self-emp-inc Federal-gov Local-gov State-gov Without-pay Never-worked\tcontinuous\tBachelors Some-college 11th HS-grad Prof-school Assoc-acdm Assoc-voc 9th 7th-8th 12th Masters 1st-4th 10th Doctorate 5th-6th Preschool\tcontinuous\tMarried-civ-spouse Divorced Never-married Separated Widowed Married-spouse-absent Married-AF-spouse\tTech-support Craft-repair Other-service Sales Exec-managerial Prof-specialty Handlers-cleaners Machine-op-inspct Adm-clerical Farming-fishing Transport-moving Priv-house-serv Protective-serv Armed-Forces\tWife Own-child Husband Not-in-family Other-relative Unmarried\tWhite Asian-Pac-Islander Amer-Indian-Eskimo Other Black\tFemale Male\tcontinuous\tcontinuous\tcontinuous\tUnited-States Cambodia England Puerto-Rico Canada Germany Outlying-US(Guam-USVI-etc) India Japan Greece South China Cuba Iran Honduras Philippines Italy Poland Jamaica Vietnam Mexico Portugal Ireland France Dominican-Republic Laos Ecuador Taiwan Haiti Columbia Hungary Guatemala Nicaragua Scotland Thailand Yugoslavia El-Salvador Trinadad&Tobago Peru Hong Holand-Netherlands\t>50K <=50K\n")
	orig_file.write("\t\t\t\t\t\t\t\t\t\t\t\t\t\tclass\n")
	for row in orig_train_reader:
		orig_file.write("\t".join(row[:-1]+[next(predictions_reader)[-1]])+"\n")

	# Access audited files
	f1 = open(repaired_file, 'rt')
	repaired_reader = csv.reader(f1)
	next(repaired_reader)

	# Open new file for writing merged data
	with open("./Data/adult2/{}_{}.csv".format(feature, learner), 'w') as file:
		orig_train.seek(0)
		next(orig_train_reader)
		predictions.seek(0)
		next(predictions_reader)
		repaired_file = csv.writer(file)

		# Merge Headers
		header = orig_cols
		repaired_header = [i+'_no{}'.format(feature) for i in header]
		merged = [None]*(len(header)+len(repaired_header))
		merged[::2] = header
		merged[1::2] = repaired_header
		
		repaired_file.writerow(merged)

		# convert to tab separated file, merge and write
		for orig_row in orig_train_reader:
			repaired_row = next(repaired_reader)
			merged = [None]*(len(orig_row)+len(repaired_row))
			merged[::2] = orig_row[:-1]+[next(predictions_reader)[-1]]
			merged[1::2] = repaired_row
			repaired_file.writerow(merged)


	summary = open("./Data/adult2/adult_{}_summary.txt".format(learner), 'w')
	f = open("./Data/predictions/adult_{}_summary.txt".format(learner), 'r')
	for line in f:
		if line.startswith('Ranked Features by accuracy:'):
			ds = line.split(':')[1][1:].replace("-","_")
 			summary.write(ds)
 	summary.close()	

def sample_retrieval_and_merger(orig_file, repaired_dir, repaired_attribs):
	repair_value = 1.0

	# Access original file
	orig = open(orig_file, 'rt')
	orig_reader = csv.reader(orig)

	# Open new file for writing original data
	orig_file = open("./Data/sample/original.tab", 'w') 

	# convert original file to tab separated file 
	orig_file.write("\t".join(next(orig_reader)) +"\n")
	orig_file.write("c\tc\tc\tc\tc\td\n")
	orig_file.write("\t\t\t\t\tclass\n")
	for row in orig_reader:
		orig_file.write("\t".join(row)+"\n")

	# Process repaired files
	for repaired_attrib in repaired_attribs:
		orig.seek(0)
		next(orig_reader)

		# Access audited files
		f1 = open(repaired_dir + "/{}.audit.test.repaired_{}.data".format(repaired_attrib, repair_value), 'rt')
		repaired_reader = csv.reader(f1)

		# Open new file for writing merged data
		repaired_file = open("./Data/sample/{}.tab".format(repaired_attrib), 'w') 

		# Merge Headers
		header = next(repaired_reader)
		repaired_header = [i+'-no{}'.format(repaired_attrib) for i in header]
		merged = [None]*(len(header)+len(repaired_header))
		merged[::2] = header
		merged[1::2] = repaired_header
		


		# convert to tab separated file, merge and write
		for orig_row in orig_reader:
			repaired_row = next(repaired_reader)
			merged = [None]*(len(orig_row)+len(repaired_row))
			merged[::2] = orig_row
			merged[1::2] = repaired_row
			repaired_file.write("\t".join(merged)+"\n")

	summary = open("./Data/sample/sample.summary", 'w')
	f = open(repaired_dir + "/summary.txt", 'r')
	for line in f:
		if line.startswith('Ranked Features by accuracy:'):
			ds = line.split(':')[1][1:]
 			summary.write(ds)
 			summary.close()

	repaired_file.close()


def sample2_retrieval_and_merger(orig_train, predictions_file, repaired_file, feature, learner):
	repair_value = 1.0

	# Access original training file
	orig_train = open(orig_train, 'rt')
	orig_train_reader = csv.reader(orig_train)
	next(orig_train_reader)

	predictions = open(predictions_file, 'rt')
	predictions_reader = csv.reader(predictions)
	next(predictions_reader)

	# Open new file for writing original data
	orig_file = open("./Data/sample2/original_{}.tab".format(learner), 'w') 

	# Get column names 
	col_names = ["Feature_A","Feature_B","Feature_C","Constant_Feature","Random_Feature","Outcome"]
	orig_cols = [col_name for col_name in col_names]

	# convert original file to tab separated file 
	orig_file.write("\t".join(col_names) +"\n")
	orig_file.write("c\tc\tc\tc\tc\td\n")
	orig_file.write("\t\t\t\t\tclass\n")
	for row in orig_train_reader:
		orig_file.write("\t".join(row[:-1]+[next(predictions_reader)[-1]])+"\n")

	# Access audited files
	f1 = open(repaired_file, 'rt')
	repaired_reader = csv.reader(f1)
	next(repaired_reader)

	# Open new file for writing merged data
	with open("./Data/sample2/{}_{}.csv".format(feature, learner), 'w') as file:
		orig_train.seek(0)
		next(orig_train_reader)
		predictions.seek(0)
		next(predictions_reader)
		repaired_file = csv.writer(file)

		# Merge Headers
		header = orig_cols
		repaired_header = [i+'_no{}'.format(feature) for i in header]
		merged = [None]*(len(header)+len(repaired_header))
		merged[::2] = header
		merged[1::2] = repaired_header
		
		repaired_file.writerow(merged)

		# convert to tab separated file, merge and write
		for orig_row in orig_train_reader:
			repaired_row = next(repaired_reader)
			merged = [None]*(len(orig_row)+len(repaired_row))
			merged[::2] = orig_row[:-1]+[next(predictions_reader)[-1]]
			merged[1::2] = repaired_row
			repaired_file.writerow(merged)
				

#	summary = open("./Data/sample2/sample_svm_summary.txt", 'w')
#	f = open("./Data/predictions/sample_svm_summary.txt", 'r')
#	for line in f:
#		if line.startswith('Ranked Features by accuracy:'):
#			ds = line.split(':')[1][1:].replace("-","_")
# 			summary.write(ds)
# 			summary.close()	

def sample_data_retrieval(orig_file, repaired_dir, repaired_attribs):
	repair_value = 1.0

	# Access original file
	orig = open(orig_file, 'rt')
	orig_reader = csv.reader(orig)

	# Open new file for writing original data
	orig_file = open("./Data/sample/original.tab", 'w') 

	# convert original file to tab separated file 
	orig_file.write("\t".join(next(orig_reader)) +"\n")
	orig_file.write("c\tc\tc\tc\tc\td\n")
	orig_file.write("\t\t\t\t\tclass\n")
	for row in orig_reader:
		orig_file.write("\t".join(row)+"\n")

	# Process repaired files
	for repaired_attrib in repaired_attribs:
		# Access audited files
		f1 = open(repaired_dir + "/{}.audit.test.repaired_{}.data".format(repaired_attrib, repair_value), 'rt')
		repaired_reader = csv.reader(f1)

		# Open new file for writing merged data
		repaired_file = open("./Data/sample/{}_unmerged.tab".format(repaired_attrib), 'w') 

		# Merge Headers
		header = next(repaired_reader)
		repaired_file.write("\t".join(header)+"\n")
		repaired_file.write("c\tc\tc\tc\tc\td\n")
		repaired_file.write("\t\t\t\t\tclass\n")
		for row in repaired_reader:
			repaired_file.write("\t".join(row)+"\n")

	summary = open("./Data/sample/sample.summary", 'w')
	f = open(repaired_dir + "/summary.txt", 'r')
	for line in f:
		if line.startswith('Ranked Features by accuracy:'):
			ds = line.split(':')[1][1:]
 			summary.write(ds)
 			summary.close()

	repaired_file.close()

def compas_retrieval_and_merger(orig_train, predictions_file, repaired_file, feature, learner):
	repair_value = 1.0

	# Access original training file
	orig_train = open(orig_train, 'rt')
	orig_train_reader = csv.reader(orig_train)
	

	predictions = open(predictions_file, 'rt')
	predictions_reader = csv.reader(predictions)
	next(predictions_reader)

	# Open new file for writing original data
	orig_file = open("./Data/compas/original_{}.tab".format(learner), 'w') 

	# Get column names 
	col_names = next(orig_train_reader)
	orig_cols = [col_name for col_name in col_names[:-1]]

	# convert original file to tab separated file 
	orig_file.write("\t".join(orig_cols) +"\n")
	orig_file.write("d\tc\td\td\tc\tc\tc\tc\td\td\tc\td\n")
	orig_file.write("\t\t\t\t\t\t\t\t\t\tignore\tclass\n")
	for row in orig_train_reader:
		orig_file.write("\t".join(row[:-2]+[next(predictions_reader)[-1]])+"\n")

	# Access audited files
	f1 = open(repaired_file, 'rt')
	repaired_reader = csv.reader(f1)
	next(repaired_reader)

	# Open new file for writing merged data
	with open("./Data/compas/{}_{}.csv".format(feature, learner), 'w') as file:
		orig_train.seek(0)
		next(orig_train_reader)
		predictions.seek(0)
		next(predictions_reader)
		repaired_file = csv.writer(file)

		# Merge Headers
		header = orig_cols
		repaired_header = [i+'_no{}'.format(feature) for i in header]
		merged = [None]*(len(header)+len(repaired_header))
		merged[::2] = header
		merged[1::2] = repaired_header
		
		repaired_file.writerow(merged)

		# convert to tab separated file, merge and write
		for orig_row in orig_train_reader:
			repaired_row = next(repaired_reader)[:-1]
			merged = [None]*(len(orig_row)-1+len(repaired_row))
			merged[::2] = orig_row[:-2]+[next(predictions_reader)[-1]]
			merged[1::2] = repaired_row
			repaired_file.writerow(merged)
				

	summary = open("./Data/compas/compas_{}_summary.txt".format(learner), 'w')
	f = open("./Data/predictions/compas_{}/summary.txt".format(learner), 'r')
	for line in f:
		if line.startswith('Ranked Features by accuracy:'):
			ds = line.split(':')[1][1:].replace("-","_")
 			summary.write(ds)
 			summary.close()	
		
def compas2_retrieval_and_merger(orig_train, predictions_file, repaired_file, feature, learner):
	repair_value = 1.0

	# Access original training file
	orig_train = open(orig_train, 'rt')
	orig_train_reader = csv.reader(orig_train)
	

	predictions = open(predictions_file, 'rt')
	predictions_reader = csv.reader(predictions)
	next(predictions_reader)

	# Open new file for writing original data
	orig_file = open("./Data/compas2/original_{}_test.tab".format(learner), 'w') 

	# Get column names 
	col_names = next(orig_train_reader)
	orig_cols = [col_name for col_name in col_names[:-1]]

	# convert original file to tab separated file 
	orig_file.write("\t".join(orig_cols) +"\n")
	orig_file.write("d\tc\td\td\tc\tc\tc\tc\td\td\tc\td\n")
	orig_file.write("\t\t\t\t\t\t\t\t\t\tignore\tclass\n")
	for row in orig_train_reader:
		orig_file.write("\t".join(row[:-2]+[next(predictions_reader)[0]])+"\n")

	# Access audited files
	f1 = open(repaired_file, 'rt')
	repaired_reader = csv.reader(f1)
	next(repaired_reader)

	# Open new file for writing merged data
	with open("./Data/compas2/{}_{}_test.csv".format(feature, learner), 'w') as file:
		orig_train.seek(0)
		next(orig_train_reader)
		predictions.seek(0)
		next(predictions_reader)
		repaired_file = csv.writer(file)

		# Merge Headers
		header = orig_cols
		repaired_header = [i+'_no{}'.format(feature) for i in header]
		merged = [None]*(len(header)+len(repaired_header))
		merged[::2] = header
		merged[1::2] = repaired_header
		
		repaired_file.writerow(merged)

		# convert to tab separated file, merge and write
		for orig_row in orig_train_reader:
			repaired_row = next(repaired_reader)[:-1]
			merged = [None]*(len(orig_row)-1+len(repaired_row))
			merged[::2] = orig_row[:-2]+[next(predictions_reader)[0]]
			merged[1::2] = repaired_row
			repaired_file.writerow(merged)
				

	summary = open("./Data/compas2/compas_{}_summary.txt".format(learner), 'w')
	f = open("./Data/predictions/compas_{}/summary.txt".format(learner), 'r')
	for line in f:
		if line.startswith('Ranked Features by accuracy:'):
			ds = line.split(':')[1][1:].replace("-","_")
 			summary.write(ds)
 			summary.close()	

def joint_retrieval_and_merger(orig_file, dir_, repaired_dir, repaired_attrib):
	repaired_files = []

	identifier = dir_	
	repair_value = 1.0

	# Access original file
	f2 = open(orig_file, 'rt')
	orig_reader = csv.reader(f2)

	# Access audited file
	f1 = open(repaired_dir + "/{}.audit.test.repaired_{}.data".format(repaired_attrib, repair_value), 'rt')
	repaired_reader = csv.reader(f1)

	# Open new file for writing
	repaired_file = open("{}/{}_direct.tab".format(identifier, repaired_attrib), 'w') 

	# Merge Headers
	orig_header = next(orig_reader)
	repaired_header = [i+'-no{}'.format(repaired_attrib) for i in next(repaired_reader)]
	merged = [None]*(len(orig_header)+len(repaired_header))
	merged[::2] = orig_header
	merged[1::2] = repaired_header
	
	repaired_file.write("\t".join(merged)+"\n")
	repaired_file.write("d\td\td\td\tHighschool Bachelors Masters\tHighschool Bachelors Masters\t<3 3-6 >6\t<3 3-6 >6\tlow medium high\tlow medium high\td\td\n")
	repaired_file.write("\t\t\t\t\t\t\t\t\t\tclass\tignore\n")

	# convert to tab separated file, merge and write
	for orig_row in orig_reader:
		repaired_row = next(repaired_reader)
		merged = [None]*(len(orig_row)+len(repaired_row))
		merged[::2] = orig_row
		merged[1::2] = repaired_row
		repaired_file.write("\t".join(merged)+"\n")

	summary = open("{}/joint.summary".format(identifier, repaired_attrib), 'w')
	f = open(repaired_dir + "/summary.txt", 'r')
	for line in f:
		if line.startswith('Ranked Features by accuracy:'):
			ds = line.split(':')[1][1:]
 			summary.write(ds)
 			summary.close()

	repaired_file.close()
	repaired_files.append(repaired_file)

if __name__ == "__main__":
	#repaired_dir = "./Audit/audits/1487023139.65"
	#repaired_dir = "./Audit/audits/1487655656.76/"
	#repaired_dir = "./Audit/audits/1488339786.6" 
	#repaired_dir = "./Audit/audits/1489282159.55" # direct
	repaired_dir = "./Audit/audits/1489282271.25/" # indirect 
	#repaired_dir = "./Audit/audits/1489762753.74" # sample 
	#repaired_dir = "./Audit/audits/1490709060.42" # sample dt
	#repaired_dir = "./Audit/audits/1490573441.42" # indirect_on_one 
	#repaired_dir = "./Audit/audits/1490562027.25" # adult
	#repaired_dir = "./Audit/audits/1490582950.82" # adult 
	#repaired_dir = "./Audit/audits/1492753002.2/" # direct joint
	#attribs = ["Race", "Gender"]
	#attribs = ['Feature_A_(i)', 'Feature_B_(2i)', 'Feature_C_(-i)', 'Random_Feature', 'Constant_Feature'] 
	#attribs = 
	#orig_file = "./Audit/test_data/adult.csv"
	#orig_file = repaired_dir+"Feature_A_(i).audit.test.repaired_0.0.data"
	#orig_file = "./Data/bonus.csv"
	#orig_file = "./Data/bonus_indirect_on_one.csv"
	#orig_file = "./Audit/audits/1490582950.82/age.audit.test.repaired_0.0.data"
	#orig_train = "./Data/predictions/sample_j48_original_train_data.csv"
	#predictions ="./Data/predictions/sample_j48_original_train_data.predictions"
	#orig_file = "./Audit/audits/1490652783.56/Random_Feature.audit.test.repaired_0.0.data"
	#learner = "j48"
	#orig_train = "./Data/predictions/adult_{}/original_train_data.csv".format(learner)
	#predictions ="./Data/predictions/adult_{}_original_train_data.predictions".format(learner)
	#orig_file = "./Audit/audits/1489762753.74/Random_Feature.audit.test.repaired_0.0.data"
	#repaired_file = "./Data/predictions/relationship_train_{}.data".format(learner)
	#feature = "relationship"
	#orig_train = "./Data/predictions/compas_{}/original_train_data.csv".format(learner)
	#orig_test = "./Data/predictions/compas_{}/original_test_data.csv".format(learner)
	#predictions ="./Data/predictions/compas_{}/original_train_data.predictions".format(learner)
	#predictions_test ="./Data/predictions/compas_{}/original_test_data.predictions".format(learner)
	#orig_file = "./Audit/audits/1489762753.74/Random_Feature.audit.test.repaired_0.0.data"
	#repaired_file = "./Data/predictions/compas_race_{}_data.csv".format(learner)
	#repaired_file_test = "./Data/predictions/compas_race_{}_test.csv".format(learner)
	#feature = "race"
	#dir_ = "./Data"
	#for i in attribs:
	#	retrieval_and_merger(orig_file, dir_, repaired_dir, i)
	#compas2_retrieval_and_merger(orig_train, predictions, repaired_file, feature, learner)
	#compas2_retrieval_and_merger(orig_test, predictions_test, repaired_file_test, feature, learner)
	#adult_retrieval_and_merger(orig_file, repaired_dir)
	orig_file = "./Data/bonus_indirect.csv"
	repaired_attrib = "Gender"
	dir_ = "./Data"
	retrieval_and_merger(orig_file, dir_, repaired_dir, repaired_attrib)
