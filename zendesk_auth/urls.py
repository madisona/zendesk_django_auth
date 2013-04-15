
from django.conf.urls import patterns, url


from zendesk_auth.views import ZendeskAuthorize

urlpatterns = patterns('',
    url(r'^zendesk-authorize/$', ZendeskAuthorize.as_view(), name="zendesk-authorize"),
)