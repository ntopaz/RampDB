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
def load_db(data):
	for int_name_short in data.keys():
		int_obj = Interactions.objects.get(name_short=int_name_short)
		for ref in data[int_name_short]:
			ref_obj = Reference.objects.get(name=ref)
			int_obj.reference.add(ref_obj)
			int_obj.save()











def main():
	input_file = sys.argv[1]
	load_db(input_file)


if __name__ == "__main__":
	main()
