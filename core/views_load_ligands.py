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
	#data = json.loads(data)
	source_obj,source_created = Source.objects.update_or_create(name="GuideToPharmacology",url="http://www.guidetopharmacology.org")
	for complex in data:
		for ligand in data[complex]:
			if "[" in ligand:
				continue
			ligand_objs = Ligand.objects.filter(name=ligand)
			if len(ligand_objs) > 0:
				ligand_obj = ligand_objs[0]
				if data[complex][ligand]["chem_id"] != 0:
					if ligand_obj.chem_id == "0":
						ligand_obj.delete()
						ligand_obj, ligand_created = Ligand.objects.update_or_create(
							name = ligand,
							chem_id = data[complex][ligand]['chem_id'],
							gtp_id = data[complex][ligand]['gtp_id'],
							inchi_key = data[complex][ligand]['inchi_key'],
							sequence = data[complex][ligand]['sequence'],
							lig_type = data[complex][ligand]['ligand_type'],
							source = source_obj,
							synonyms = data[complex][ligand]["synonyms"],
							)	
						
			else:	
				ligand_obj, ligand_created = Ligand.objects.update_or_create(
								name = ligand,
								chem_id = data[complex][ligand]['chem_id'],
								gtp_id = data[complex][ligand]['gtp_id'],
								inchi_key = data[complex][ligand]['inchi_key'],
								sequence = data[complex][ligand]['sequence'],
								lig_type = data[complex][ligand]['ligand_type'],
								source = source_obj,
								synonyms = data[complex][ligand]["synonyms"],
								)








def main():
	input_file = sys.argv[1]
	load_db(input_file)


if __name__ == "__main__":
	main()
