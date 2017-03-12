import os, sys
import datetime
import csv
from collections import defaultdict


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
	repaired_file.write("\t\t\t\t\t\t\t\t\t\tignore\tclass\n")

	# convert to tab separated file, merge and write
	for orig_row in orig_reader:
		repaired_row = next(repaired_reader)
		merged = [None]*(len(orig_row)+len(repaired_row))
		merged[::2] = orig_row
		merged[1::2] = repaired_row
		repaired_file.write("\t".join(merged)+"\n")

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

if __name__ == "__main__":
	#repaired_dir = "./Audit/audits/1487023139.65"
	#repaired_dir = "./Audit/audits/1487655656.76/"
	#repaired_dir = "./Audit/audits/1488339786.6" 
	#repaired_dir = "./Audit/audits/1489282159.55/"
	repaired_dir = "./Audit/audits/1489282271.25/"
	attrib = ["Race", "Gender"]
	orig_file = "./Data/bonus_indirect.csv"
	for repaired_attrib in attrib:
		dir_ = "./Data".format(repaired_attrib)
		#repaired_data_retrieval(dir_, repaired_dir, repaired_attrib)
		retrieval_and_merger(orig_file, dir_, repaired_dir, repaired_attrib)