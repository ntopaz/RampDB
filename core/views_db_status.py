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
def db_status():
	results = OrderedDict()
	protein_count = Protein.objects.all().count()
	organism_count = Organism.objects.all().count()
	interaction_count = Interactions.objects.all().count()
	reference_count = Reference.objects.all().count()
	results = {'Proteins':protein_count,'Organisms':organism_count}
	return results





@api_view(['GET'])
def get_status(request):
	if request.method == 'GET':
		contents = db_status()
		response = JsonResponse(contents)
		return response


