from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Family(models.Model):
	name = models.CharField(max_length=1000)
	name_short = models.CharField(max_length=500)
	pdb_id = models.CharField(max_length=500)
	gtp_id = models.CharField(max_length=200)
	status = models.CharField(max_length=500)

	def __unicode__(self):
		return self.name + " " + self.name_short

class Organism(models.Model):
	name = models.CharField(max_length=1000)


	def __unicode__(self):
		return self.name


class LoadingHandler(models.Model):
	name = models.CharField(max_length=100)
	handler = models.BooleanField(default=False)


class Reference(models.Model):
	name = models.CharField(max_length=1000)
	url = models.TextField()
	citation = models.TextField(null=True)


	def __unicode__(self):
		return self.name + " " + self.url

class Source(models.Model):
	name = models.CharField(max_length=100)
	url = models.TextField()


	def __unicode__(self):
		return self.name + " " + self.url

class Protein(models.Model):
	name = models.CharField(max_length=1000)
	sequence = models.TextField()
	reference_id = models.CharField(max_length=45)
	family = models.ForeignKey(Family)
	organism = models.ForeignKey(Organism)
	source = models.ForeignKey(Source)


	def __unicode__(self):
		return self.family.name + " " + self.name

class Ligand(models.Model):
	name = models.CharField(max_length=1000)
	inchi_key = models.CharField(max_length=200)
	chem_id = models.CharField(max_length=200)
	gtp_id = models.CharField(max_length=200)
	sequence = models.CharField(max_length=200, null=True)
	lig_type = models.CharField(max_length=50)
	synonyms = models.TextField(null=True)
	source = models.ForeignKey(Source)

	def __unicode__(self):
		return self.name + " " + self.name_short + " " + self.chem_id

class Interactions(models.Model):
	rampfamily = models.ForeignKey(Family, related_name="ramp_family")
	gpcrfamily = models.ForeignKey(Family, related_name="gpcr_family")
	ligand = models.ForeignKey(Ligand, null=True)
	ligand_affinity = models.CharField(max_length=200)
	ligand_binding_type = models.CharField(max_length=200)
	name_short = models.CharField(max_length=200)
	reference = models.ManyToManyField(Reference, null=True)
	phenotype = models.CharField(max_length=500)

	def __unicode__(self):
		return self.phenotype
