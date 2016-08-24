import sys,os,json
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
def load_db(data):
	short_name = {'receptor activity modifying protein 1':'Ramp 1','receptor activity modifying protein 2':'Ramp 2','receptor activity modifying protein 3':'Ramp 3',
                        'receptor activity modifying protein 4':'Ramp 4','receptor activity modifying protein 5':'Ramp 5','calcitonin receptor':'CT','calcitonin receptor-like receptor':'CLR',
                        'vasoactive intestinal polypeptide receptor 1':'VIP 1'}

	source_obj, source_created = Source.objects.get_or_create(name="NCBI",url="www.ncbi.nlm.nih.gov")
	for family in sorted(data.keys()):
		family_obj, family_created = Family.objects.get_or_create(name = family, name_short=short_name[family])
		for protein in sorted(data[family].keys()):
			organism_obj, organism_created = Organism.objects.update_or_create(name=data[family][protein]['org'])
			protein_obj, protein_created = Protein.objects.update_or_create(
							name = data[family][protein]['desc'],
							sequence = data[family][protein]['seq'],
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
