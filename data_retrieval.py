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

	summary = open("{}/{}_.summary".format(identifier, repaired_attrib), 'w')
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

def adult_retrieval_and_merger(orig_file, dir_, repaired_dir, repaired_attrib):
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
	repaired_file = open("{}/adult_{}.tab".format(identifier, repaired_attrib), 'w') 

	# Merge Headers
	orig_header = next(orig_reader)
	repaired_header = [i+'-no{}'.format(repaired_attrib) for i in next(repaired_reader)]
	merged = [None]*(len(orig_header)+len(repaired_header))
	merged[::2] = orig_header
	merged[1::2] = repaired_header
	
	repaired_file.write("\t".join(merged)+"\n")
	type = "continuous\tPrivate Self-emp-not-inc Self-emp-inc Federal-gov Local-gov State-gov Without-pay Never-worked\t \
			continuous\tBachelors Some-college 11th HS-grad Prof-school Assoc-acdm Assoc-voc 9th 7th-8th 12th Masters 1st-4th 10th Doctorate 5th-6th Preschool \
			\tcontinuous\tMarried-civ-spouse Divorced Never-married Separated Widowed Married-spouse-absent Married-AF-spouse \
			\tTech-support Craft-repair Other-service Sales Exec-managerial Prof-specialty Handlers-cleaners Machine-op-inspct \
			Adm-clerical Farming-fishing Transport-moving Priv-house-serv Protective-serv Armed-Forces\tWife Own-child Husband \
			Not-in-family Other-relative Unmarried\tWhite Asian-Pac-Islander Amer-Indian-Eskimo Other Black\tFemale Male\tcontinuous \
			\tcontinuous\tcontinuous\tUnited-States Cambodia England Puerto-Rico Canada Germany Outlying-US(Guam-USVI-etc) \
			 India Japan Greece South China Cuba Iran Honduras Philippines Italy Poland Jamaica Vietnam Mexico Portugal \
			 Ireland France Dominican-Republic Laos Ecuador Taiwan Haiti Columbia Hungary Guatemala Nicaragua Scotland \
			 Thailand Yugoslavia El-Salvador Trinadad&Tobago Peru Hong Holand-Netherlands\t>50K <=50K\n"
	col_info = "\t\t\t\t\t\t\t\t\t\t\t\t\t\tclass \n"
	repaired_file.write(types)
	repaired_file.write(col_info)

	# convert to tab separated file, merge and write
	for orig_row in orig_reader:
		repaired_row = next(repaired_reader)
		merged = [None]*(len(orig_row)+len(repaired_row))
		merged[::2] = orig_row
		merged[1::2] = repaired_row
		repaired_file.write("\t".join(merged)+"\n")

	summary = open("{}/{}_.summary".format(identifier, repaired_attrib), 'w')
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
	#repaired_dir = "./Audit/audits/1489282159.55/"
	#repaired_dir = "./Audit/audits/1489282271.25/"
	repaired_dir = 
	attrib = ["Race", "Gender"]
	orig_file = "./Audit/test_data/adult.csv"
	for repaired_attrib in attrib:
		dir_ = "./Data"
		#repaired_data_retrieval(dir_, repaired_dir, repaired_attrib)
		retrieval_and_merger(orig_file, dir_, repaired_dir, repaired_attrib)