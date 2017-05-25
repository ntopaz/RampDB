import os,json,sys
import pprint as pp
from Bio import Entrez
os.environ["DJANGO_SETTINGS_MODULE"] = "rampdb.settings"
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from core.models import *
from django.db import transaction
Entrez.email = "ntopaz@spsu.edu"

@transaction.atomic
def main():
	ref_json = sys.argv[1]
	with open(ref_json) as f:
        	my_data = json.load(f)
	
	for key in my_data.keys():
		int_obj = Interactions.objects.get(name_short=key)
		my_sources = ",".join([str(x) for x in my_data[key]['confirmed']])
		if my_sources:
			handle = Entrez.efetch(db="pubmed", id=my_sources, rettype="json")
			record = Entrez.read(handle)
			for item in record:
				for sub_item in record[item]:
					if "MedlineCitation" in sub_item:
						url = "https://www.ncbi.nlm.nih.gov/pubmed/{}".format(sub_item['MedlineCitation']['PMID'])
						title = sub_item['MedlineCitation']['Article']['ArticleTitle']
				try:
					if Reference.objects.filter(name=title).exists():
						continue
					else:
						ref_obj = Reference(name=title,url=url)
						ref_obj.save()
					int_obj.reference.add(ref_obj)
					int_obj.save()
				except:
					continue


if __name__=="__main__":
	main()
