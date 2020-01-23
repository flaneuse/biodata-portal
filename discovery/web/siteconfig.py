
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
# NOTE: Everything should be automated; if you want to change the sort order in the heatmap in /schema, though, you need to alter schema.vue:repoOrder
REPOSITORIES = [{
"name": "Omics DI",
"id": "omicsdi",
"synonyms": ["omicsdi", "indexed_omicsdi"],
"img_src": "static/img/repositories/omicsdi.png",
"url": "https://www.omicsdi.org/",
"description": ""
},
{
"name": "NCBI GEO",
"id": "ncbi_geo",
"synonyms": ["indexed_ncbi_geo", "ncbi_geo", "ncbi geo"],
"img_src": "static/img/repositories/geo.gif",
"url": "https://www.ncbi.nlm.nih.gov/geo/",
"description": ""
},
{
"name": "Zenodo",
"id": "zenodo",
"synonyms": ["indexed_zenodo", "zenodo"],
"img_src": "static/img/repositories/zenodo.svg",
"url": "https://zenodo.org/",
"description": ""
},
{
"name": "Harvard Dataverse",
"id": "harvard_dataverse",
"synonyms": ["indexed_harvard_dataverse", "harvard_dataverse", "harvard dataverse"],
"img_src": "static/img/repositories/dataverse_small.png",
"url": "https://dataverse.harvard.edu/",
"description": ""
},
{
"name": "NYU Data Catalog",
"id": "nyu",
"synonyms": ["indexed_nyu", "nyu"],
"img_src": "static/img/repositories/nyu.png",
"url": "https://datacatalog.med.nyu.edu/",
"description": ""
}
]
