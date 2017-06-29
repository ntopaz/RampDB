from django.conf.urls import url

from . import views_db_status
from . import views_get_prot
from . import views_get_family
from . import views_blastall
from . import views_get_int
from . import views_get_ligand_int

urlpatterns = [
	url(r'db_status', views_db_status.get_status),
	url(r'calculate_result',views_blastall.get_result),
	url(r'interactions',views_get_int.get_int),
	url(r'ligand_int',views_get_ligand_int.get_lig_int),
	url(r'get_prot',views_get_prot.get_prot),
	url(r'get_family',views_get_family.get_family),
]
