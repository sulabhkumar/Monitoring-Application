from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.views.defaults import page_not_found

handler404 = 'SharedApps_Application.views.handler404'
handler500 = 'SharedApps_Application.views.handler500'

urlpatterns=[
	path('',views.index, name = 'index'),
	path('basic',views.basic, name = 'basic'),
	path('saveIncident',views.saveIncident, name = 'saveIncident'),
	path('DisplayIncident',views.DisplayIncident, name = 'DisplayIncident'),
	
	
	url(r'^list/$', views.list, name='list'),
	url(r'^list/create$', views.certificate_create, name='certificate_create'),
	url(r'^list/(?P<id>\d+)/update$', views.certificate_update, name='certificate_update'),
	url(r'^list/(?P<id>\d+)/delete$', views.certificate_delete, name='certificate_delete'),

	url(r'^service_account/$', views.service_account, name='service_account'),
	url(r'^service_account/create$', views.service_account_create, name='service_account_create'),
	url(r'^service_account/(?P<id>\d+)/update$', views.service_account_update, name='service_account_update'),
	url(r'^service_account/(?P<id>\d+)/delete$', views.service_account_delete, name='service_account_delete'),

	path('',views.index, name = 'index'),
	path('displayLogs',views.displayLogs, name = 'displayLogs'),
	path('upload',views.upload, name = 'upload'),
	path('download/<int:pk>/', views.download, name='download'),


]
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)