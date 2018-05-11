#import pika
import logging
from pyramid.view import view_config
from pyramid.response import Response
from authomatic import Authomatic
from authomatic.adapters import WebObAdapter
from authomatic.providers import oauth2
from .dp_provisioner import DpProvisioner
from grampg import PasswordGenerator
#from .rmp import MQclient

log = logging.getLogger(__name__)

class LoginFailedException(Exception):
    pass

class NoUserException(Exception):
    pass

class NoEmailException(Exception):
    pass

class ProvisionerClient(object):
    def __init__(self, request):
        self.request = request
        self.settings = request.registry.settings

    def provision(self, user):
        keystone_url = self.settings.get('keystone_url', '')
        horizon_url = self.settings.get('horizon_url', '')
        admin_pw = self.settings.get('admin_pw', '')
        admin_user = self.settings.get('admin_user', '')
        project_name = self.settings.get('project_name', '')
        dp_domain_name = self.settings.get('dp_domain_name', '')
        default_domain_name = self.settings.get('default_domain_name', '')
        member_role_name = self.settings.get('member_role_name', '')
        keystone_cachain =  self.settings.get('keystone_cachain', None)
        with_local_user =  self.settings.get('with_local_user', 'false').lower() == 'true'
        mq_username = self.settings.get('mq_username', '')
        mq_password = self.settings.get('mq_password', '')
        mq_host = self.settings.get('mq_host', '')
        mq_vhost = self.settings.get('mq_vhost', '')
        config = dict(url=keystone_url,
                      password=admin_pw,
                      username=admin_user,
                      project_name=project_name,
                      dp_domain_name=dp_domain_name,
                      user_domain_name=default_domain_name,
                      project_domain_name=default_domain_name,
                      member_role_name=member_role_name,
                      keystone_cachain=keystone_cachain,
                      with_local_user=with_local_user,
                      mq_username=mq_username,
                      mq_password=mq_password,
                      mq_host=mq_host,
                      mq_vhost=mq_vhost)
        prov = DpProvisioner(config)
        was_provisioned = prov.is_provisioned(user.email)
        local_pw = None
        tpl = '{}/dashboard/auth/login/'
        res = dict(user=user,
                    dashboard_url=tpl.format(horizon_url),
                    was_provisioned=was_provisioned)
        if not was_provisioned:
            prov_result = prov.provision(user.email)
            res.update(prov_result)
        return res

    @view_config(route_name='reset', renderer='templates/reset.mak')
    def reset_view(self):
        keystone_url = self.settings.get('keystone_url', '')
        horizon_url = self.settings.get('horizon_url', '')
        admin_pw = self.settings.get('admin_pw', '')
        admin_user = self.settings.get('admin_user', '')
        project_name = self.settings.get('project_name', '')
        dp_domain_name = self.settings.get('dp_domain_name', '')
        default_domain_name = self.settings.get('default_domain_name', '')
        member_role_name = self.settings.get('member_role_name', '')
        keystone_cachain =  self.settings.get('keystone_cachain', None)
        with_local_user =  self.settings.get('with_local_user', 'false').lower() == 'true'
        mq_username = self.settings.get('mq_username', '')
        mq_password = self.settings.get('mq_password', '')
        mq_host = self.settings.get('mq_host', '')
        mq_vhost = self.settings.get('mq_vhost', '')
        config = dict(url=keystone_url,
                      password=admin_pw,
                      username=admin_user,
                      project_name=project_name,
                      dp_domain_name=dp_domain_name,
                      user_domain_name=default_domain_name,
                      project_domain_name=default_domain_name,
                      member_role_name=member_role_name,
                      keystone_cachain=keystone_cachain,
                      with_local_user=with_local_user,
                      mq_username=mq_username,
                      mq_password=mq_password,
                      mq_host=mq_host,
                      mq_vhost=mq_vhost)
        prov = DpProvisioner(config)
        user_email = prov.get_user(self) #get user from DP
        horizon_url = self.settings.get('horizon_url', '')
        tpl = '{}/dashboard/auth/login/'
        local_pw = prov.reset(user_email)
        #return { 'local_pw': local_pw }
        res = dict(local_user_name=user_email, local_pw=local_pw)
        return res

    def login_complete(self, result):
        if result.error:
            raise LoginFailedException(result.error.message)
        elif not result.user:
            raise NoUserException()
        elif not (result.user.name and result.user.email):
            # OAuth 2.0 provides only limited user data on login,
            # We need to update the user to get more info.
            result.user.update()
        if not (result.user.email and len(result.user.email) > 0):
            raise NoEmailException()
        return self.provision(result.user)

    @view_config(route_name='login', renderer='templates/loggedin.mak')
    def login_view(self):
        log.debug('login_view')
        response = Response()
        dpconf = dict(class_=oauth2.Dataporten,
                      consumer_key=self.settings.get('oauth_client_id', ''),
                      consumer_secret=self.settings.get('oauth_client_secret', ''))
        authomatic = Authomatic(config=dict(dp=dpconf), secret='mumbojumbo')
        result = authomatic.login(WebObAdapter(self.request, response), 'dp')
        if result:
            # The login procedure is over
            log.debug('login_view - login complete')
            return self.login_complete(result)
        else:
            log.debug('login_view - login not complete')
            return response

@view_config(route_name='home', renderer='templates/home.mak')
def home_view(request):
    log.debug('home_view')
    return {}

@view_config(context=LoginFailedException, renderer="templates/loginfailed.mak")
def login_failed_view(exc, request):
    return {'message': str(exc)}

@view_config(context=NoUserException, renderer="templates/loginfailed.mak")
def no_user_view(exc, request):
    return {'message': 'User not known after login'}

@view_config(context=NoEmailException, renderer="templates/noemail.mak")
def no_email_view(exc, request):
    return {}
