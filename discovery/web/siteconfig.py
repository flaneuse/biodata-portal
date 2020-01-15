
# DO NOT comment out
#  (REQ) REQUIRED

# *****************************************************************************
# DATA DISCOVERY ENGINE - MAIN (REQ)
# *****************************************************************************

# name also used on metadata
SITE_NAME = "NIAID Data portal"
SITE_DESC = 'An aggregator of open datasets, with a particular focus on allergy and infectious diseases'
API_URL = "http://su07:8080/api/"
SITE_URL = "https://discovery.biothings.io/niaid/"
# SITE_URL = "http://localhost:8000/"

CONTACT_REPO = "https://github.com/SuLab/niaid-data-portal"
CONTACT_EMAIL = "cd2h-metadata@googlegroups.com"

# *****************************************************************************
# DATA DISCOVERY ENGINE - METADATA (REQ)
# *****************************************************************************

METADATA_CONTENT_URL = "http://discovery.biothings.io/"
METADATA_DESC = 'An aggregator of open datasets, with a particular focus on allergy and infectious diseases'
METADATA_FEATURED_IMAGE = "https://i.postimg.cc/zvRMbPSs/featured.jpg"
METADATA_MAIN_COLOR = "#1C5D5D"

# *****************************************************************************
# DATA DISCOVERY ENGINE - COLORS (REQ)
# *****************************************************************************

MAIN_COLOR = "#1C5D5D"
SEC_COLOR = "#A5E7CF"

# *****************************************************************************
# DATA DISCOVERY ENGINE - IMAGES (REQ)
# *****************************************************************************

# create a folder with <name> and put all icons there
STATIC_IMAGE_FOLDER = 'dde'

# *****************************************************************************
# DATA DISCOVERY ENGINE - METADATA
# *****************************************************************************

GUIDE_PRESETS = [
                    # {
                    # 'namespace':'ctsa',
                    # 'prefix':'bts',
                    # 'name':'CTSADataset',
                    # 'description':'A schema describing Dataset from CTSA center'
                    # },
                    {
                    'namespace':'biomedical',
                    'prefix':'bts',
                    'name':'BioMedicalDataset',
                    'description':'A schema describing a BioMedical Dataset'
                    },
                ]

GUIDE_SETTINGS = {
                    "form-mode": 0,
                }

GUIDE_PORTALS = [
                    {
                    'namespace':'google',
                    'prefix':'bts',
                    'name':'Google',
                    'description':'A list of metadata fields required and recommended by Google Dataset Search Engine. <a target="_blank" href="https://developers.google.com/search/docs/data-types/dataset">Learn More<a/>',
                    'selected': 1
                    },
                    {
                    'namespace':'datacite',
                    'prefix':'bts',
                    'name':'DataCite',
                    'description':'A list of core metadata properties chosen for an accurate and consistent identification of a resource for citation and retrieval purposes by DataCite. <a target="_blank" href="https://schema.datacite.org/">Learn More<a/>',
                    'selected': 0
                    },
                ]
# *****************************************************************************
# DATA DISCOVERY ENGINE - SCHEMA PLAYGROUND
# *****************************************************************************

# also used in registry shortcuts
STARTING_POINTS = [
                    {
                    'namespace':'schema',
                    'prefix':'schema',
                    'name':'Dataset',
                    'description':'A body of structured information describing some topic(s) of interest.'
                    },
                ]

# *****************************************************************************
# DATA DISCOVERY ENGINE - SCHEMA REGISTRY
# *****************************************************************************

REGISTRY_SHORTCUTS= [
                        {
                        "name" : "Schema.org",
                        "registered_namespace" :'schema'
                        },
                        {
                        "name" : "BioLink",
                        "registered_namespace" :'bts'
                        }
                    ]

# *****************************************************************************
# DATA DISCOVERY ENGINE - FAQ
# *****************************************************************************
