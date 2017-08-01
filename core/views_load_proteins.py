import sys,os,json
import pprint as pp
#from django.conf import settings
#settings.configure()
os.environ["DJANGO_SETTINGS_MODULE"] = "rampdb.settings"
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from django.shortcuts import render
from django.db import transaction
from models import *
# Create your views here.

@transaction.atomic
def load_db(data,family_data):
	source_obj, source_created = Source.objects.get_or_create(name="NCBI",url="www.ncbi.nlm.nih.gov")
	for family in family_data:
		family_name = family_data[family]["name"]
		pdb_id = family_data[family]["pdb_id"]
		gtp_id = family_data[family]["gtp_id"]
		status = family_data[family]["status"]
		family_obj, family_created = Family.objects.get_or_create(name= family_name, name_short=family, pdb_id = pdb_id, gtp_id = gtp_id, status = status)
		if family_name in data:
			for protein in sorted(data[family_name].keys()):
				organism_obj, organism_created = Organism.objects.update_or_create(name=data[family_name][protein]['org'])
				protein_obj, protein_created = Protein.objects.update_or_create(
								name = data[family_name][protein]['desc'],
								sequence = data[family_name][protein]['seq'],
								reference_id = protein,
								family = family_obj,
								organism = organism_obj,
								source = source_obj,
								)












def main():
	input_file = sys.argv[1]
	load_db(input_file)


if __name__ == "__main__":
	main()
