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
	if len(r_interactions) > 0:
		final_dict['interactions'] = {}
		final_dict['ramp'] = ""
		for interaction in r_interactions:
			final_dict['interactions'][interaction.phenotype] = {'function':interaction.function,'prot':interaction.gpcrfamily.name,'ligand':interaction.ligand.name, 'references': {}}
			ref_objs = Interactions_Reference.objects.filter(interactions_id=interaction).select_related('reference')
			for ref_obj in ref_objs:
				final_dict['interactions'][interaction.phenotype]['references']['name'] = ref_obj.reference.name
				final_dict['interactions'][interaction.phenotype]['references']['url'] = ref_obj.reference.url
	else:
		final_dict['interactions'] = {}
		final_dict['gpcr'] = ""
		for interaction in g_interactions:
			final_dict['interactions'][interaction.phenotype] = {'function':interaction.function,'prot':interaction.rampfamily.name,'ligand':interaction.ligand.name, 'references': {}}
			ref_objs = Interactions_Reference.objects.filter(interactions_id=interaction).select_related('reference')
			for ref_obj in ref_objs:
				final_dict['interactions'][interaction.phenotype]['references']['name'] = ref_obj.reference.name
				final_dict['interactions'][interaction.phenotype]['references']['url'] = ref_obj.reference.url

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


