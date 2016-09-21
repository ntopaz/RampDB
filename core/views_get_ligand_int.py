import sys,os,json
from collections import OrderedDict
#from django.conf import settings
#settings.configure()
os.environ["DJANGO_SETTINGS_MODULE"] = "rampdb.settings"
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from django.shortcuts import render
from django.db import transaction
from rest_framework.decorators import api_view
from django.http import JsonResponse
from models import *
# Create your views here.

@transaction.atomic
def db_int(cid):
	final_dict = {}
	ligand_obj = Ligand.objects.get(chem_id=cid)
	interaction_objs = Interactions.objects.filter(ligand_id=ligand_obj).select_related("gpcrfamily","rampfamily")
	for int_obj in interaction_objs:
		final_dict[int_obj.name_short] = {"name": int_obj.phenotype,"function":int_obj.function,"gpcr":int_obj.gpcrfamily.name,"ramp":int_obj.rampfamily.name, "references": {}}
		ref_objs = int_obj.reference.all()
		for ref_obj in ref_objs:
			final_dict[int_obj.name_short]['references'][ref_obj.name] = ref_obj.url
		final_dict[int_obj.name_short]['ref_length'] = len(ref_objs)
	return final_dict


@api_view(['POST'])
def get_lig_int(request):
	if request.method == 'POST':
		data = request.data
		print data
		contents = db_int(data['ligand_cid'])
		response = JsonResponse(contents)
		return response


