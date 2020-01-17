{% extends "main.html" %}
{% block content %}
{% include "header.html" %}
<style scoped>
  .search-term {
    opacity: 0.75;
    background: #ddd;
    padding: 1px 3px;
  }

  .num-results {
    /* padding: 2px 10px;
    border-radius: 5px; */
    font-size: 1.25em;
  }

  .disease-title {
    margin-bottom: 0 !important;
  }

  .disease-title-container {
    padding: 5px 10px;
  }

  h6.summary-title {
    /* background: #ddd; */
    padding: 0.25em;
    font-weight: 100;
    text-transform: uppercase;
    margin: 0 !important;
}

.summary-container {
  margin-right: 1em;
}

.light {
  color: white;
}

.dark {
  color: #6c757d;
}

.search-link {
  background: white;
  padding: 0 8px;
  border: none;
  border-radius: 4px;
  /* box-shadow: 2px 2px 5px #6c757d; */
}

.search-link.dark {
  background: #6c757d;
}

.search-link.dark:hover {
  background: #545b62 !important;
}

.search-link.light:hover {
  background: #dde0e2 !important;
}

</style>
<div id="niaid-diseases" class="container d-flex" style="min-height:100vh">
  <div v-if=loading class="loader">
    <img src="static/img/ripple.svg" />
  </div>

  <div class="jumbotron bg-light text-muted w-100" v-if="numResults">
    <div class="jumbotron bg-light bg-animated">
      <h1 class="row">Datasets containing NIAID priority diseases</h1>
    </div>
    <p class="row"
      v-html="`<span>Of the ${diseaseKeywords.length} priority diseases and conditions for the National Institute of Allergy and Infectious Diseases, <b>${results[0].disease}</b> has the most results within the ` + '{{site_name}}' + '.</span>'">
    </p>

    <!-- TREEMAP -->
    <div id="niaid-treemap" class="mb-5">
      <h5>Number of datasets per disease area</h5>
      <app-treemap v-bind:results="results" v-bind:route="'niaid-priorities'" v-if="numResults"></app-treemap>
    </div>

    <!-- LOOP OVER INDIVIDUAL DISEASES -->
    <div v-for="disease in results" :id="disease.diseaseID" :key="disease.diseaseID" class="disease-summary border-bottom mb-5">

      <!-- NUMBER OF RESULTS -->
      <div class="row d-flex align-items-center justify-content-between mb-1 disease-title-container" v-bind:style="{background: colorScale(disease.total)}" v-bind:class="textColorScale(disease.total)">
        <div class="d-flex align-items-center">
          <h4 class="disease-title" v-text="disease.disease"></h4>
          <small class="ml-3 pointer" @click="disease.showTerms = !disease.showTerms" v-text="disease.showTerms ? 'hide search terms' : 'show search terms'"></small>
        </div>

        <div class="d-flex">
          <div v-text="disease.total.toLocaleString() + ' results'" class="num-results"></div>
          <button class="ml-3 search-link" v-bind:class="textColorScale(disease.total)">
            <a :href="'search?q=' + disease.query" v-text="'view ' + disease.disease + ' datasets'" v-bind:style="{color: colorScale(disease.total)}"></a>
          </button>
        </div>
      </div>

      <!-- SEARCH TERMS -->
      <div class="row" v-show="disease.showTerms">
        <small class="search-term mr-2 mb-1" v-for="term in disease.searchTerms" :key="term">
          <span v-text="term"></span>
        </small>
      </div>

      <div class="d-flex flex-wrap">

        <!-- SOURCE -->
        <div class="summary-container">
          <h6 class="summary-title">source</h6>
          <app-donut v-bind:source_counts="disease.source_counts" v-bind:width="100"></app-donut>
        </div>

        <!-- FUNDER -->
        <div class="summary-container">
          <h6 class="summary-title">funder</h6>
          <app-bar-graph v-bind:counts="disease.funders_counts"></app-bar-graph>
        </div>

        <!-- VARIABLE MEASURED -->
        <div class="summary-container">
          <h6 class="summary-title">variable measured</h6>
          <app-bar-graph v-bind:counts="disease.variable_count"></app-bar-graph>
        </div>

        <!-- MEASUREMENT TECHNIQUE -->
        <div class="summary-container">
          <h6 class="summary-title">measurement technique</h6>
          <app-bar-graph v-bind:counts="disease.technique_count"></app-bar-graph>
        </div>

        <!-- KEYWORDS -->
        <div class="p-3">
          <h6 v-text="facetSize + ' most common keywords'" class="summary-title"></h6>
          <div class="d-flex" id="keyword-counts">
            <div v-for="keywordPair in disease['keywords.keyword']['terms']" v-text="keywordPair.term" class="keyword-cloud" v-bind:style="{ opacity: calcOpacity(keywordPair, disease['keywords.keyword']['terms'])}" :key="disease.disease + '_' + keywordPair.term">
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>

</div>
{% endblock %}

{% block extra_scripts %}
<script src="https://unpkg.com/vuex"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/vue/2.4.2/vue.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/axios/0.18.0/axios.min.js"></script>
<script src="https://unpkg.com/rxjs/bundles/rxjs.umd.js"></script>
<script src="https://unpkg.com/vue/dist/vue.js"></script>
<script src="https://unpkg.com/http-vue-loader"></script>
<script src="https://d3js.org/d3.v5.min.js"></script>
<script src="static/js/vue-rx.js"></script>
<script src="static/js/clean-facets.js"></script>
<script src="static/js/chroma.min.js"></script>
<script src="https://unpkg.com/tippy.js@3/dist/tippy.all.min.js"></script>

<script type="module">
  var app = new Vue({
    el: '#niaid-diseases',
    name: "NIAID-diseases",
    components: {
  'app-treemap': window.httpVueLoader('static/components/Treemap.vue'),
  'app-donut': window.httpVueLoader('static/components/Donut.vue'),
  'app-bar-graph': window.httpVueLoader('static/components/BarGraph.vue')
},
    data: function() {
      return {
        loading: false,
        facetSize: 10,
        numResults: 0,
        colorScale: null,
        facets: ["_index", "funder.name.keyword", "funding.funder.name.keyword", "variableMeasured.keyword", "measurementTechnique.keyword", "keywords.keyword"],
        // Semi-automatically generated by scraping https://www.niaid.nih.gov/diseases-conditions
        // then manually looked at word counts from individual pages, cross-referencing with the physical websites, with a bit of random common synonyms thrown in:
        diseaseKeywords: [{
            "disease": "Asthma",
            "terms": ["Asthma"]
          },
          {
            "disease": "Autoimmune Diseases",
            "terms": ["Autoimmune Disease", "type 1 diabetes", "rheumatoid arthritis", "systemic lupus erythematosus", "systemic lupus", "lupus", "inflammatory bowel disease", "Diffuse Cutaneous Systemic Sclerosis"]
          },
          {
            "disease": "Autoimmune Lymphoproliferative Syndrome (ALPS)",
            "terms": ["Autoimmune Lymphoproliferative Syndrome", "ALPS"]
          },
          {
            "disease": "Cholera",
            "terms": ["Cholera", "Vibrio cholerae", "V. cholerae", "CTX"]
          },
          {
            "disease": "Dengue Fever",
            "terms": ["Dengue", "Dengue Fever", "DENV"]
          },
          {
            "disease": "E. coli",
            "terms": ["E. coli", "Escherichia coli", "Shiga Toxin-Producing E. coli", "STEC"]
          },
          {
            "disease": "Ebola & Marburg",
            "terms": ["Ebola", "EBOV", "EVD", "Marburg", "MARV", "MVD"]
          },
          {
            "disease": "Eczema (Atopic Dermatitis)",
            "terms": ["Eczema", "Atopic Dermatitis"]
          },
          {
            "disease": "Food Allergy",
            "terms": ["Food Allergy", "food allergen"]
          },
          {
            "disease": "Fungal Diseases",
            "terms": ["fungal disease", "Candidiasis", "Candida", "Candida albicans", "Candida glabrata", "Candida parapsilosis", "Candida tropicalis", "Candida auris", "C. albicans", "C. glabrata", "C. parapsilosis", "C. tropicalis",
              "C. auris", "thrush", "yeast infection", "Cryptococcosis", "Cryptococcus", "Cryptococcus neoformans", "Cryptococcus gattii", "C. neoformans", "C. gattii", "cryptococcal meningitis", "cryptococcal", "Aspergillosis",
              "Aspergillus", "Coccidioidomycosis", "Valley Fever", "Coccidioides", "Coccidioides immitis", "Coccidioides posadasii", "C. immitis", "C. posadasii", "Histoplasmosis", "Histoplasma", "Histoplasma capsulatum", "H. capsulatum",
              "Blastomycosis", "Blastomyces", "Blastomyces dermatitidis", "B. dermatitidis", "Pneumocystis", "Pneumocystis pneumonia", "Pneumocystis jirovecii", "P. jirovecii", "P. carinii"
            ]
          },
          {
            "disease": "Gonorrhea",
            "terms": ["Gonorrhea", "Neisseria gonorrhoeae", "N. gonorrhoeae", "gonococcal", "gonococci"]
          },
          {
            "disease": "Group A Streptococcal Infections",
            "terms": ["Group A Streptococcal Infections", "strep throat", "streptococcus", "Cellulitis", "Erysipelas", "Impetigo", "Scarlet fever", "scarlatina", "Necrotizing fasciitis", "Toxic shock syndrome", "Bacteremia"]
          },
          {
            "disease": "Hepatitis",
            "terms": ["Hepatitis", "HAV", "HBV", "HCV", "HDV", "HEV", "HepA", "HepB", "HepC", "HepD", "HepE"]
          },
          {
            "disease": "HIV/AIDS",
            "terms": ["HIV/AIDS", "HIV", "AIDS", "human immunodeficiency virus", "acquired immunodeficiency syndrome", "antiretroviral therapy"]
          },
          {
            "disease": "Influenza",
            "terms": ["Influenza", "flu"]
          },
          {
            "disease": "Leishmaniasis",
            "terms": ["Leishmaniasis", "Leishmania"]
          },
          {
            "disease": "Leprosy (Hansen's Disease)",
            "terms": ["Leprosy", "Hansen's disease", "Mycobacterium leprae", "M. leprae"]
          },
          {
            "disease": "Lyme Disease",
            "terms": ["Lyme Disease", "Borrelia burgdorferi", "B. burgdorferi", "borreliosis"]
          },
          {
            "disease": "Malaria ",
            "terms": ["Malaria", "Plasmodium", "Plasmodium falciparum", "Plasmodium vivax", "P. falciparum", "P. vivax"]
          },
          {
            "disease": "MERS & SARS",
            "terms": ["MERS", "SARS", "Middle East Respiratory Syndrome", "MERS-CoV", "severe acute respiratory syndrome", "SARS-CoV"]
          },
          {
            "disease": "Pertussis (Whooping Cough)",
            "terms": ["Pertussis", "Whooping Cough", "Bordetella pertussis", "B. pertussis"]
          },
          {
            "disease": "Plague",
            "terms": ["Plague", "Yersinia pestis", "Y. pestis"]
          },
          {
            "disease": "Primary Immune Deficiency Diseases",
            // "terms": ["Primary Immune Deficiency Disease", "PIDD", "Epstein-Barr virus", "EBV"]
            "terms": ["Primary Immune Deficiency Disease", "PIDD", "Epstein-Barr virus", "EBV", "Autoimmune polyglandular syndrome type 1", "APS-1", "autoimmune polyendocrinopathy-candidiasis-ectodermal dystrophy", "APECED", "BENTA", "B-cell expansion with NF-jB and T-cell anergy", "Caspase Eight Deficiency State", "CEDS", "CARD9 deficiency", "Chronic Granulomatous Disease", "CGD", "Common Variable Immunodeficiency", "CVID", "Congenital Neutropenia Syndrome", "CTLA4 Deficiency", "DOCK8 Deficiency", "GATA2 Deficiency", "Glycosylation Disorders", "Hyper-Immunoglobulin E Syndromes", "HIES", "Hyper-Immunoglobulin M Syndromes", "Interferon Gamma Deficiency", "Interleukin 12 Deficiency", "Interleukin 23 Deficiency", "Leukocyte Adhesion Deficiency", "LAD", "LRBA Deficiency", "PI3 Kinase Disease", "PLCG2-associated Antibody Deficiency and Immune Dysregulation", "PLAID", "Severe Combined Immunodeficiency", "SCID", "STAT3 Dominant-Negative Disease", "STAT3DN", "autosomal dominant hyper-IgE syndrome", "AD-HIES", "Job's Syndrome", "STAT3 Gain-of-Function Disease", "Warts, Hypogammaglobulinemia, Infections, and Myelokathexis", "WHIM Syndrome", "Wiskott-Aldrich Syndrome", "X-Linked Agammaglobulinemia", "XLA", "X-Linked Lymphoproliferative Disease", "XLP", "XMEN Disease"]
          },
          {
            "disease": "Prion Diseases",
            "terms": ["Prion disease", "transmissible spongiform encephalopathies", "TSE", "bovine spongiform encephalopathy", "BSE", "mad cow", "Creutzfeldt-Jakob disease", "CJD", "scrapie", "chronic wasting disease", "CWD"]
          },
          {
            "disease": "Respiratory Syncytial Virus (RSV)",
            "terms": ["Respiratory Syncytial Virus", "RSV"]
          },
          {
            "disease": "Rocky Mountain Spotted Fever",
            "terms": ["Rocky Mountain Spotted Fever", "Rickettsia rickettsii", "R. rickettsii"]
          },
          {
            "disease": "Schistosomiasis (Bilharzia)",
            "terms": ["Schistosomiasis", "Bilharzia", "Schistosoma", "schistosome", "Schistosoma mansoni", "Schistosoma haematobium", "Schistosoma japonicum", "S. mansoni", "S. haematobium", "S. japonicum"]
          },
          {
            "disease": "Sexually Transmitted Diseases",
            "terms": ["Sexually Transmitted Disease", "STD", "Sexually Transmitted infection", "STI", "gonorrhea", "Neisseria gonorrhoeae", "N. gonorrhoeae", "gonococcal", "gonococci", "genital herpes", "HSV", "human papillomavirus", "HPV",
              "HIV/AIDS", "HIV", "AIDS", "human immunodeficiency virus", "acquired immunodeficiency syndrome", "chlamydia", "Chlamydia trachomatis", "C. trachomatis", "syphilis", "Treponema pallidum", "T. pallidum", "trichomoniasis",
              "Trichomonas vaginalis", "T. vaginalis", "human genital ulcer disease", "chancroid", "Haemophilus ducreyi", "H. ducreyi", "Pelvic Inflammatory Disease", "PID", "Vaginitis", "vaginosis"
            ]
          },
          {
            "disease": "Shigellosis",
            "terms": ["Shigellosis", "Shigella", "Shiga toxin"]
          },
          {
            "disease": "Smallpox",
            "terms": ["Smallpox", "variola"]
          },
          {
            "disease": "STAT3 Dominant-Negative Disease",
            "terms": ["STAT3 Dominant-Negative Disease", "STAT3DN", "autosomal dominant hyper-IgE syndrome", "AD-HIES", "Job's Syndrome"]
          },
          {
            "disease": "Syphilis",
            "terms": ["syphilis", "Treponema pallidum", "T. pallidum", "chancre"]
          },
          {
            "disease": "Tickborne Diseases",
            "terms": ["Tickborne Diseases", "Babesiosis", "Babesia microti", "B. microti", "Ehrlichiosis", "Anaplasmosis", "Anaplasma phagocytophilum", "Ehrlichia chaffeensis", "A. phagocytophilum", "E. chaffeensis", "Lyme Disease",
              "Borrelia burgdorferi", "B. burgdorferi", "borreliosis", "Relapsing Fever", "Rocky Mountain Spotted Fever", "Rickettsia rickettsii", "R. rickettsii", "Tularemia", "Francisella tularensis", "F. tularensis"
            ]
          },
          {
            "disease": "Tuberculosis",
            "terms": ["Tuberculosis", "TB", "Mycobacterium tuberculosis", "M. tuberculosis", "Mtb"]
          },
          {
            "disease": "West Nile Virus",
            "terms": ["West Nile virus", "WNV"]
          },
          {
            "disease": "Zika Virus",
            "terms": ["Zika Virus", "Zika", "ZIKV"]
          }
        ]
      }
    },
    mounted: function() {
    },
    methods: {
      fetchData(diseaseObject) {
        this.loading = true;
        let searchTerms = diseaseObject.terms;

        var params = {
          "params": {
            "q": `"${searchTerms.join('" "')}"`, // make sure to enquote everything or else you'll search individual terms
            "size": 0,
            "facets": this.facets.join(","),
            "facet_size": this.facetSize
          }
        }

        return (
          rxjs.from(axios.get("{{api_url}}" + 'query?', params)).pipe(
            rxjs.operators.pluck("data"),
            rxjs.operators.pluck("facets"),
            rxjs.operators.tap(result => result['total'] = result['_index']['total']),
            rxjs.operators.tap(result => result['disease'] = diseaseObject.disease),
            rxjs.operators.tap(result => result['searchTerms'] = diseaseObject.terms),
            rxjs.operators.tap(result => result['query'] = `"${diseaseObject.terms.join('" "')}"`),
            rxjs.operators.tap(result => result['diseaseID'] = diseaseObject.disease.replace(/\s+/g, "-")),
            rxjs.operators.tap(result => result['funders_counts'] = combineFunders(result, 9, true)),
            rxjs.operators.tap(result => result['variable_count'] = result['variableMeasured.keyword']['terms'].map(d => {
              return({"key": d.term, "value": d.count})
            })),
            rxjs.operators.tap(result => result['technique_count'] = result['measurementTechnique.keyword']['terms'].map(d => {
              return({"key": d.term, "value": d.count})
            })),
            rxjs.operators.tap(result => result['source_counts'] = cleanSources(result['_index']['terms']))
          )
        );
      },
      calcOpacity(keywordPair, allKeywords, lowerLimit = 0.3, logValues = true) {
        var self = this;
          let limits = d3.extent(allKeywords.map(d => d.count));

          let opacityScale;
          if (logValues) {
            opacityScale = d3.scaleLog().domain(limits).range([lowerLimit, 1]);
          } else {
            opacityScale = d3.scaleLinear().domain(limits).range([lowerLimit, 1]);
          }
          return (opacityScale(keywordPair.count))
      },
      textColorScale(value) {
        let color = this.colorScale(value);

        return chroma.contrast(color, 'white') >= 2.5 ? "light" : "dark";
      }
    },
    observableMethods: {


    },
    subscriptions() {
      return {
        results: rxjs.forkJoin(...this.diseaseKeywords.map(this.fetchData)).pipe(
          rxjs.operators.tap(results => results.sort((a, b) => b.total - a.total)),
          rxjs.operators.tap(results => results.forEach(d => d['showTerms'] = false)),
          rxjs.operators.tap(x => console.log(x)),
          rxjs.operators.tap(results => this.numResults = results.length),
          rxjs.operators.tap(results => this.colorScale = d3.scaleOrdinal()
            .domain(results.map(d => d.disease))
            .range(d3.quantize(t => d3.interpolateSpectral(t * 0.8 + 0.1), results.length))),
          rxjs.operators.tap(_ => this.loading = false)
        )
      }
    }
  });
</script>
{% include "footer.html" %}
{% endblock %}
