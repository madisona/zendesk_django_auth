from django.conf.urls import url

from zendesk_auth.views import ZendeskAuthorize, ZendeskJWTAuthorize

urlpatterns = [
    url(
        r'^zendesk-authorize/$',
        ZendeskAuthorize.as_view(),
        name="zendesk-authorize"),
    url(
        r'^zendesk-jwt-authorize/$',
        ZendeskJWTAuthorize.as_view(),
        name="zendesk-jwt-authorize"),
]
