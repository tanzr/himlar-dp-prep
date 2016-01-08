import logging
import argparse
from keystoneclient.auth.identity import v3
from keystoneclient import session
from keystoneclient.v3 import client

ADMIN_NAME = 'admin'
PROJECT_NAME = 'openstack'
DEFAULT_DOMAIN_NAME = 'default'
DP_DOMAIN_NAME = 'dataporten'
MEMBER_ROLE_NAME = 'user'

log = logging.getLogger(__name__)

def group_name(user_id):
    return  '{}-group'.format(user_id)

def proj_name(user_id):
    return  user_id.lower()

class DpProvisioner(object):
    def __init__(self, url, password):
        auth = v3.Password(auth_url=url,
                           username=ADMIN_NAME,
                           password=password,
                           user_domain_name=DEFAULT_DOMAIN_NAME,
                           project_name=PROJECT_NAME,
                           project_domain_name=DEFAULT_DOMAIN_NAME)
        sess = session.Session(auth=auth)
        self.ks = client.Client(session=sess)
        domains = self.ks.domains.list(name=DP_DOMAIN_NAME)
        if len(domains) == 1:
            self.domain = domains[0]
        else:
            raise ValueError("Expecting unique '{}' domain".format(DP_DOMAIN_NAME))

    def del_resources(self, user_id):
        groups = self.ks.groups.list(name=group_name(user_id), domain=self.domain)
        projs = self.ks.projects.list(name=proj_name(user_id), domain=self.domain)
        for p in projs:
            self.ks.projects.delete(p.id)
            log.info("deleted project %s", p.id)
        for g in groups:
            self.ks.groups.delete(g.id)
            log.info("deleted group %s", g.id)


    def is_provisioned(self, user_id):
        groups = self.ks.groups.list(name=group_name(user_id), domain=self.domain)
        if len(groups) > 0:
            group = groups[0]
            roles = self.ks.role_assignments.list(group=group)
            return any(['project' in r.scope for r in roles])
        else:
            return False

    def grant_membership(self, proj, group):
        member_roles = self.ks.roles.list(name=MEMBER_ROLE_NAME)
        if len(member_roles) == 1:
            member_role = member_roles[0]
        else:
            raise ValueError('Expecting unique _member_ role')
        res = self.ks.roles.grant(role=member_role, project=proj, group=group)
        log.debug("res of granting role: %s", res)
        log.debug("role assignments for %s: %s",
                  group.name, self.ks.role_assignments.list(group=group))

    def provision(self, user_id):
        gname = group_name(user_id)
        pname = proj_name(user_id)
        groups = self.ks.groups.list(name=gname, domain=self.domain)
        projs = self.ks.projects.list(name=pname, domain=self.domain)
        if len(groups) < 1:
            group = self.ks.groups.create(name=gname, domain=self.domain)
            log.info("group created: %s", group.id)
        else:
            group = groups[0]
        if len(projs) < 1:
            proj = self.ks.projects.create(name=pname, domain=self.domain)
            log.info("project created: %s", proj.id)
        else:
            proj = projs[0]
        self.grant_membership(proj, group)

if __name__ == '__main__':
    DESCRIPTION = "Dataporten provisioner for Openstack"

    AUTH_URL = 'http://10.0.3.11:5000/v3'
    EMAIL_JK = 'jon.kare.hellan@uninett.no'

    def parse_args():
        parser = argparse.ArgumentParser(description=DESCRIPTION)
        parser.add_argument('--id', default=EMAIL_JK,
                            help="Identity to provision for")
        parser.add_argument('--pw', help='Password')
        parser.add_argument('--url', default=AUTH_URL, help="Keystone url")
        parser.add_argument('--delete', default=0, type=int,
                            help="Set to 1 to delete resources")
        parser.add_argument('--provision', default=1, type=int,
                            help="Set to 1 to provision")
        return parser.parse_args()

    args = parse_args()
    logging.basicConfig(level=logging.INFO)
    prov = DpProvisioner(args.url, args.pw)
    if args.delete:
        prov.del_resources(args.id)
    if args.provision:
        prov.provision(args.id)
