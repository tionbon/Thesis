# Thesis

The main file make_rules.py uses Orange's CN2-SD learner to produce rules for a given file

The file data_retrieval.py takes the Audited csv files and formated them into tab separated files that are required by Orange

The file make_data.py creates a synthetic datset without indirect discrimination

The file make_proxy.py creates a synthetic dataset where education is used as the proxy variable for discrimination 

(highschool educaion status has low chance of having a positive label and black men overwheliming are highschool educated)

rules.py is my modified version of Orange's rule induction script
