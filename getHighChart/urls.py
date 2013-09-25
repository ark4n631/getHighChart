from django.conf.urls import patterns, include, url
from django.conf import settings
from getHigh import views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^getGraph',views.getGraph,name='getGraph'),
	url(r'^$',views.index,name='index'),
	# Examples:
	# url(r'^$', 'getHighChart.views.home', name='home'),
	# url(r'^getHighChart/', include('getHighChart.foo.urls')),

	# Uncomment the admin/doc line below to enable admin documentation:
	# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	# url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += patterns('',
	url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
	url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)
