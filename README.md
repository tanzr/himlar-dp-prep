# himlar-dp-prep

Himlar onboarding page for Dataporten users.

When a user logs in to this page using Dataporten, a personal group
and project are created and access granted to it for the user.

From then on, the user can log in direct to the OpenStack dashboard.

The page is a tiny Pyramid web application using Authomatic for OpenID
Connect logon. It has been tested with Python 2.7.10 and 3.5.1.

### Registration in Dataporten

The application must be registered as a client in Dataporten. See
the [Dataporten documentation](http://feideconnect.no/docs/authorization/#register). The redirect URL
should be the application's _/login_, and the scopes _profile_, _userid_,
_email_ and _openid_ should be accepted.

For testing and development, a client has already been registered with
the following parameters: 
<dl>
<dt>Client ID<dt>
<dd><em>ad604e3b-30cf-4b6a-9c4f-69483c316a02</em></dd>
<dt>Client Secret<dt>
<dd><em>f2de303a-3e70-4141-b0ac-03207ae42e54</em></dd>
<dt>Redirect URI<dt>
<dd><em>http://localhost:6543/login</em></dd>
</dl>

The OpenStack dashboard also has to be registered in Dataporten. See
the [himlar-connect documentation](https://github.com/norcams/himlar-connect#to-register-the-dev-env-horizonkeystone-in-connect).

###  configuration

All parameters are entered in the `app:main` section of the
configuration file (`development.ini` or `production.ini`).

The following are OpenStack settings. Values for the Vagrant based himlar-connect
development environment are shown.

<dl>
<dt>horizon_url</dt>
<dd>URL for the OpenStack dashboard. E.g. <em>http://10.0.3.11</em></dd>
<dt>keystone_url</dt>
<dd>URL for the OpenStack Keystone Identity Service, v3. E.g. <em>http://10.0.3.11:5000/v3</em></dd>
<dt>admin_pw</dt>
<dd>Administrator password for OpenStack. E.g. <em>himlardev</em></dd>
</dl>

The following are settings from the client's page on the Dataporten
dashboard, OAuth Details / OAuth Client credentials
section:

<dl>
<dt>oauth_client_id</dt>
<dd>E.g. the client ID above</dd>
<dt>oauth_client_secret</dt>
<dd>E.g. the client secret above</em></dd>
</dl>

### Installation

The app will typically be installed inside a virtualenv

    python setup.py develop

or

    python setup.py install

To run it as a standalone web server:

    pserve --reload developent.ini

or

    pserve production.ini

