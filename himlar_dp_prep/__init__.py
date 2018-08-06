from pyramid.config import Configurator
import socket

def main(global_config, **settings):

#    ip = '172.31.0.31' #'mq.vagrant.iaas.intern'
#    port = 5672
#
#    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    result = sock.connect_ex((ip, port))
#    if result == 0:
#        print "Port is open."
#    else:
#        print "Port is closed."

    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_mako')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('uninett-theme', 'uninett-theme')
    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.add_route('reset', '/reset')
    config.scan()
    return config.make_wsgi_app()
