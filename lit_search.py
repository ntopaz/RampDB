### Script to use RampDB to grab all pubmed publications with stored interactions and identify those which contain evidence
### of interaction and produce JSON output for DB storage

import os
from Bio import Entrez
os.environ["DJANGO_SETTINGS_MODULE"] = "rampdb.settings"
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from core.models import *
Entrez.email = "ntopaz@spsu.edu"

int_short = {}

strong_checks = ['interacts with','binds with','complex with','complexes with']
weak_checks = ['interacts','interaction','binding','binds','complex']


def check_text(text, ramp, gpcr):
	for line in text:
		#print line
		for s_check in strong_checks:
			my_string = ramp +" " + s_check + " " + gpcr
	#		print my_string
			try:
				if my_string in line:
					return True
			except:
				pass
		for w_check in weak_checks:
			if w_check in line:
				return True
	return False


interaction_objs = Interactions.objects.all()
for int_obj in interaction_objs:
	int_short[int_obj.name_short] = {'ramp_short':int_obj.rampfamily.name_short,'gpcr_short':int_obj.gpcrfamily.name_short,
						'ramp':int_obj.rampfamily.name, 'gpcr':int_obj.gpcrfamily.name,
							'phenotype':int_obj.phenotype,'confirmed':[]}


for key in sorted(int_short.keys()):
	ramp_short_term = int_short[key]['ramp_short'].replace(" ","").strip()
	gpcr_short_term = int_short[key]['gpcr_short'].strip()
	handle_short = Entrez.esearch(db="pubmed", term=ramp_short_term + " " + gpcr_short_term, retmax="100000")
#	handle_long = Entrez.esearch(db="pubmed", term=ramp, retmax="100000")
	short_record = Entrez.read(handle_short)
	for potential_id in short_record["IdList"]:
		try:
			fetch_handle = Entrez.efetch(db="pubmed", id=potential_id, rettype="gb", retmode="text")
			text = fetch_handle.readlines()
			add_to_list = check_text(text,ramp_short_term,gpcr_short_term)
			if add_to_list:
				print potential_id
				int_short[key]['confirmed'].append(potential_id)
		except:
			pass
#for line in text:
#	print line

