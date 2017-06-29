### Script to use RampDB to grab all pubmed publications with stored interactions and identify those which contain evidence
### of interaction and produce JSON output for DB storage

import os, json
from Bio import Entrez
os.environ["DJANGO_SETTINGS_MODULE"] = "rampdb.settings"
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from core.models import *
Entrez.email = "ntopaz@spsu.edu"

### variables
int_short = {}

### keyword checks
#strong_checks = ['interacts with','binds with','complex with','complexes with']
weak_checks = ['interacts','interaction','binding','binds','complex','interact']

### function to scan each line of matched literature for keywords
def check_text(text, ramp, gpcr):
	for line in text:
#		for s_check in strong_checks:
#			my_string = ramp +" " + s_check + " " + gpcr
#			try:
#				if my_string in line:
#					return True
#			except:
#				pass
		for w_check in weak_checks:
			if w_check in line:
				return True
	return False


### grab interactions from DB and setup dictionary
interaction_objs = Interactions.objects.all()
for int_obj in interaction_objs:
	int_short[int_obj.name_short] = {'ramp_short':int_obj.rampfamily.name_short,'gpcr_short':int_obj.gpcrfamily.name_short,
						'ramp':int_obj.rampfamily.name, 'gpcr':int_obj.gpcrfamily.name,
							'phenotype':int_obj.phenotype,'confirmed':[]}

### for each key in dict, query NCBI for matching literature and call check_text() for matching keywords
for key in sorted(int_short.keys()):
	ramp_short_term = int_short[key]['ramp_short'].replace(" ","").strip()
	gpcr_short_term = int_short[key]['gpcr_short'].strip()
	ramp = int_short[key]['ramp'].strip()
	gpcr = int_short[key]['gpcr'].strip()
	handle_short = Entrez.esearch(db="pubmed", term=ramp_short_term + " " + gpcr_short_term, retmax="100000")
	handle_long = Entrez.esearch(db="pubmed", term=ramp + " " + gpcr, retmax="100000")
	short_record = Entrez.read(handle_short)
	long_record = Entrez.read(handle_long)
	my_set = set(short_record["IdList"] + long_record["IdList"])
	for potential_id in my_set:
		try:
			fetch_handle = Entrez.efetch(db="pubmed", id=potential_id, rettype="gb", retmode="text")
			text = fetch_handle.readlines()
			add_to_list = check_text(text,ramp_short_term,gpcr_short_term)
			if add_to_list:
				int_short[key]['confirmed'].append(potential_id)
		except:
			pass


### convert dict to json
with open ("text_mining_sources_loose.json","w") as f:
	json.dump(int_short, f)


