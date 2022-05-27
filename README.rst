Zendesk Django Auth
===================

Allows your Django App to be used as an authentication platform for your Zendesk Account

Zendesk API Documentation
-------------------------
see `http://www.zendesk.com/support/api/remote-authentication` for ZenDesk Documentation.

This module is specifically for Zendesk API v1

Installation
------------
zendesk_auth version 0.0.3+ works with django 1.5 and above

    `pip install zendesk_django_auth`


Usage
-----
Using Zendesk SSO in your app is extremely simple...

in your settings.py, add 'zendesk_auth' to your `INSTALLED_APPS`

Then add the following two settings
    `ZENDESK_URL=https://your_domain.zendesk.com`
    `ZENDESK_TOKEN=you_zendesk_token`

Next, add this (or equivalent) to your urls.py:

    `url(r'', include('zendesk_auth.urls')),`

You'll need to setup your zendesk remote authentication settings to allow/use your zendesk_authorize view.

You're done! Now watch it work.

