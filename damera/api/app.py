import os
import pecan
from oslo_config import cfg
from oslo_log import log as logging
from paste import deploy

from damera.common import config as common_config
from damera.api import config as api_config
from damera.api import middleware

API_SERVICE_OPTS = [
    cfg.PortOpt('port',
                default=9800,
                help="The port for the Damera API server."),
    cfg.IPOpt('host',
              default='127.0.0.1',
              help="The listen IP for the Damera API server."),
    cfg.StrOpt('api_paste_config',
               default="api-paste.ini",
               help="Configuration file for WSGI definition of API.")
]

CONF = cfg.CONF
opt_group = cfg.OptGroup(name='api',
                         title='Options for the damera-api services.')

CONF.register_group(opt_group)
CONF.register_opts(API_SERVICE_OPTS, opt_group)

LOG = logging.getLogger(__name__)


def get_pecan_config():
    # Set up the pecan configuration
    filename = api_config.__file__.replace('.pyc', '.py')
    return pecan.configuration.conf_from_file(filename)


def setup_app(config=None):
    if not config:
        config = get_pecan_config()

    app_conf = dict(config.app)
    common_config.set_config_defaults()

    app = pecan.make_app(
        app_conf.pop('root'),
        logging=getattr(config, 'logging', {}),
        wrap_app=middleware.ParsableErrorMiddleware,
        **app_conf
    )

    return app


def load_app():
    cfg_file = None
    cfg_path = cfg.CONF.api.api_paste_config
    if not os.path.isabs(cfg_path):
        cfg_file = CONF.find_file(cfg_path)
    elif os.path.exists(cfg_path):
        cfg_file = cfg_path

    if not cfg_file:
        raise cfg.ConfigFilesNotFoundError([cfg.CONF.api_paste_config])
    LOG.info(_("Full WSGI config used: %s") % cfg_file)
    return deploy.loadapp("config:" + cfg_file)


def app_factory(global_config, **local_conf):
    return setup_app()