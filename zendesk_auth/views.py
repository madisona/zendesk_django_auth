from hashlib import md5
import time

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode  # python 27

import uuid

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import RedirectView

import jwt


class ZendeskAuthorize(RedirectView):
    """
    View that is hit from zendesk, makes sure user is logged in, then passes
    information back to Zendesk to validate the authentication.
    """
    permanent = False

    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ZendeskAuthorize, self).dispatch(request, *args, **kwargs)

    def get_redirect_url(self, **kwargs):
        """
        Returns the url back to Zendesk after successful authentication.

        To see all the available parameters you can pass back to zendesk, read:
            http://www.zendesk.com/support/api/remote-authentication
            name, email, timestamp, and hash are required.
        """
        return r"{zendesk_url}/access/remoteauth/?{query_string}&hash={hashed_val}".format(  # noqa: E501
            zendesk_url=settings.ZENDESK_URL,
            query_string=self.create_query_string(),
            hashed_val=self.generate_hash())

    def get_zendesk_parameters(self):
        """
        returns a list of two element tuples for each variable zendesk
        accepts. The order of these are critically important as it will
        affect the hashed value being sent to Zendesk.
        """
        return [
            ("name", self.get_user_name()),
            ("email", self.get_email()),
            ("external_id", self.get_external_id()),
            ("organization", self.get_organization()),
            ("tags", self.get_tags()),
            ("remote_photo_url", self.get_remote_photo_url()),
            ("token", self.get_token()),
            ("timestamp", self.get_timestamp()),
        ]

    def create_query_string(self):
        """
        Returns a url encoded query string based on the parameters present.
        i.e. won't return a value when empty.
        """
        params = self.get_zendesk_parameters()
        return urlencode([p for p in params if p[1] and p[0] != 'token'])

    def generate_hash(self):
        """
        hash should be pipe delimited values for all items possible to send to
        zendesk. If any items are missing, that's ok, just leave them as
        empty string.
        """
        params = self.get_zendesk_parameters()
        input_string = "|".join([p[1] for p in params])
        return md5(input_string.encode('utf-8')).hexdigest()

    def get_user_name(self):
        """
        Required by Zendesk remote auth API.
        Uses username if real name is not defined.
        """
        u = self.request.user

        full_name = u"{} {}".format(u.first_name, u.last_name).strip()
        return full_name or u.username

    def get_email(self):
        """
        Required by Zendesk remote auth API.
        """
        return self.request.user.email

    def get_external_id(self):
        """
        Use when username is not the unique identifier for your users and
        might change. For standard Django Apps you'll want this to return the
        username because there's not a unique constraint on email by default.
        """
        return self.request.user.get_username()

    def get_organization(self):
        """
        Use when you want to tie the user to an Organization in Zendesk
        """
        return ''

    def get_tags(self):
        """
        Use when you want to add tags to the user's Zendesk Profile.
          tag1, tag2, tag3, etc...
        """
        return ''

    def get_remote_photo_url(self):
        """
        If you use this, the url must be publicly available and not behind
        any authentication.
        """
        return ''

    def get_token(self):
        return settings.ZENDESK_TOKEN

    def get_timestamp(self):
        return self.request.GET.get('timestamp', '')


class ZendeskJWTAuthorize(ZendeskAuthorize):
    """
    A view for working with the new mandatory JWT style of authentication.

    Zendesk is moving everyone to JWT Authentication:
    https://support.zendesk.com/entries/23675367-Setting-up-single-sign-on-with-JWT-JSON-Web-Token-

    """

    def get_redirect_url(self, **kwargs):
        """
        Returns the url back to Zendesk after successful authentication.

        To see all the available parameters you can pass back to zendesk, read:
            http://www.zendesk.com/support/api/remote-authentication
            name, email, timestamp, and hash are required.
        """
        return r"{zendesk_url}/access/jwt/?jwt={jwt_string}".format(
            zendesk_url=settings.ZENDESK_URL,
            jwt_string=self.get_jwt_string(), )

    def get_jwt_string(self):
        payload = {
            "iat": int(time.time()),  # issued at time
            "jti": str(uuid.uuid1()),  # web token id
            "email": self.get_email(),
            "name": self.get_user_name(),
            "external_id": self.get_external_id(),
            "organization": self.get_organization(),
            "tags": self.get_tags(),
            "remote_photo_url": self.get_remote_photo_url(),
        }
        clean_payload = {k: v for k, v in payload.items() if v}

        try:
            return jwt.encode(clean_payload, settings.ZENDESK_TOKEN).decode()
        except AttributeError:
            return jwt.encode(clean_payload, settings.ZENDESK_TOKEN)
