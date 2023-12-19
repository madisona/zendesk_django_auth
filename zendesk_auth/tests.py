#! /usr/bin/env python
# -*- coding: utf8 -*-


try:
    from unittest import mock
except ImportError:
    import mock  # python27

from django.contrib.auth.models import User
from django.urls import reverse
from django import test
from django.conf import settings
import jwt

from zendesk_auth import views

TEST_ZENDESK_URL = "http://mycompany.zendesk.com"
TEST_ZENDESK_TOKEN = "my-zendesk-token-for-tests"


def create_user(username="test",
                email="test@example.com",
                password='pswd',
                **kwargs):
    u = User(username=username, email=email, **kwargs)
    u.set_password(password)
    u.save()
    return u


@test.utils.override_settings(
    ZENDESK_URL=TEST_ZENDESK_URL, ZENDESK_TOKEN=TEST_ZENDESK_TOKEN)
class AuthorizeJWTTests(test.TestCase):
    urls = 'zendesk_auth.urls'

    def setUp(self):
        self.authorize_url = reverse('zendesk-jwt-authorize')
        self.sut = views.ZendeskJWTAuthorize

    def test_redirects_to_login_when_not_logged_in(self):
        response = self.client.get(self.authorize_url)
        self.assertEqual(302, response.status_code)
        self.assertEqual(True, response['Location'].endswith(
            r'{}?next={}'.format(settings.LOGIN_URL, self.authorize_url)))

    def test_get_user_name_returns_first_name_when_thats_all_thats_present(
            self):
        u = User(first_name=" Joe ")
        request = test.RequestFactory().get("/")
        request.user = u

        view = views.ZendeskJWTAuthorize(request=request)
        self.assertEqual("Joe", view.get_user_name())

    def test_get_user_name_returns_last_name_when_thats_all_thats_present(
            self):
        u = User(last_name=" Tester ")
        request = test.RequestFactory().get("/")
        request.user = u

        view = views.ZendeskJWTAuthorize(request=request)
        self.assertEqual("Tester", view.get_user_name())

    def test_get_user_name_returns_full_name_when_present(self):
        u = User(first_name=" Joe", last_name="Tester ")
        request = test.RequestFactory().get("/")
        request.user = u

        view = views.ZendeskJWTAuthorize(request=request)
        self.assertEqual("Joe Tester", view.get_user_name())

    def test_get_user_name_returns_username_when_no_first_or_last_name(self):
        u = User(username="joetester23")
        request = test.RequestFactory().get("/")
        request.user = u

        view = views.ZendeskJWTAuthorize(request=request)
        self.assertEqual(u.get_username(), view.get_user_name())

    def test_get_email_returns_user_email(self):
        u = create_user(username="joe", email="joe@example.com")
        request = test.RequestFactory().get("/")
        request.user = u

        view = views.ZendeskJWTAuthorize(request=request)
        self.assertEqual(u.email, view.get_email())

    def test_get_external_id_returns_username(self):
        u = create_user(username="joe", password="pswd")
        request = test.RequestFactory().get("/")
        request.user = u

        view = views.ZendeskJWTAuthorize(request=request)
        self.assertEqual(u.get_username(), view.get_external_id())

    def test_get_organization_returns_empty_string_by_default(self):
        view = views.ZendeskJWTAuthorize()
        self.assertEqual('', view.get_organization())

    def test_get_tags_returns_empty_string_by_default(self):
        view = views.ZendeskJWTAuthorize()
        self.assertEqual('', view.get_tags())

    def test_get_remote_photo_returns_empty_string_by_default(self):
        view = views.ZendeskJWTAuthorize()
        self.assertEqual('', view.get_remote_photo_url())

    def test_get_token_returns_zendesk_token_from_settings(self):
        view = views.ZendeskJWTAuthorize()

        with self.settings(ZENDESK_TOKEN="my-token-from-settings"):
            token = view.get_token()
        self.assertEqual("my-token-from-settings", token)

    def test_get_timestamp_returns_timestamp_from_get_parameter(self):
        request = test.RequestFactory().get("/", {"timestamp": 500})
        view = views.ZendeskJWTAuthorize(request=request)

        timestamp = view.get_timestamp()
        self.assertEqual(u'500', timestamp)

    def test_get_timestamp_returns_empty_string_when_not_in_get_parameter(
            self):
        request = test.RequestFactory().get("/", {})
        view = views.ZendeskJWTAuthorize(request=request)

        timestamp = view.get_timestamp()
        self.assertEqual(u'', timestamp)

    def test_get_request_responds_success_with_correct_template(self):
        create_user("test",  password="pswd")

        self.client.login(username='test', password='pswd')
        response = self.client.get("/zendesk-jwt-authorize/")

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, "zendesk_auth/zendesk_auth_passthrough.html")

    @mock.patch('zendesk_auth.views.ZendeskJWTAuthorize.get_jwt_string')
    def test_get_request_contains_jwt_in_hidden_field(self, get_jwt_string):
        get_jwt_string.return_value = "abcd"
        create_user("test",  password="pswd")

        self.client.login(username='test', password='pswd')
        response = self.client.get("/zendesk-jwt-authorize/")

        self.assertContains(response, '<input id="jwtInput" type="hidden" name="jwt" value="abcd" />', count=1)

    def test_get_request_contains_form_to_post_to_zendesk(self):
        create_user("test",  password="pswd")

        self.client.login(username='test', password='pswd')
        response = self.client.get("/zendesk-jwt-authorize/")
        expected_string = '<form id="jwtForm" method="post" action="{}/access/jwt">'.format(settings.ZENDESK_URL)
        self.assertContains(response, expected_string, count=1)

    @mock.patch('zendesk_auth.views.time')
    @mock.patch('zendesk_auth.views.uuid')
    @mock.patch.object(views.ZendeskJWTAuthorize, 'get_email')
    @mock.patch.object(views.ZendeskJWTAuthorize, 'get_user_name')
    @mock.patch.object(views.ZendeskJWTAuthorize, 'get_external_id')
    @mock.patch.object(views.ZendeskJWTAuthorize, 'get_organization')
    @mock.patch.object(views.ZendeskJWTAuthorize, 'get_tags')
    @mock.patch.object(views.ZendeskJWTAuthorize, 'get_remote_photo_url')
    def test_get_jwt_string_returns_encoded_string(
            self, get_photo, get_tags, get_organization, get_id, get_name,
            get_email, uuid, time):
        time.time.return_value = 123456
        uuid.uuid1.return_value = "abcd1234"
        get_email.return_value = "test@example.com"
        get_name.return_value = "Tester McGee"
        get_id.return_value = "TST1234"
        get_organization.return_value = "Acme, Inc."
        get_tags.return_value = ["foo", "bar"]
        get_photo.return_value = "http://s3.amazonaws.com/rapgenius/filepicker%2FvCleswcKTpuRXKptjOPo_kitten.jpg"  # noqa: E501

        view = self.sut()
        with mock.patch.object(jwt, "encode") as encode:
            jwt_string = view.get_jwt_string()

        payload = {
            "iat": time.time.return_value,
            "jti": uuid.uuid1.return_value,
            "email": get_email.return_value,
            "name": get_name.return_value,
            "external_id": get_id.return_value,
            "organization": get_organization.return_value,
            "tags": get_tags.return_value,
            "remote_photo_url": get_photo.return_value,
        }
        encode.assert_called_once_with(payload, settings.ZENDESK_TOKEN)
        self.assert_jwt_string(encode, jwt_string)
        get_email.assert_called_once_with()
        get_name.assert_called_once_with()
        get_id.assert_called_once_with()
        get_organization.assert_called_once_with()
        get_tags.assert_called_once_with()
        get_photo.assert_called_once_with()
        time.time.assert_called_once_with()
        uuid.uuid1.assert_called_once_with()

    @mock.patch('zendesk_auth.views.time')
    @mock.patch('zendesk_auth.views.uuid')
    @mock.patch.object(views.ZendeskJWTAuthorize, 'get_email')
    @mock.patch.object(views.ZendeskJWTAuthorize, 'get_user_name')
    @mock.patch.object(views.ZendeskJWTAuthorize, 'get_external_id')
    @mock.patch.object(views.ZendeskJWTAuthorize, 'get_organization')
    @mock.patch.object(views.ZendeskJWTAuthorize, 'get_tags')
    @mock.patch.object(views.ZendeskJWTAuthorize, 'get_remote_photo_url')
    def test_only_encodes_parameters_that_have_a_value(
            self, get_photo, get_tags, get_organization, get_id, get_name,
            get_email, uuid, time):
        time.time.return_value = 123456
        uuid.uuid1.return_value = "abcd1234"
        get_email.return_value = "test@example.com"
        get_name.return_value = "Tester McGee"
        get_id.return_value = ""
        get_organization.return_value = ""
        get_tags.return_value = ["foo", "bar"]
        get_photo.return_value = ""

        view = self.sut()
        with mock.patch.object(jwt, "encode") as encode:
            jwt_string = view.get_jwt_string()

        expected_payload = {
            "iat": time.time.return_value,
            "jti": uuid.uuid1.return_value,
            "email": get_email.return_value,
            "name": get_name.return_value,
            "tags": get_tags.return_value,
        }
        encode.assert_called_once_with(expected_payload,
                                       settings.ZENDESK_TOKEN)
        self.assert_jwt_string(encode, jwt_string)
        get_email.assert_called_once_with()
        get_name.assert_called_once_with()
        get_id.assert_called_once_with()
        get_organization.assert_called_once_with()
        get_tags.assert_called_once_with()
        get_photo.assert_called_once_with()
        time.time.assert_called_once_with()
        uuid.uuid1.assert_called_once_with()

    @mock.patch('zendesk_auth.views.time')
    @mock.patch('zendesk_auth.views.uuid')
    @mock.patch.object(views.ZendeskJWTAuthorize, 'get_email')
    @mock.patch.object(views.ZendeskJWTAuthorize, 'get_user_name')
    @mock.patch.object(views.ZendeskJWTAuthorize, 'get_external_id')
    @mock.patch.object(views.ZendeskJWTAuthorize, 'get_organization')
    @mock.patch.object(views.ZendeskJWTAuthorize, 'get_tags')
    @mock.patch.object(views.ZendeskJWTAuthorize, 'get_remote_photo_url')
    def test_jwt_string_is_returned_as_str_not_bytes(
            self, get_photo, get_tags, get_organization, get_id, get_name,
            get_email, uuid, time):
        time.time.return_value = 123456
        uuid.uuid1.return_value = "abcd1234"
        get_email.return_value = "test@example.com"
        get_name.return_value = "Tester McGee"
        get_id.return_value = ""
        get_organization.return_value = ""
        get_tags.return_value = ["foo", "bar"]
        get_photo.return_value = ""

        view = self.sut()
        jwt_string = view.get_jwt_string()
        try:
            self.assertTrue(isinstance(jwt_string, unicode))
        except NameError:
            self.assertTrue(isinstance(jwt_string, str))

    def assert_jwt_string(self, encode, jwt_string):
        try:
            expected = encode.return_value.decode()
        except AttributeError:
            expected = encode.return_value
        self.assertEqual(expected, jwt_string)
