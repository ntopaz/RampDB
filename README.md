# About RampDB 

RampDB is a central repository for:

1. Exploring known information regarding Receptor Activity Modifying proteins (RAMPs), G-Protein Coupled Receptors (GPCRs) and associated ligands

2. Predicting potential RAMP interactions with your sequence or ligand

3. Visualizing currently known interactions between RAMPs, GPCRs and ligands

RampDB was developed using the following stack: 

```
* Framework: Django (Python)
* Database: MySQL
* Front End: HTML/CSS/AngularJS
* Server: Apache2.4
```

Flushes current DB content
```
python manage.py flush
```
Loads all proteins, interactions, ligands and pre-existing reference names into DB
```
python load_all.py output.json references.json 
```

Loads all text-mined sources into DB
```
python upload_int_sources.py text_mining_sources.json 
```


# Citation Information:

Topaz,N., Mojib,N., Chande,A.T. et al. RampDB: a web application and database for the exploration and prediction of receptor activity modifying protein interactions. Database (2017) Vol. 2017: article ID bax067; doi:10.1093/database/bax067
