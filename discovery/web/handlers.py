# pylint: disable=abstract-method, arguments-differ, missing-docstring

''' Discovery Web Tornado Request Handler'''

import json
import logging
import os

from jinja2 import Environment, FileSystemLoader
from tornado.httputil import url_concat
import sass

from biothings.web.api.helper import BaseHandler as BioThingsBaseHandler

import discovery.web.siteconfig as siteconfig

TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
TEMPLATE_LOADER = FileSystemLoader(searchpath=TEMPLATE_PATH)
TEMPLATE_ENV = Environment(loader=TEMPLATE_LOADER, cache_size=0)

# Project specific globals
TEMPLATE_ENV.globals['site_name'] = siteconfig.SITE_NAME
TEMPLATE_ENV.globals['site_desc'] = siteconfig.SITE_DESC
TEMPLATE_ENV.globals['contact_email'] = siteconfig.CONTACT_EMAIL
TEMPLATE_ENV.globals['contact_repo'] = siteconfig.CONTACT_REPO
TEMPLATE_ENV.globals['api_url'] = siteconfig.API_URL
TEMPLATE_ENV.globals['site_url'] = siteconfig.SITE_URL
# Repositories
TEMPLATE_ENV.globals['repo_names'] = list(map(lambda x: x['name'], siteconfig.REPOSITORIES))
TEMPLATE_ENV.globals['repo_objects'] = siteconfig.REPOSITORIES

# IMAGES FOLDER
TEMPLATE_ENV.globals['static_image_folder'] = siteconfig.STATIC_IMAGE_FOLDER
# Colors used
TEMPLATE_ENV.globals['color_main'] = siteconfig.MAIN_COLOR
TEMPLATE_ENV.globals['color_sec'] = siteconfig.SEC_COLOR

# Compile site specific minified css
sass.compile(dirname=(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/scss'), os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/css')), output_style='compressed')


class BaseHandler(BioThingsBaseHandler):
    def return_404(self):
        '''return a custom 404 page'''
        doc_file = "404.html"
        doc_template = TEMPLATE_ENV.get_template(doc_file)
        doc_output = doc_template.render()
        self.set_status(404)
        self.write(doc_output)


class MainHandler(BaseHandler):
    def get(self):
        url = self.get_argument('url', None)
        if url:
            print(url)
            template_file = "viewer.html"
            schema_template = TEMPLATE_ENV.get_template(template_file)
            schema_output = schema_template.render(
                Context=json.dumps({"Query": '', "Content": True, 'URL': url}))
            self.write(schema_output)
        else:
            index_file = "index.html"
            index_template = TEMPLATE_ENV.get_template(index_file)
            index_output = index_template.render()
            self.write(index_output)


class AboutHandler(BaseHandler):
    def get(self):
        doc_file = "about.html"
        about_template = TEMPLATE_ENV.get_template(doc_file)
        about_output = about_template.render()
        self.write(about_output)

class PageNotFoundHandler(BaseHandler):
    def get(self):
        self.return_404()


class SearchHandler(BaseHandler):
    def get(self):
        doc_file = "search-results.vue"
        guide_template = TEMPLATE_ENV.get_template(doc_file)
        guide_output = guide_template.render()
        self.write(guide_output)

class NiaidHandler(BaseHandler):
    def get(self):
        doc_file = "niaid.vue"
        guide_template = TEMPLATE_ENV.get_template(doc_file)
        guide_output = guide_template.render()
        self.write(guide_output)

class SchemaHandler(BaseHandler):
    def get(self):
        doc_file = "schema.vue"
        guide_template = TEMPLATE_ENV.get_template(doc_file)
        guide_output = guide_template.render()
        self.write(guide_output)


APP_LIST = [
    (r"/?", MainHandler),
    (r"/about/?", AboutHandler),
    (r"/search/?", SearchHandler),
    (r"/niaid-priorities/?", NiaidHandler),
    (r"/schema/?", SchemaHandler),
    (r".*", PageNotFoundHandler)
]
