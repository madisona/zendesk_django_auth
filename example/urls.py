import django

if django.get_version() >= '2.0.0':
    from django.urls import re_path as url
    from django.urls import include
else:
    from django.conf.urls import url
    from django.conf.urls import include

from django.contrib import admin
from zendesk_auth import urls
admin.autodiscover()

urlpatterns = [
    url(r'', include(urls.urlpatterns)),

    url(r'^admin/', admin.site.urls),
]
