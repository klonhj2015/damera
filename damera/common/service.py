import socket

from oslo_config import cfg
from oslo_log import log as logging

from damera.common import config
from damera.i18n import _


service_opts = [
    cfg.StrOpt('host',
               default=socket.getfqdn(),
               help=_('Name of this node. This can be an opaque identifier. '
                      'It is not necessarily a hostname, FQDN, or IP address. '
                      'However, the node name must be valid within '
                      'an AMQP key, and if using ZeroMQ, a valid '
                      'hostname, FQDN, or IP address.')),
]

cfg.CONF.register_opts(service_opts)


def prepare_service(argv=None):
    if argv is None:
        argv = []
    logging.register_options(cfg.CONF)
    config.parse_args(argv)
    config.set_config_defaults()

    logging.setup(cfg.CONF, 'damera')
