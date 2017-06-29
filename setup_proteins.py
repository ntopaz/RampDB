import sys, os, json
from core.views_load_proteins import *

def load_proteins(input_file,family_data):
	with open(input_file) as f:
		my_dict=json.load(f)

	load_db(my_dict,family_data)


def main():
	input_file = sys.argv[1]
	load_proteins(input_file)


if __name__=="__main__":
	main()
