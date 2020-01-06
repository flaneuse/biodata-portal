{% extends "main.html" %}
{% block content %}
{% include "header.html" %}
<style scoped>
  .search-term {
    opacity: 0.75;
    background: #ddd;
    padding: 1px 3px;
  }
</style>
<div id="niaid-diseases" class="container d-flex" style="min-height:100vh">
  <div v-if=loading class="loader">
    <img src="/static/img/ripple.svg" />
  </div>

  <div class="jumbotron bg-light text-muted w-100">
    <h1 class="row">Datasets containing NIAID priority diseases</h1>
    <app-bar-graph v-bind:counts="hardcoded"></app-bar-graph>
    <div class="d-flex flex-wrap">
      <div v-for="term in source_counts">
        <app-donut v-bind:source_counts="term" class="row"></app-donut>
      </div>
    </div>

    <app-treemap v-bind="{results}" v-if="results"></app-treemap>

    <div v-for="disease in results" :id="disease.diseaseID" v-if="results" class="row mb-5">
      <div class="col-sm-12">
        <h4 class="row" v-text="disease.disease"></h4>

        <template>
          <div class="row">
            <div v-text="disease.total.toLocaleString() + ' results'"></div>
            <a :href="'/search?q=' + disease.query" v-text="'view ' + disease.disease + ' datasets'" class="ml-3"></a>
          </div>
        </template>

        <div class="row">
          <small class="search-term mr-2 mb-1" v-for="term in disease.searchTerms.sort()">
            <span v-text="term"></span>
            <!-- <span>"</span><span v-text="term"></span><span>"</span> -->
          </small>
        </div>
<!-- <app-donut v-bind:source_counts="disease['source_counts']" class="row"></app-donut> -->

<!-- <app-donut source_counts="disease['source_counts']" class="row" v-if="disease.source_counts"></app-donut> -->

<div class="row">
  <div class="col-sm-12 col-md-12 p-3">
    <h6 v-text="facetSize + ' most common keywords in datasets'"></h6>
    <div class="d-flex" id="keyword-counts">
      <div v-for="keywordPair in disease['keywords.keyword']['terms']" v-text="keywordPair.term" class="keyword-cloud" v-bind:style="{ opacity: calcOpacity(keywordPair, disease['keywords.keyword']['terms'])}">
      </div>
    </div>
</div>

        </div>

        <!-- <app-donut v-bind="{source_counts}" class="row"></app-donut> -->
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
<script src="/static/js/vue-rx.js"></script>
<script src="/static/js/clean-facets.js"></script>

<script type="module">
  var app = new Vue({
    el: '#niaid-diseases',
    name: "NIAID-diseases",
    components: {
  'app-treemap': window.httpVueLoader('/static/components/Treemap.vue'),
  'app-donut': window.httpVueLoader('/static/components/Donut.vue'),
  'app-bar-graph': window.httpVueLoader('/static/components/BarGraph.vue')
},
    data: function() {
      return {
        hardcoded: [{"count":13,"term":"GM/NIGMS NIH HHS"},{"count":4,"term":"AR/NIAMS NIH HHS"},{"count":4,"term":"Biotechnology and Biological Sciences Research Council"},{"count":3,"term":"EB/NIBIB NIH HHS"},{"count":3,"term":"PHS HHS"},{"count":2,"term":"AI/NIAID NIH HHS"},{"count":2,"term":"CA/NCI NIH HHS"},{"count":2,"term":"EY/NEI NIH HHS"},{"count":1,"term":"Canadian Institutes of Health Research (CIHR)"},{"count":1,"term":"DK/NIDDK NIH HHS"}],
        source_counts: [[{"key":"omicsdi","value":7515},{"key":"ncbi geo","value":1227},{"key":"zenodo","value":55},{"key":"harvard dataverse","value":10}],[{"key":"omicsdi","value":4202},{"key":"ncbi geo","value":888},{"key":"zenodo","value":14},{"key":"harvard dataverse","value":3}],[{"key":"omicsdi","value":4084},{"key":"ncbi geo","value":869},{"key":"zenodo","value":56},{"key":"harvard dataverse","value":57}],[{"key":"omicsdi","value":4184},{"key":"ncbi geo","value":554},{"key":"zenodo","value":4},{"key":"harvard dataverse","value":2}],[{"key":"omicsdi","value":2627},{"key":"ncbi geo","value":1040},{"key":"harvard dataverse","value":817},{"key":"zenodo","value":80}],[{"key":"omicsdi","value":1933},{"key":"ncbi geo","value":1213},{"key":"zenodo","value":20},{"key":"harvard dataverse","value":7}],[{"key":"omicsdi","value":1336},{"key":"ncbi geo","value":671},{"key":"harvard dataverse","value":789},{"key":"zenodo","value":44}],[{"key":"omicsdi","value":1640},{"key":"ncbi geo","value":442},{"key":"zenodo","value":109},{"key":"harvard dataverse","value":96}],[{"key":"omicsdi","value":1237},{"key":"ncbi geo","value":600},{"key":"zenodo","value":33},{"key":"harvard dataverse","value":48}],[{"key":"omicsdi","value":1000},{"key":"ncbi geo","value":514},{"key":"zenodo","value":18},{"key":"harvard dataverse","value":29}],[{"key":"omicsdi","value":612},{"key":"ncbi geo","value":351},{"key":"harvard dataverse","value":44},{"key":"zenodo","value":7}],[{"key":"omicsdi","value":800},{"key":"ncbi geo","value":125},{"key":"zenodo","value":6},{"key":"harvard dataverse","value":7}],[{"key":"omicsdi","value":565},{"key":"ncbi geo","value":298},{"key":"zenodo","value":5},{"key":"harvard dataverse","value":4}],[{"key":"omicsdi","value":487},{"key":"ncbi geo","value":92},{"key":"zenodo","value":2}],[{"key":"omicsdi","value":344},{"key":"ncbi geo","value":99},{"key":"zenodo","value":1}],[{"key":"omicsdi","value":377},{"key":"ncbi geo","value":56},{"key":"zenodo","value":7},{"key":"harvard dataverse","value":1}],[{"key":"omicsdi","value":315},{"key":"ncbi geo","value":110},{"key":"zenodo","value":5},{"key":"harvard dataverse","value":1}],[{"key":"omicsdi","value":346},{"key":"ncbi geo","value":55},{"key":"zenodo","value":3},{"key":"harvard dataverse","value":2}],[{"key":"omicsdi","value":246},{"key":"ncbi geo","value":98},{"key":"zenodo","value":5},{"key":"harvard dataverse","value":3}],[{"key":"omicsdi","value":191},{"key":"ncbi geo","value":105},{"key":"zenodo","value":16},{"key":"harvard dataverse","value":9}],[{"key":"omicsdi","value":225},{"key":"ncbi geo","value":31},{"key":"zenodo","value":8},{"key":"harvard dataverse","value":1}],[{"key":"omicsdi","value":112},{"key":"zenodo","value":85},{"key":"ncbi geo","value":57},{"key":"harvard dataverse","value":9}],[{"key":"omicsdi","value":159},{"key":"ncbi geo","value":93},{"key":"zenodo","value":2},{"key":"harvard dataverse","value":1}],[{"key":"omicsdi","value":139},{"key":"ncbi geo","value":84},{"key":"zenodo","value":17},{"key":"harvard dataverse","value":5}],[{"key":"omicsdi","value":143},{"key":"ncbi geo","value":74},{"key":"harvard dataverse","value":7}],[{"key":"omicsdi","value":163},{"key":"ncbi geo","value":29},{"key":"harvard dataverse","value":19},{"key":"zenodo","value":1}],[{"key":"omicsdi","value":95},{"key":"ncbi geo","value":39},{"key":"zenodo","value":20},{"key":"harvard dataverse","value":14}],[{"key":"omicsdi","value":102},{"key":"ncbi geo","value":52}],[{"key":"omicsdi","value":100},{"key":"ncbi geo","value":37},{"key":"zenodo","value":1}],[{"key":"omicsdi","value":78},{"key":"ncbi geo","value":27},{"key":"harvard dataverse","value":1},{"key":"zenodo","value":1}],[{"key":"zenodo","value":40},{"key":"omicsdi","value":21},{"key":"ncbi geo","value":8},{"key":"harvard dataverse","value":2}],[{"key":"omicsdi","value":25},{"key":"ncbi geo","value":13},{"key":"zenodo","value":1}],[{"key":"omicsdi","value":31},{"key":"harvard dataverse","value":4},{"key":"ncbi geo","value":2}],[{"key":"omicsdi","value":28},{"key":"ncbi geo","value":5}],[{"key":"omicsdi","value":16},{"key":"ncbi geo","value":8},{"key":"harvard dataverse","value":5}],[{"key":"omicsdi","value":8},{"key":"ncbi geo","value":5}]],
        loading: false,
        facetSize: 10,
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
            "disease": "Primary Immune Deficiency Diseases (PIDDs)",
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
          rxjs.from(axios.get('http://su07:8080/api/query?', params)).pipe(
            rxjs.operators.pluck("data"),
            rxjs.operators.pluck("facets"),
            rxjs.operators.tap(result => result['total'] = result['_index']['total']),
            rxjs.operators.tap(result => result['disease'] = diseaseObject.disease),
            rxjs.operators.tap(result => result['searchTerms'] = diseaseObject.terms),
            rxjs.operators.tap(result => result['query'] = `"${diseaseObject.terms.join('" "')}"`),
            rxjs.operators.tap(result => result['diseaseID'] = diseaseObject.id),
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
      }
    },
    observableMethods: {


    },
    subscriptions() {
      return {
        results: rxjs.forkJoin(...this.diseaseKeywords.map(this.fetchData)).pipe(
          rxjs.operators.tap(results => results.sort((a, b) => b.total - a.total)),
          rxjs.operators.tap(x => console.log(x)),
          rxjs.operators.tap(x => this.loading = false)
        )
      }
    }
  });
</script>
{% include "footer.html" %}
{% endblock %}
