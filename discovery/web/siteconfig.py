
# DO NOT comment out
#  (REQ) REQUIRED

# *****************************************************************************
# DATA DISCOVERY ENGINE - MAIN (REQ)
# *****************************************************************************

# name also used on metadata
SITE_NAME = "NIAID Data Portal"
SITE_DESC = 'An aggregator of open datasets, with a particular focus on allergy and infectious diseases'
API_URL = "https://metadataplus.biothings.io/api/"
# API_URL = "https://crawler.biothings.io/api/"
SITE_URL = "https://discovery.biothings.io/niaid/"
# SITE_URL = "http://localhost:8000/"

CONTACT_REPO = "https://github.com/SuLab/niaid-data-portal"
CONTACT_EMAIL = "cd2h-metadata@googlegroups.com"

# *****************************************************************************
# DATA DISCOVERY ENGINE - METADATA (REQ)
# *****************************************************************************

METADATA_CONTENT_URL = "http://discovery.biothings.io/"
METADATA_DESC = 'An aggregator of open datasets, with a particular focus on allergy and infectious diseases'
METADATA_FEATURED_IMAGE = "https://i.postimg.cc/vZYnpSML/featured.jpg"
METADATA_MAIN_COLOR = "#1C5D5D"

# *****************************************************************************
# DATA DISCOVERY ENGINE - COLORS (REQ)
# *****************************************************************************

MAIN_COLOR = "#113B56"
SEC_COLOR = "#0F627C"

# *****************************************************************************
# DATA DISCOVERY ENGINE - IMAGES (REQ)
# *****************************************************************************

# create a folder with <name> and put all icons there
STATIC_IMAGE_FOLDER = 'niaid'

# *****************************************************************************
# REPOSITORY NAMES
# *****************************************************************************

# List of all possible repositories.
# NOTE: if you want the names to appear in a particular way, you also need to change clean-facets.js
REPOSITORIES = [{
"name": "Omics DI",
"id": "omicsdi",
"img_src": "static/img/repositories/omicsdi.png",
"url": "https://www.omicsdi.org/",
"description": ""
},
{
"name": "NCBI GEO",
"id": "ncbi_geo",
"img_src": "static/img/repositories/geo.gif",
"url": "https://www.ncbi.nlm.nih.gov/geo/",
"description": ""
},
{
"name": "Zenodo",
"id": "zenodo",
"img_src": "static/img/repositories/zenodo.svg",
"url": "https://zenodo.org/",
"description": ""
},
{
"name": "Harvard Dataverse",
"id": "harvard_dataverse",
"img_src": "static/img/repositories/dataverse_small.png",
"url": "https://dataverse.harvard.edu/",
"description": ""
}]
