from django.conf.urls import url

from . import views_db_status
from . import views_blastall
from . import views_get_int

urlpatterns = [
	url(r'db_status', views_db_status.get_status),
	url(r'calculate_result',views_blastall.get_result),
	url(r'interactions',views_get_int.get_int),
]
