# pylint: disable=unused-wildcard-import, wildcard-import, unused-import, invalid-name

''' Discovery App Configuration '''

from biothings.web.settings.default import *
from tornado.web import RedirectHandler

from discovery.config_key import (COOKIE_SECRET, GITHUB_CLIENT_ID,
                                  GITHUB_CLIENT_SECRET)
from discovery.web.handlers import APP_LIST as WEB_ENDPOINTS

# *****************************************************************************
# Credentials
# *****************************************************************************
# Define in ./config_key.py:
#   COOKIE_SECRET = '<Any Random String>'
#   GITHUB_CLIENT_ID = '<your Github application Client ID>'
#   GITHUB_CLIENT_SECRET = '<your Github application Client Secret>'


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
