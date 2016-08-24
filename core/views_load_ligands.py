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
def load_ligands(data):
	data = json.loads(data)
	source_obj,source_created = Source.objects.update_or_create(name="PubChem",url="pubchem.ncbi.nlm.nih.gov")
	for ligand in sorted(data.keys()):
		ligand_obj, ligand_created = Ligand.objects.update_or_create(
						name = ligand,
						name_short = data[ligand]['name_short'],
						chem_id = data[ligand]['chem_id'],
						inchi_key = data[ligand]['inchi_key'],
						source = source_obj,
						)








def main():
	input_file = sys.argv[1]
	load_db(input_file)


if __name__ == "__main__":
	main()
