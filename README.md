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
<dd><em>1375546d-7476-4ed7-a61a-92fd841f36a2</em></dd>
<dt>Client Secret<dt>
<dd><em>a244b4c8-8e9a-40e6-858d-c4b66cd9454c</em></dd>
<dt>Redirect URI<dt>
<dd><em>http://localhost:6543/login</em></dd>
</dl>

The OpenStack dashboard also has to be registered in Dataporten. See
the [himlar-connect documentation](https://github.com/norcams/himlar-connect#to-register-the-dev-env-horizonkeystone-in-connect).

###  configuration

All parameters are entered in the `app:main` section of the
configuration file (`development.ini` or `production.ini`). Copy
`development.ini.example` to `development.ini` and add the parameters.

The following are OpenStack parameters. Values for the Vagrant based himlar-connect
development environment are shown.

<dl>
<dt>horizon_url</dt>
<dd>URL for the OpenStack dashboard. E.g. <em>http://10.0.3.11</em></dd>
<dt>keystone_url</dt>
<dd>URL for the OpenStack Keystone Identity Service, v3. E.g. <em>http://10.0.3.11:5000/v3</em></dd>
<dt>admin_pw</dt>
<dd>Administrator password for OpenStack. E.g. <em>himlardev</em></dd>
<dt>project_name</dt>
<dd>Name of project which creates resources. E.g.: admin</dd>
<dt>dp_domain_name</dt>
<dd>Name of domain resources will belong to. E.g.: connect</dd>
<dt>default_domain_name</dt>
<dd>Name of default domain. E.g.: default</dd>
<dt>member_role_name</dt>
<dd>Name of member role. E.g.: _member_</dd>
<dt>with_local_user</dt>
<dd>If 'true', a local user will be created in the same group, with
the Dataporten email as username.</dd>
<dt>keystone_cachain</dt>
<dd>Certificate chain for keystone. Optional.</dd>
</dl>

The following are parameters from the client's page on the Dataporten
dashboard, OAuth Details / OAuth Client credentials
section:

<dl>
<dt>oauth_client_id</dt>
<dd>E.g. the client ID above</dd>
<dt>oauth_client_secret</dt>
<dd>E.g. the client secret above</em></dd>
</dl>

### Installation

If the project was checked out from git, first make sure that the
submodule with the theme is fetched:

    git submodule init
    git submodule update

The app will typically be installed inside a virtualenv

    python setup.py develop

or

    python setup.py install

To run it as a standalone web server:

    pserve --reload developent.ini

or

    pserve production.ini

### Standalone use

You can also access the functionality as a script. You can delete
resources, provision resources, or both. Here is how to delete
resources for a user:

    python himlar_dp_prep/dp_provisioner.py --pw=topsecret \
        --dp-domain-name=connect --id=donald@duck.com  \
        --url=http://10.0.3.11:5000/v3 \
        --delete=1 --provision=0

Arguments:

<dl>
<dt>--id</dt>
<dd>Identity to provision for. Typically email</dd>
<dt>--pw</dt>
<dd>Admin password</dd>
<dt>--url</dt>
<dd>Keystone url</dd>
<dt>--project-name</dt>
<dd>Admin project name</dd>
<dt>--dp-domain-name</dt>
<dd>Dataporten domain name</dd>
<dt>--delete</dt>
<dd>Set to 1 to delete resources</dd>
<dt>--provision</dt>
<dd>Set to 1 to provision resources</dd>
<dt>--with-local-user</dt>
<dd>Set to 1 to provision a local user for local access</dd>
</dl>
