import sys,os,json, subprocess, re, tempfile
from subprocess import *
from Bio import SeqIO
#from django.conf import settings
#settings.configure()
os.environ["DJANGO_SETTINGS_MODULE"] = "rampdb.settings"
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from django.shortcuts import render
from django.db import transaction
from models import *
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Create your views here.

@transaction.atomic
def hmm_query(query):
	profile_score = {}
	profile_quer_seq = {}
	profile_ref_seq = {}
	my_profiles = ['Ramp 1','Ramp 2','Ramp 3','CLR','CT']
	fp = tempfile.NamedTemporaryFile(suffix="",dir="",delete = False)
	for profile in my_profiles:
		fp.seek(0)
		fp.truncate()
               	subprocess.check_output(["hmmscan","-o",fp.name,
               	"core/profiles/%s" % profile,query],shell=False)
                best_domain = 0
                best_domain_score = 0
                rows = fp.read()
		print rows
                rows = re.split("\n",rows.rstrip())
                i=0
                for line in rows:
                        col = re.split('\s*',rows[i].strip())
                        rows[i]=(col)
                        i+=1
                if len(rows[16]) > 1:
                        profile_score[profile] = float(rows[16][1])
                        do_continue = True
                        num_domains = int(rows[16][7])
                        for i in range(0,num_domains):
                                if float(rows[23+i][2]) > float(best_domain_score):
                                        best_domain = rows[23+i][0]
                                        best_domain_score = rows[23+i][2]
                        for i in range(len(rows)):
                                if rows[i][0] == "==" and rows[i][2] == best_domain:
                                        profile_ref_seq[profile] = rows[i+1][2]
                                        if rows[i+6][0] == rows[i+1][0]:
                                                profile_ref_seq[profile] += rows[i+6][2]
                                        profile_quer_seq[profile] = rows[i+3][2]
                                        if rows[i+8][0] == rows[i+3][0]:
                                                profile_quer_seq[profile] += rows[i+8][2]
                else:
                        profile_score[profile] = 0

        max_value = 0

        for key in profile_score:
                if (max_value < profile_score[key]):
                        max_value = profile_score[key]
                        best_profile = key

        if max_value > 0:
                fp_quer = tempfile.NamedTemporaryFile(suffix="",dir="", delete = False)
                fp_quer.write(">query\n"+profile_quer_seq[best_profile])
                fp_quer.seek(0)
                fp_subj = tempfile.NamedTemporaryFile(suffix="",dir="", delete = False)
                fp_subj.write(">ref\n"+profile_ref_seq[best_profile])
                fp_subj.seek(0)
                results = subprocess.check_output(["blastp","-subject",
                fp_subj.name,"-outfmt","6","-query",fp_quer.name],shell=False)
                fp_quer.close()
                os.remove(fp_quer.name)
                fp_subj.close()
                os.remove(fp_subj.name)
                hmm_match(query,best_profile, max_value,results)
        else:
                no_results(query)
	fp.close()
	os.remove(fp.name)

def no_results(the_query):
        print "No results were found for the query: " + the_query 

def hmm_match(query,family,confidence,blast_results):
	for record in SeqIO.parse(query,"fasta"):
		quer_id = record.id
		quer_desc = record.description
	my_line = re.split('\s+', blast_results)
        my_ident = round(float(my_line[2]),1)
        queryName = quer_id
        confidenceScore = my_ident
	print confidenceScore, family, queryName 
