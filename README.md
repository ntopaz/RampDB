# rampdb

To flush current DB content and repopulate:

```
(Flushes current DB content)

python manage.py flush

(Loads all proteins, interactions, ligands and pre-existing reference names into DB)
python load_all.py output.json references.json

(loads all text-mined sources into DB)

python upload_int_sources.py text_mining_sources.json

```
