import os, sys
import datetime
import csv
from collections import defaultdict


def repaired_data_retrieval(dir_, repaired_dir, repaired_attrib):
	repaired_files = []

	t = datetime.datetime.now()
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
	repaired_dir = "./Audit/audits/1489282159.55/"
	#repaired_dir = "./Audit/audits/1489282271.25/"
	attrib = ["Race", "Gender"]
	for repaired_attrib in attrib:
		dir_ = "./Data/Bonus_Repaired_{}".format(repaired_attrib)
		repaired_data_retrieval(dir_, repaired_dir, repaired_attrib)