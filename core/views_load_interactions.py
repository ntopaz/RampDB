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
def load_interactions(data):
	data = json.loads(data)
	for interaction in sorted(data.keys()):
		ramp_fam = Family.objects.get(name=data[interaction]['rampfamily'])
		gpcr_fam = Family.objects.get(name=data[interaction]['gpcrfamily'])
		for ligand in data[interaction]["ligands"]:
			lig_seq = data[interaction]["ligands"][ligand]["sequence"]
			ligand_obj = Ligand.objects.get(name=ligand,sequence=lig_seq)
			interact_obj, interact_created = Interactions.objects.update_or_create(
							phenotype = data[interaction]['name'],
							rampfamily = ramp_fam,
							gpcrfamily = gpcr_fam,
							ligand = ligand_obj,
							ligand_affinity = str(data[interaction]["ligands"][ligand]["affinity"]),
							ligand_binding_type = data[interaction]["ligands"][ligand]["binding_type"],
							name_short = data[interaction]['name_short'],
							)








def main():
	input_file = sys.argv[1]
	load_db(input_file)


if __name__ == "__main__":
	main()
