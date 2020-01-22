{% extends "main.html" %}
{% block content %}
{% include "header.html" %}

<div id="search-results" class="container d-flex" style="min-height:100vh">
  <div v-if=loading class="loader">
    <img src="static/img/ripple.svg" />
  </div>

<!-- SEARCH BAR, IF NO RESULTS -->
  <div class="jumbotron bg-light text-muted w-100" v-if="!numResults && numResults !== 0">
    <div class="jumbotron">

      <h1 class="mb-5">Search {{site_name}}</h1>
      <form class="row" @submit.prevent="search(query, 'queryChanged')">
        <input id="search-query" type="search" v-model='query' name="query" class="form-control mb-4 col-lg-4 col-md-6" placeholder="search datasets" autocomplete="off">
      </form>
    </div>
  </div>

  <div class="jumbotron bg-light text-muted w-100" v-if="numResults || numResults === 0">
    <!-- SEARCH, IF THERE ARE RESULTS -->
    <form class="row" @submit.prevent="search(query, 'queryChanged')">
      <input id="search-query" type="search" v-model='query' name="query" class="form-control mb-4 col-lg-4 col-md-6" placeholder="search datasets" autocomplete="off">
    </form>

    <div id="results-count" class="d-flex align-items-center mb-2 justify-content-between">
      <!-- RESULTS COUNT -->
      <h3 id="num-results">
        <template v-if="numResults">
          <span v-text="selectedMin"></span><span>-</span><span v-text="selectedMax"></span><span> of </span>
        </template>
        <span v-if="numResults === 10000"> over </span>
        <span v-text="numResults.toLocaleString()"></span>
        <span> results</span>
      </h3>

      <!-- PAGINATION -->
      <div id="pagination-page-size" class="pagination">
        Show
        <ul>
          <li v-for="(pageSize, index) in paginationOptions" v-if="pageSize <= numResults || index === 0 || paginationOptions[index-1] < numResults" v-bind:class="[ pageSize == selectedPerPage ? 'selected' : 'unselected' ]" :key="'page-size-' + pageSize">
            <a v-text="pageSize" v-on:click="changePageSize(pageSize)"></a>
          </li>
        </ul>
      </div>

    </div>


    <template v-show="results && results.length > 0" v-if="results && results.length > 0">

      <div class="row">
        <!-- facet filters -->
        <div id="filters" class="col-md-3 pr-4">
          <!-- clear filters button -->
          <small class="d-flex justify-content-end"><a @click.prevent="clearFilters()" href="">clear filters</a></small>


          <template v-if="facetSummary && facetSummary.length > 0">
            <!-- loop: filter form group for each facet variable -->
            <template v-for="variable in filteredFacetSummary" :key="'filter-' + varaible.variable">
              <!-- facet title -->
              <p class="facet-title" v-text="variable.variable"></p>

              <!-- filter the filters: search box -->
              <form class="facet-search whitefadedarker pt-1" @submit.prevent="selectFilterText(variable.variable)" @input.prevent="debounceFilterText(variable.variable)" v-if="variable.counts.length > 0">
                <small>
                  <input class="facet-search-box font-awesome" type="text" autocomplete="off" v-model='selectedFilterText[variable.variable]' name="selectedFilterText" :placeholder="`&#xF002; ${variable.variable}`"/>
                  </small>
              </form>

              <form class="facet-group whitefadedarker" @change.prevent="search(query, 'filtersChanged')">

                <!-- checkbox + label for each option -->
                <fieldset v-for="(count, index) in variable.counts" v-if="variable.counts.length > 0" :key="variable.variable + '-' + count.key">
                    <input class="facet-counts px-1" type="checkbox" :id="variable.variable + '-' + count.key" :value="count.key" :name="count.key" v-model="selectedFilters[variable.variable]">
                    <label :for="`${variable.variable}-${count.key}`">
                      <small v-html="`${count.key} (${count.value.toLocaleString()})`" :for="count.key"></small>
                  </label>
                </fieldset>

                <!-- show more option -->
                <small class="d-flex justify-content-end" v-if="variable.moreFacets">
                  <a @click.prevent="showMore(variable.variable)" href="" :id="`${variable.variable}_show-more`">
                    more
                  </a>
                </small>
              </form>
            </template>
          </template>
        </div>

        <div id="results" class="col-md-9">
          <div v-for="item in results" class="row py-3 result-summary" :key="item['_id']">
            <div class="col-md-4 text-left">
              <!-- name -->
              <a :href="item._id" target="_blank" rel="noreferrer">
                <h5 v-text="item.name" class="row" v-if="item.name"></h5>
                <h5 v-text="'Unnamed dataset'" class="row" v-if="!item.name"></h5>
              </a>

              <!-- other short properties -->
              <div class="dataset-properties">
                <div id="credit" class="row" v-if="item.credit || item.creator || item.author || item.publisher || item.provider">
                  <!-- creator / author -->
                  <div id="creator" v-if="item.credit">
                    <template v-if="item.authorsExpanded">
                      <div v-text="author.name" v-for="author in item.credit"></div>
                      <a class="show-more" href="#" @click.prevent="item.authorsExpanded=false">hide authors</a>
                    </template>
                    <template v-else>
                      <span v-text="item.credit[0].name"></span>
                      <template v-if="item.credit.length > 1">
                      <i> et al.</i>
                      <a class="show-more" href="#" @click.prevent="item.authorsExpanded=true">see all</a>
                      </template>
                    </template>

                  </div>

                  <!-- affiliation -->
                  <div id="creator-affiliation" v-text="item.creator[0].affiliation" v-if="item.creator && item.creator[0] && item.creator[0].affiliation">
                  </div>
                  <div id="creator-affiliation" v-text="item.author[0].affiliation" v-else-if="item.author && item.author[0] && item.author[0].affiliation">
                  </div>
                  <div id="publisher" v-text="item.publisher.name" v-else-if="item.publisher"></div>
                  <div id="provider" v-text="item.provider.name" v-else-if="item.provider"></div>

                  <!-- citation -->
                  <div id="citation" class="citation mainTextDark" v-if="item.citation">
                    <template v-if="Array.isArray(item.citation)">
                      <span v-for="(citation, name) in item.citation" v-text="citation" :key="name"></span>
                    </template>
                    <template v-else>
                      <span v-text="item.citation"></span>
                    </template>
                  </div>
                </div>

                <div id="funding" class="row" v-if="item.funding || item.funder">
                  <p class="mb-0">
                    Funded by:
                  </p>

                  <template v-if="item.fundingExpanded">
                    <template v-if="Array.isArray(item.funding)">
                      <div v-for="(funding, name) in item.funding" :key="name" class="funding-group">
                        <span class="funding-name" v-text="funding.funder.name" v-if="funding.funder.name"></span>
                        <a class="funding-name" v-text="funding.identifier" :href="'http://grantome.com/grant/NIH/' + funding.identifier" v-if="funding.identifier" target="_blank" rel="noreferrer"></a>
                      </div>
                    </template>
                    <template v-if="Array.isArray(item.funder)">
                      <div v-for="(funder, name) in item.funder" :key="name" class="funding-group">
                        <span class="funding-name" v-text="funder.name"  v-if="funder.name"></span>
                      </div>
                    </template>

                    <a class="show-more" v-if="item.fundersTooLong" href="#" @click.prevent="item.fundingExpanded=false">see fewer</a>
                  </template>
                  <template v-else>
                    <template v-if="Array.isArray(item.funding)">
                      <div v-for="(funding, index) in item.funding" class="funding-group" v-if="index < 2">
                        <span class="funding-name" v-text="funding.funder.name" v-if="funding.funder.name"></span>
                        <a class="funding-name" v-text="funding.identifier" :href="'http://grantome.com/grant/NIH/' + funding.identifier" v-if="funding.identifier" target="_blank" rel="noreferrer"></a>
                      </div>
                    </template>
                    <template v-if="Array.isArray(item.funder)">
                      <div v-for="(funder, index) in item.funder" class="funding-group"  v-if="index < 2">
                        <span class="funding-name" v-text="funder.name"  v-if="funder.name"></span>
                      </div>
                    </template>

                    <a class="show-more" href="#" @click.prevent="item.fundingExpanded=true" v-if="item.fundersTooLong">see all</a>
                  </template>
                </div>

                <div id="source">
                    view on <a :href="item['_id']" target="_blank" rel="noreferrer"><span v-text="item['sourceIndex']"></span></a>
                </div>

                <!-- dates -->
                <div id="dateModified" v-if="item.dateModified"><span style="padding-right:4px">updated</span><span v-text="item.dateModified"></span></div>
                <!-- <div id="dateModified" class="row" v-if="item.dateModified | moment('dddd, MMMM Do YYYY')"><span style="padding-right:4px">updated</span><span v-text="item.dateModified"></span></div> -->
                <div id="datePublished" v-if="item.datePublished"><span style="padding-right:4px">published</span><span v-text="item.datePublished"></span></div>

                <!-- license -->
                <div id="license" v-if="item.license && item.license.text">
                  <a target="_blank" :href="item.license.url" v-html="item.license.text">link</a>
                </div>
              </div>
            </div>

            <!-- description -->
            <div class="col-md-8 text-left" id="description">
              <a :href="item['_id']" target="_blank" rel="noreferrer">
                <img v-for="repo in {{repo_objects}}" class="repo-icon float-right" :data-tippy-info="`View on ${repo.name}`" :src="repo.img_src" v-if="item['_index'].includes(repo.id)"/>
              </a>

              <template v-if="item.descriptionExpanded">
                <span v-html="item.longDescription"></span>
                <span><a class="show-more" v-if="item.descriptionTooLong" href="#" @click.prevent="item.descriptionExpanded=false">(show less)</a></span>
              </template>
              <template v-else>
                <span v-html="item.shortDescription"></span>
                <span v-if="item.descriptionTooLong">... <a class="show-more" href="#" @click.prevent="item.descriptionExpanded=true">(show more)</a></span>
              </template>
            </div>

            <!-- measurementTechnique -->
            <div class="col-md-12">
              <div class="row d-flex justify-content-end" id="variableMeasured" v-if="item.variableMeasured || item.measurementTechnique">
                <!-- variableMeasured -->
                <template v-if="Array.isArray(item.variableMeasured)">
                  <small :data-tippy-info='`Search for "${measurement}"`' class="launch-search measurement mainBackDark" v-text="measurement" v-for="(measurement, name) in item.variableMeasured" :key="name" @click.prevent="search(measurement, 'queryChanged', true)">
                  </small>
                </template>
                <small :data-tippy-info='`Search for "${item.variableMeasured}"`' class="launch-search measurement mainBackDark" v-else v-text="item.variableMeasured" v-if="item.variableMeasured"
                  @click.prevent="search(item.variableMeasured, 'queryChanged', true)">
                </small>

                <!-- measurementTechnique -->
                <template v-if="Array.isArray(item.measurementTechnique)">
                  <small :data-tippy-info='`Search for "${measurement}"`' class="launch-search measurement mainBackDark" v-text="measurement" v-for="(measurement, name) in item.measurementTechnique" :key="name" @click.prevent="search(measurement, 'queryChanged', true)">
                  </small>
                </template>
                <small :data-tippy-info='`Search for "${item.measurementTechnique}"`' class="launch-search measurement mainBackDark" v-else v-text="item.measurementTechnique" v-if="item.measurementTechnique"
                  @click.prevent="search(item.measurementTechnique, 'queryChanged', true)">
                </small>
              </div>
            </div>

            <!-- keywords -->
            <div class="col-md-12">
              <div class="row d-flex justify-content-end" id="keywords" v-if="item.keywords">
                <template v-if="Array.isArray(item.keywords)">
                  <small :data-tippy-info='`Search for "${keyword}"`' class="launch-search keyword keyword-arr mainBackLight" v-text="keyword" v-for="(keyword, name) in item.keywords" :key="name" @click.prevent="search(keyword, 'queryChanged', true)">
                  </small>
                </template>
                <small :data-tippy-info='`Search for "${item.keywords}"`' class="launch-search keyword keyword-str mainBackLight" v-text="item.keywords" @click.prevent="search(item.keywords, 'queryChanged', true)" v-else>
                </small>
              </div>
            </div>
          </div>

        </div>

      </div>
  </div>

  <nav class="row m-auto d-flex justify-content-center" id="pagination">
    <ul class="pagination m-2 flex-wrap p-2">
      <li class="page-item" :class="{ 'disabled': selectedPage <= 1 }">
        <a class="page-link" @click.prevent="prevPage()">&lt;</a>
      </li>
      <li class="page-item" :class="{ 'active': selectedPage == 1, 'bg-primary': selectedPage == 1, 'white-text': selectedPage == 1  }">
        <a href="#" class="page-link" @click.prevent="changePageNumber(1)">1</a>
      </li>
      <li class="page-item disabled" v-if="selectedPage > 3 && pages > 4">
        ...
      </li>
      <li class="page-item" :class="{ 'active': selectedPage == n, 'bg-primary': selectedPage == n, 'white-text': selectedPage == n  }" v-for="n in pages" :key="n"
        v-if="n !== 1 && n !== pages && ((n >= selectedPage - 1 && n <= selectedPage + 1) || (n <=4 && selectedPage <= n) || (n >= pages - 3 && selectedPage >= pages - 1))">
        <a href="#" class="page-link" @click.prevent="changePageNumber(n)" v-text="n"></a>
      </li>
      <li class="page-item disabled" v-if="(selectedPage < pages - 2) && pages > 4">
        ...
      </li>
      <li class="page-item" :class="{ 'active': selectedPage == pages, 'bg-primary': selectedPage == pages, 'white-text': selectedPage == pages  }" v-if="pages !== 1">
        <a href="#" class="page-link" @click.prevent="changePageNumber(pages)" v-text="pages"></a>
      </li>
      <li class="page-item" :class="{ 'disabled': selectedPage >= pages }">
        <a class="page-link" @click.prevent="nextPage()">&gt;</a>
      </li>
    </ul>
  </nav>
  </template>


</div>
</div>
{% endblock %}

{% block extra_scripts %}
<script src="https://unpkg.com/vuex"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/vue/2.4.2/vue.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/axios/0.18.0/axios.min.js"></script>
<script src="https://unpkg.com/vue-router"></script>
<script src="https://d3js.org/d3.v5.min.js"></script>
<script src="static/js/clean-facets.js"></script>
<script src="https://unpkg.com/tippy.js@3/dist/tippy.all.min.js"></script>
<!-- <script src="https://cdn.jsdelivr.net/npm/sweetalert2@7.28.11/dist/sweetalert2.all.min.js"></script> -->
<script>
var router = new VueRouter({
  mode: 'history',
  routes: [{
    path: '/search/:q',
    component: app,
    props: (route) => ({
      query: route.query.q
    })
  }],
});

const store = new Vuex.Store({
  state: {
    'metadata': {},
  },
  strict: true,
  mutations: {
    saveMetadata(state, payload) {
      state.metadata = payload['metadata']
    },
  },
  getters: {
    // exposed as store.getters.nameOfGetter
    getMetadata: state => {
      return state.metadata
    },
  }
});

var app = new Vue({
  el: '#search-results',
  name: "search-results",
  router: router,
  data: function() {
    return {
      query: "",
      loading: false,
      maxDescriptionLength: 75,

      pages: 1,
      paginationOptions: [10, 25, 50],
      defaultPerPage: 10,
      selectedPerPage: 10,
      selectedPage: 1,

      numResults: null,
      results: [],

      facetSize: 1000,
      facetsPerShowMore: 5,
      selectedFacetSize: {
        "funder": 5,
        "source": 5,
        "variableMeasured": 5,
        "measurementTechnique": 5,
        "keywords": 5
      },
      facets: ["funder.name.keyword", "funding.funder.name.keyword", "_index", "variableMeasured.keyword", "measurementTechnique.keyword", "keywords.keyword"],
      selectedFilters: {
        "funder": [],
        "source": [],
        "variableMeasured": [],
        "measurementTechnique": [],
        "keywords": []
      },
      selectedFilterText: {
        "funder": null,
        "source": null,
        "variableMeasured": null,
        "measurementTechnique": null,
        "keywords": null
      },
      facetSummary: [],
      // filteredFacetSummary: []
    }
  },
  computed: {
    selectedMin: function() {
      return (this.selectedPage - 1) * this.selectedPerPage + 1;
    },
    selectedMax: function() {
      var maxValue = this.selectedPage * this.selectedPerPage;
      return maxValue <= this.numResults ? maxValue : this.numResults;
    },
    filteredFacetSummary: function() {
      let filtered = this.facetSummary.map(facet => {
        let selectedVar = this.selectedFilterText[facet.variable];
        selectedVar = selectedVar ? selectedVar.toLowerCase() : "";
        return ({
          'counts': facet.counts.filter(d => d.key.toLowerCase().includes(selectedVar)).slice(0, this.selectedFacetSize[facet.variable]),
          'variable': facet.variable,
          'moreFacets': facet.counts.length > this.selectedFacetSize[facet.variable]
        })
      })

      return (filtered);
    },
  },
  watch: {
    $route(to, from) {
      let queryChanged = to.query.q !== from.query.q || to.query.filters !== from.query.filters;
      // If query changed between routes (either because query or filters were changed), re-call the facet function to summarize the counts per keyword, funder, etc.
      this.executeSearch(queryChanged);
    }
  },
  mounted: function() {
    this.executeSearch();


    tippy('body', {
      target: '.launch-search',
      content: 'Loading...',
      maxWidth: '200px',
      placement: 'bottom',
      animation: 'fade',
      theme: 'light',
      onShow(instance) {
        let info = instance.reference.dataset.tippyInfo;
        instance.setContent("<div class='text-muted m-0'>" + info + "</div>")
      }
    });

    tippy('div', {
      target: '.repo-icon',
      content: 'Loading...',
      maxWidth: '200px',
      placement: 'bottom',
      animation: 'fade',
      theme: 'light',
      onShow(instance) {
        let info = instance.reference.dataset.tippyInfo;
        instance.setContent("<div class='text-muted m-0'>" + info + "</div>")
      }
    });
  },
  created: function() {
    this.debounceFilterText = _.debounce(this.selectFilterText, 500);
  },
  methods: {
    resetFilters() {
      this.selectedFilters = {
        "funder": [],
        "source": [],
        "variableMeasured": [],
        "measurementTechnique": [],
        "keywords": []
      };

      this.selectedFacetSize = {
        "funder": 5,
        "source": 5,
        "variableMeasured": 5,
        "measurementTechnique": 5,
        "keywords": 5
      };

      this.selectedFilterText = {
        "funder": null,
        "source": null,
        "variableMeasured": null,
        "measurementTechnique": null,
        "keywords": null
      }
    },
    clearFilters() {
      this.resetFilters();

      this.search(this.query, 'filtersChanged');
    },
    showMore(variableName) {
      this.selectedFacetSize[variableName] += this.facetsPerShowMore;
    },
    changePageSize(selectedSize) {
      let self = this;
      self.selectedPerPage = selectedSize;

      self.search(self.query, "pageChanged");
    },
    changePageNumber(pageNumber) {
      let self = this;
      self.selectedPage = pageNumber;

      self.search(self.query, "pageChanged");
    },
    calculatePages: function() {
      var self = this;
      self.pages = Math.ceil(self.numResults / self.selectedPerPage);
    },
    prevPage: function() {
      var self = this;
      if (self.selectedPage > 1)
        self.selectedPage -= 1
      self.search(self.query, "pageChanged");
    },
    nextPage: function() {
      var self = this;
      if (self.selectedPage < self.pages)
        self.selectedPage += 1
      self.search(self.query, "pageChanged");
    },
    selectFilterText(variableName) {
      let selectedText = this.selectedFilterText[variableName].toLowerCase();
      if (selectedText !== "") {
        let selected = this.facetSummary.filter(d => d.variable === variableName)[0].counts.filter(d => d.key.toLowerCase().includes(selectedText));
        this.selectedFilters[variableName] = selected.map(d => d.key);
      } else {
        this.selectedFilters[variableName] = [];
      }
      this.search(this.query, "filtersChanged");
    },
    // Logic to get which person to display as the author
    getAuthors(item) {
      // (1): creator
      if(item.creator) {
        if(Array.isArray(item.creator)) {
          return(item.creator);
        } else {
          return([item.creator]);
        }
      }
      // (2): author
      if(item.author) {
        if(Array.isArray(item.author)) {
          return(item.author);
        } else {
          return([item.author]);
        }
      }
    },
    search(query, queryType, enquoteQuery = false) {
      var self = this;

      var queryText = query ? (enquoteQuery ? `"${query}"` : query) : "__all__";

      // reset pagination, filters if there's a new query
      if (queryType === "queryChanged") {
        self.query = queryText;
        self.selectedPerPage = self.defaultPerPage;
        self.selectedPage = 1;
        this.resetFilters();
      } else if (queryType === "filtersChanged") {
        self.selectedPerPage = self.defaultPerPage;
        self.selectedPage = 1;
      } else if (queryType === "pageChanged") {}

      if (query) {
        // update route url
        this.$router.push({
          path: "/search",
          query: {
            q: self.query,
            filters: getQueryFilters(self.selectedFilters),
            size: self.selectedPerPage,
            from: self.selectedPage
          }
        }).catch(err => {});
      }
    },
    executeSearch(queryChanged = true) {
      var self = this;
      self.query = self.$route.query.q;

      if (self.query) {
        self.selectedPerPage = self.$route.query.size ? self.$route.query.size : self.defaultPerPage;
        self.selectedPage = self.$route.query.from ? self.$route.query.from : 1;

        var queryText = self.query ? self.query : "__all__";

        // pull out the applied filter string and convert to an object.
        self.selectedFilters = filterString2Obj(self.$route.query.filters);

        // if (Object.values(self.selectedFilters).flatMap(d => d).length > 0) {
        // let selectedFilters = getQueryFilters(self.selectedFilters);
        if (self.$route.query.filters) {
          queryText = queryText === "__all__" ? self.$route.query.filters : `(${queryText}) AND ${self.$route.query.filters}`;
        }

        var params = {
          "params": {
            "q": queryText,
            "size": self.selectedPerPage,
            "from": (self.selectedPage - 1) * self.selectedPerPage,
          }
        };

        var facetParams = {
          "params": {
            "q": queryText,
            "facet_size": this.facetSize,
            "facets": this.facets.join(","),
          }
        };

        self.loading = true;

        self.results = [];

        // TODO: set in config
        axios.get("{{api_url}}" + 'query?', params).then(function(response) {
          console.log(`%c searching ${self.query}...`, 'color:hotpink')
          // console.log(response)
          console.log(response.data.hits)

          // Standardize descriptions. NOTE: needs to be done before assign to <this> to ensure proper change detection.
          response.data.hits.forEach(d => {
            if (Array.isArray(d.description)) {
              d['longDescription'] = d.description.join("<br/>");
            } else {
              d['longDescription'] = d.description;
            }
            let descriptionArray = d.longDescription.split(" ");
            d['shortDescription'] = descriptionArray.slice(0, self.maxDescriptionLength).join(" ");
            d['descriptionTooLong'] = descriptionArray.length >= self.maxDescriptionLength;
            d['fundersTooLong'] = (d.funding && d.funding.length > 2) || (d.funder && d.funder.length > 2);
            d['credit'] = self.getAuthors(d);
            d['descriptionExpanded'] = false;
            d['authorsExpanded'] = false;
            d['fundingExpanded'] = !((d.funding && d.funding.length > 2) || (d.funder && d.funder.length > 2));
            d['sourceIndex'] = cleanSourceName(d['_index']);
          })

          self.results = response.data.hits;
          self.numResults = response.data.total.value;

          if (self.numResults) {
            self.calculatePages();
          }

          self.loading = false;
        });

        // TODO: promise-ize this.
        if (queryChanged) {
          axios.get("{{api_url}}" + 'query?', facetParams).then(function(response) {
            let allResults = cleanFacets(response.data.facets, self.facetSize);

            // console.log(response.data.facets)
            // console.log(allResults)
            self.facetSummary = allResults;
            self.loading = false;
          });
        }
      }

    }
  }
});
</script>
<style>
  #results-count h1 {
    margin-bottom: 0;
  }

  .pagination {
    display: inline-flex;
  }

  .pagination ul {
    list-style-type: none;
    margin-bottom: 0;
  }

  .pagination li {
    display: inline-block;
    margin-right: 5px;
    cursor: pointer;
  }

  #pagination-page-size li {
    margin-right: 25px;
  }

  .result-summary:first-of-type {
    padding-top: 0 !important;
  }

  .result-summary {
    border-bottom: 1px solid #BBB;
  }

  .disabled {
    opacity: 0.5;
  }

  .keyword,
  .measurement {
    padding: 3px 5px;
    border-radius: 0.3em;
    margin-left: 0.5em;
    margin-bottom: 0.5em;
    font-size: 0.75em;
    cursor: pointer;
    color: white;
    font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji";
  }

  .dataset-properties {
    font-size: 0.85em;
  }

  .measurement {
    color: white;
  }

  .citation {
    line-height: 1.2em;
  }

  #credit, #funding {
    border-bottom: 1px dashed #bbb;
    padding-bottom: 2px;
    margin-bottom: 5px;
    flex-direction: column;
  }

  .facet-group {
    margin-bottom: 15px;
    border-bottom: 1px solid;
  }

  .facet-title {
    font-size: 0.9em;
    font-weight: 400;
    background: #ddd;
    border-top: 1px solid;
    border-bottom: 1px solid;
  }

  .facet-title,
  .facet-group fieldset {
    padding: 0 0.5em;
  }

  .facet-counts {
    line-height: .8em;
    margin-bottom: 0.4em;
  }

  .facet-counts small {
    font-weight: 300;
  }

  .repo-icon {
    height: 30px;
  }

  form.facet-search {
    padding: 0 0.5em;
}

  input.facet-search-box {
    width: 100%;
    color: #495057;
    border: 1px solid #ced4da;
    border-radius: 0.25rem;
    padding: 0.125rem 0.55rem;
}
</style>
{% include "footer.html" %}
{% endblock %}
