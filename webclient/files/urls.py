from django.conf.urls.defaults import *

urlpatterns = patterns('barabas.views',
    (r'^create/$', 'createFile'),
    (r'^tags/([a-zA-Z0-9 ]*)/$', 'viewFiles'),
    (r'^(\d*)/tag/$', 'tag'),
    (r'^(\d*)/untag/$', 'untag'),
    (r'^(\d*)/store/$', 'uploadVersion'),
    (r'^(\d*)/(\d*)/download/$', 'download'),
    (r'^(\d*)/$', 'viewFile'),
)
