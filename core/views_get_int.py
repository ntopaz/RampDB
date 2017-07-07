import sys,os,json
import pprint as pp
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
def db_int(family):
	final_dict = {}
	family_obj = Family.objects.get(name=family)
	r_interactions = Interactions.objects.filter(rampfamily_id=family_obj).select_related('gpcrfamily','ligand')
	g_interactions = Interactions.objects.filter(gpcrfamily_id=family_obj).select_related('rampfamily','ligand')
	final_dict['interactions'] = []
	if len(r_interactions) > 0:
		final_dict['ramp'] = ""
		for interaction in r_interactions:
			reference_set = {}
                        ref_objs = interaction.reference.all()
                        for ref_obj in ref_objs:
				reference_set[ref_obj.name] = ref_obj.url
			final_dict['interactions'].append({'status':interaction.status,'ref_length':len(reference_set),'references':reference_set,'name_short':interaction.name_short,'ligand_affinity':interaction.ligand_affinity,'ligand_binding_type':interaction.ligand_binding_type,'prot':interaction.gpcrfamily.name,'ligand':interaction.ligand.name, 'phenotype':interaction.phenotype})

	else:
		final_dict['gpcr'] = ""
		for interaction in g_interactions:
			reference_set = {}
                        ref_objs = interaction.reference.all()
                        for ref_obj in ref_objs:
				reference_set[ref_obj.name] = ref_obj.url
			final_dict['interactions'].append({'status':interaction.status,'ref_length':len(reference_set),'references':reference_set,'ligand_affinity':interaction.ligand_affinity,'ligand_binding_type':interaction.ligand_binding_type,'prot':interaction.rampfamily.name,'ligand':interaction.ligand.name, 'phenotype':interaction.phenotype})

	pp.pprint(final_dict)
	return final_dict

@api_view(['POST'])
def get_int(request):
	if request.method == 'POST':
		data = request.data
		print data
		contents = db_int(data['family'])
		response = JsonResponse(contents)
		return response


