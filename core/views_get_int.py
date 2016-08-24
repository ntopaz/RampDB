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
def db_int(family):
	final_dict = {}
	family_obj = Family.objects.get(name=family)
	r_interactions = Interactions.objects.filter(rampfamily_id=family_obj).select_related('gpcrfamily','ligand')
	g_interactions = Interactions.objects.filter(gpcrfamily_id=family_obj).select_related('rampfamily','ligand')
	if len(r_interactions) > 0:
		for interaction in r_interactions:
			final_dict[interaction.phenotype] = {'function':interaction.function,'gpcr':interaction.gpcrfamily.name,'ligand':interaction.ligand.name}
	else:
		for interaction in g_interactions:
			final_dict[interaction.phenotype] = {'function':interaction.function,'ramp':interaction.rampfamily.name,'ligand':interaction.ligand.name}

	return final_dict

@api_view(['POST'])
def get_int(request):
	if request.method == 'POST':
		data = request.data
		print data
		contents = db_int(data['family'])
		response = JsonResponse(contents)
		return response


