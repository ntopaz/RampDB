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
		int_objs = Interactions.objects.filter(name_short=int_name_short)
		for int_obj in int_objs:
			for ref in data[int_name_short]:
				if Reference.objects.filter(name=ref).exists():
					ref_obj = Reference.objects.get(name=ref)
				else:
					continue
				int_obj.reference.add(ref_obj)
				int_obj.save()











def main():
	input_file = sys.argv[1]
	load_db(input_file)


if __name__ == "__main__":
	main()
