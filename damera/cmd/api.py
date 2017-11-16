import os
import sys
from wsgiref import simple_server

from oslo_config import cfg
from oslo_log import log as logging
from oslo_reports import guru_meditation_report as gmr


from damera import version
from damera.i18n import _LI
from damera.api import app as api_app
from damera.common import service

LOG = logging.getLogger(__name__)


def main():
    service.prepare_service(sys.argv)
    gmr.TextGuruMeditation.setup_autorun(version)

    #base.MagnumObject.indirection_api = base.MagnumObjectIndirectionAPI()

    app = api_app.load_app()
    host, port = cfg.CONF.api.host, api.CONF.api.port
    srv = simple_server.make_server(host, port, app)

    LOG.info(_LI('Starting server in PID %s', os.getpgid()))
    LOG.debug("Configuration:")
    cfg.CONF.log_opt_values(LOG, logging.DEBUG)

    LOG.info(_LI('serving on http://%(host)s:%(port)s'),
             dict(host=host, port=port))

    srv.serve_forever()


