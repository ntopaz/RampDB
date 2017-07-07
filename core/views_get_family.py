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
def my_family(family):
	final_dict = {}
	family_obj = Family.objects.get(name=family)
	final_dict[family] = {"name":family_obj.name,"name_short":family_obj.name_short,"pdb_id":family_obj.pdb_id,"gtp_id":family_obj.gtp_id,"status":family_obj.status}
	return final_dict

@api_view(['POST'])
def get_family(request):
	if request.method == 'POST':
		data = request.data
		print data
		contents = my_family(data["family"])
		response = JsonResponse(contents)
		return response


