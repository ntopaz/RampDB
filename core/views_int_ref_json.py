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
def generate_json():
	final_dict = {}
	interactions = Interactions.objects.all()
	references = Reference.objects.all()
	for int_obj in interactions:
		final_dict[int_obj.name_short] = []
		ref_objs = int_obj.reference.all()
		for ref_obj in ref_objs:
			final_dict[int_obj.name_short].append(ref_obj.name)


	with open("references.json","w") as f:
		json.dump(final_dict,f)

	return final_dict



