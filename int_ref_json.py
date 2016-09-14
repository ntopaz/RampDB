import os, sys, json
import pprint as pp
from core.views_int_ref_json import generate_json



def main():
	output = generate_json()
	pp.pprint(output) 

if __name__=="__main__":
	main()
