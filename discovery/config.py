# pylint: disable=unused-wildcard-import, wildcard-import, unused-import, invalid-name

''' Discovery App Configuration '''

from biothings.web.settings.default import *
from tornado.web import RedirectHandler

from discovery.web.handlers import APP_LIST as WEB_ENDPOINTS


# *****************************************************************************
# Tornado URL Patterns
# *****************************************************************************
UNINITIALIZED_APP_LIST = [
    (r"/sitemap.xml", RedirectHandler, {"url": "/static/sitemap.xml"}),
]
API_ENDPOINTS = []
APP_LIST = API_ENDPOINTS + WEB_ENDPOINTS

# *****************************************************************************
# Biothings SDK Settings
# *****************************************************************************
ACCESS_CONTROL_ALLOW_METHODS = 'HEAD,GET,POST,DELETE,PUT,OPTIONS'
DISABLE_CACHING = True
