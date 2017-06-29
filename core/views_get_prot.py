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
def my_prot():
	results = OrderedDict()
	family_info = Family.objects.all()
	for obj in family_info:
		if "modifying" in obj.name:
			my_type = "Ramp"
		else:
			my_type = "GPCR"
		if my_type not in results:
			results[my_type] = []
		results[my_type].append(obj.name)
	return results





@api_view(['GET'])
def get_prot(request):
	if request.method == 'GET':
		contents = my_prot()
		response = JsonResponse(contents)
		return response


