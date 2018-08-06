import logging
import argparse
from keystoneclient.auth.identity import v3
from keystoneclient import session
import keystoneauth1.exceptions as exceptions
from keystoneclient.v3 import client
from grampg import PasswordGenerator
from himlar_dp_prep.rmq import MQclient
import pyramid.httpexceptions as exc

ADMIN_NAME = 'admin'
PROJECT_NAME = 'admin'
DEFAULT_DOMAIN_NAME = 'default'
DP_DOMAIN_NAME = 'dataporten'
MEMBER_ROLE_NAME = '_member_'

log = logging.getLogger(__name__)

def api_user_name(user_id):
    return user_id.lower()

def make_password():
    gen = PasswordGenerator()
    return (gen.of().some('numbers').some('lower_letters').some('upper_letters')
            .length(16).done().generate())

class DpProvisioner(object):
    def __init__(self, config):
	self.config = config
        self.member_role_name = config['member_role_name']
        self.with_local_user = config.get('with_local_user')
        self.api_pw = None
        dp_domain_name = config['dp_domain_name']
        keystone_cachain = config.get('keystone_cachain')
        auth = v3.Password(auth_url=config['url'],
                           username=config['username'],
                           password=config['password'],
                           project_name=config['project_name'],
                           user_domain_name=config['user_domain_name'],
                           project_domain_name=config['project_domain_name'])
        sess = session.Session(auth=auth,verify=keystone_cachain)
        self.ks = client.Client(session=sess)
        domains = self.ks.domains.list(name=dp_domain_name)
        if len(domains) == 1:
            self.domain = domains[0]
        else:
            raise ValueError("Expecting unique '{}' domain".format(dp_domain_name))
#        self.rmq = MQclient(config)

    def get_user(self, user_id):
	api_users = self.ks.users.list(domain=self.domain, name=api_user_name(user_id))
	try:
	    if api_users:
		for user in api_users:
	    	    self.ks.users.get(user.id)
                    return user
        except: #exceptions.http.NotFound:
	    log.info('User %s not found!', api_users)

    def is_provisioned(self, user_id, user_type='api'):
        user = self.get_user(user_id)
	try:
            if user:
              if hasattr(user, 'type') and user.type == user_type:
                log.info('User %s is already provisioned!', user.name)
                return True
              # User found but type missing: we guess this is still ok
              log.info('User %s found, but missing type = api!', user.name)
              return True
	except:
	    log.info('User %s not found!', user)

    def provision(self, user_id):
        api_name = api_user_name(user_id)
        if self.with_local_user:
            api_pw = make_password()
	    log.info('API user and password: %s  %s', api_name, api_pw)
            data = {
                'action': 'provision',
                'email': user_id,
                'password': api_pw
            }
	    try:
	        self.rmq = MQclient(self.config)
		self.rmq.push(data=data, queue='access')
		return dict(api_user_name=api_name, api_pw=api_pw)
	    except:
	        raise exc.HTTPInternalServerError("HTTP error occurred during provision process.")

    def reset(self, user_id):
        api_name = api_user_name(user_id)
        if self.with_local_user:
            api_pw = make_password()
            log.info("Reset password for: %s", user_id)
            data = {
                'action': 'reset_password',
                'email': user_id,
                'password': api_pw
            }
	try:
	    self.rmq = MQclient(self.config)
            if self.is_provisioned(user_id):
                self.rmq.push(data=data, queue='access')
                return api_pw
	except:
            raise exc.HTTPInternalServerError("HTTP error occurred during reset process.")

if __name__ == '__main__':
    DESCRIPTION = "Dataporten provisioner for Openstack"

    AUTH_URL = 'http://10.0.3.11:5000/v3'
    EMAIL_JK = 'jon.kare.hellan@uninett.no'

#    def parse_args():
#        parser = argparse.ArgumentParser(description=DESCRIPTION)
#        parser.add_argument('--id', default=EMAIL_JK,
#                            help="Identity to provision for")
#        parser.add_argument('--pw', help='Password')
#        parser.add_argument('--url', default=AUTH_URL, help="Keystone url")
#        parser.add_argument('--project-name', default=PROJECT_NAME, help="Admin project name")
#        parser.add_argument('--dp-domain-name', default=DP_DOMAIN_NAME, help="Dataporten domain name")
#        parser.add_argument('--delete', default=0, type=int,
#                            help="Set to 1 to delete resources")
#        parser.add_argument('--provision', default=1, type=int,
#                            help="Set to 1 to provision")
#        parser.add_argument('--with-local-user', default=1, type=int,
#                            help="Set to 1 to provision a local user for local access")
#        return parser.parse_args()
#
#    def make_config(args):
#        return dict(url=args.url,
#                    password=args.pw,
#                    username=ADMIN_NAME,
#                    project_name=args.project_name,
#                    dp_domain_name=args.dp_domain_name,
#                    user_domain_name=DEFAULT_DOMAIN_NAME,
#                    project_domain_name=DEFAULT_DOMAIN_NAME,
#                    member_role_name=MEMBER_ROLE_NAME,
#                    with_local_user=args.with_local_user)
#
#    args = parse_args()
#    config = make_config(args)
#    logging.basicConfig(level=logging.INFO)
#    prov = DpProvisioner(config)
#    if args.delete:
#        prov.del_resources(args.id)
#    if args.provision:
#        prov.provision(args.id)
#        if prov.local_pw:
#            print('password for local user: {}'.format(prov.local_pw))
