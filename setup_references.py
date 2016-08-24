import os, sys, json
import pprint as pp
from core.views_load_ref import load_ref

def load_reference():
	reference = {}
	list = []
	attributes = {'url':'www.ncbi.nlm.nih.gov/pubmed/12529938','citation':'Usdin TB, Bonner TI, Hoare SR. The parathyroid hormone 2 (PTH2) receptor. Receptors Channels. 2002;8(3-4):211-8. Review. Pubmed PMID: 12529938.'}
	reference['The parathyroid hormone 2 (PTH2) receptor'] = attributes
	attributes = {'url':'www.ncbi.nlm.nih.gov/pubmed/21439408','citation':'Umetsu Y, Tenno T, Goda N, Shirakawa M, Ikegami T, Hiroaki H (May 2011). "Structural difference of vasoactive intestinal peptide in two distinct membrane-mimicking environments". Biochimica Et Biophysica Acta 1814 (5): 724-30.'}
	reference['Structural difference of vasoactive intestinal peptide in two distinct membrane-mimicking evironments'] = attributes
	attributes = {'url':'http://www.guidetopharmacology.org/GRAC/FamilyIntroductionForward?familyId=11.','citation':'IUPHAR/BPS Guide to PHARMACOLOGY, http://www.guidetopharmacology.org/GRAC/FamilyIntroductionForward?familyId=11.'}
	reference['Calcitonin Receptors: Introduction'] = attributes
	attributes = {'url':'www.ncbi.nlm.nih.gov/pubmed/15494035','citation':'Hay DL, Christopoulos G, Christopoulos A, Sexton PM. Amylin receptors: molecular composition and pharmacology. Biochem Soc Trans. 2004;32:865-07.'}
	reference['Amylin receptors: molecular composition and pharmacology'] = attributes
	attributes = {'url':'www.ncbi.nlm.nih.gov/pubmed/16888151','citation':'Sexton PM, Morfis M, Tilakaratne N, Hay DL, Udawela M, Christopoulos G, Christopoulos A. Complexing receptor pharmacology: modulation of family B G protein-coupled receptor function by RAMPs. Ann N Y Acad Sci. 2006;1070:90-104.'}
	reference['Complexing receptor pharmacology: modulation of family B G protein-coupled receptor function by RAMPs'] = attributes
	load_ref(json.dumps(reference))

def main():
	load_reference()

if __name__ == "__main__":
	main()
