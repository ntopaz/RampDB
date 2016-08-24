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
def load_ref(data):
	data = json.loads(data)
	for ref in sorted(data.keys()):
		ref_obj, ref_created = Reference.objects.update_or_create(
						name = ref,
						url = data[ref]['url'],
						citation = data[ref]['citation'],
						)








def main():
	input_file = sys.argv[1]
	load_db(input_file)


if __name__ == "__main__":
	main()
