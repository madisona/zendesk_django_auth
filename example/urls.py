from django.conf.urls import include, url

from django.contrib import admin
from zendesk_auth import urls
admin.autodiscover()

urlpatterns = [
    url(r'', include(urls.urlpatterns)),

    url(r'^admin/', admin.site.urls),
]
