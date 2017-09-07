from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
	url(r'^get/(?P<uuid>[\w-]+)/$', views.getFileViaToken, name="get_file"),
	url(r'^getfile/(?P<id>[\w-]+)/$', views.getFileAdmin, name="get_file_admin"),
	url(r'^posttime/$', views.posttime, name="make_fileviewing"),
	url(r'^downloadfile/(?P<id>[\w-]+)/$', views.downloadfile, name="download_file"),
	url(r'^(?P<slug>[\w-]+)/$', views.displayfile, name="display_file"),	
]
