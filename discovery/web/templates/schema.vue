{% extends "main.html" %}
{% block content %}
{% include "header.html" %}
<div id="schema" class="container d-flex" style="min-height:100vh">
  <div v-if=loading class="loader">
    <img src="static/img/ripple.svg" />
  </div>
  <div class="jumbotron bg-light text-muted w-100">
    <div class="jumbotron bg-light bg-animated">
      <h1 class="text-center text-muted test">Dataset schema in <span class="logoText">{{site_name}}</span></h1>
    </div>
    <div>
      <p>
        A critical part of assembling datasets from different sources is making sure that they
        use a common schema to describe these datasets.
      </p>
      <p>
        We rely on <a href="http://schema.org/Dataset" rel="noreferrer" target="_blank">schema.org's Dataset schema</a>, but each source uses the standard differently. <a href="https://discovery.biothings.io/view/niaid/" target="_blank" rel="noreferrer"><small class="badge badge-pill badge-secondary pointer">View NIAID's Minimal Dataset Schema</small></a>
      </p>
    </div>
    <div class="pt-5 pb-5 text-center">
      <h4 v-if="results">
        There are <span class="mainTextLight" v-text="schemaTotal"></span> schema.org Dataset properties
      </h4>
    </div>
    <div class="pt-5 pb-5 text-center">
      <h4 v-if="results">
        ... but only <span class="mainTextLight" v-text="results.filter(d => d.total).length"></span> are used by any of our dataset repositories.
      </h4>
    </div>
    <div class="d-flex flex-wrap justify-content-between">
      <div>

      <svg id="heatmap" class='heatmap' :width='width + margin.left + margin.right' :height='height + margin.top + margin.bottom' class="mr-5">
        <defs>
          <linearGradient id="gradient-legend" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop v-for="n in 10" :key="n" :offset="(n/10)*100 + '%'" :style="`stop-color:${colorScheme(n/10)}; stop-opacity:1`" />
          </linearGradient>
        </defs>

        <!-- legend -->
        <g id="color-legend" transform='translate(0, -10)'>
          <rect width="15" height="15" :y="margin.top - 5" :style="`fill: ${colorScheme(0)}; stroke: ${colorScheme(1)}`"></rect>
          <line :x1="0" :x2="15" :y1="margin.top - 5 + 15" :y2="margin.top - 5" class="slash-line" />
          <text :x="20" :y="margin.top - 5" class="legend-title">not used</text>

          <text :x="0" :y="margin.top - 60" class="legend-title">prevalence in source</text>
          <rect :width="margin.left - 7" height="15" :y="margin.top - 45"fill="url(#gradient-legend)" :style="`stroke: ${colorScheme(1)}`"></rect>
          <text :x="margin.left - 7" :y="margin.top - 27" class="legend-label legend-label--max">100%</text>
          <text :x="0" :y="margin.top - 27" class="legend-label legend-label--min">0</text>
        </g>

        <!-- blank chiclets to represent no data -->
        <g :transform='`translate(${this.margin.left}, ${this.margin.top})`' id="nodata-heatmap">
          <g v-for="property in results" class="property-row" :key="property.property + '_group'">
            <g v-for="repo in repos" :key="property.property + '-' + repo + '-nodata'">
              <rect :data-tippy-info="`<b>NO</b> datasets in <b>${repo}</b> use <b>${property.property}</b>`" :id="property.property + '-' + repo + '-nodata'" class="chiclet no-data" :x="x(repo)" :y="y(property.property)" :width="x.bandwidth()" :height="y.bandwidth()" :fill="colorScheme(0)"></rect>
              <line :x1="x(repo) + 3" :x2="x(repo) - 3 + x.bandwidth()" :y1="y(property.property) + y.bandwidth()" :y2="y(property.property)" class="slash-line" />
              </g>
          </g>
        </g>

        <!-- heatmap of actual data -->
        <g :transform='`translate(${this.margin.left}, ${this.margin.top})`' id="heatmap-chart">
          <g v-for="property in results" :id="property.property + '-data'" class="property-row" :id="property.property + '-' + repo + '-data'">
              <rect :data-tippy-info="repo.key === 'AVERAGE' ? `<b>${repo.percent.toLocaleString(undefined, {style:'percent'})}</b> of datasets use <b>${property.property}</b> on average` :
              `<b>${repo.percent.toLocaleString(undefined, {style:'percent'})}</b> of datasets in <b>${repo.key}</b> use <b>${property.property}</b>`"
              v-for="repo in property.counts" :key="property.property + '-' + repo.key" :id="property.property + '-' + repo.key" class="chiclet" :x="repo.x" :y="repo.y" :fill="repo.fill" :width="x.bandwidth()" :height="y.bandwidth()"></rect>
          </g>
        </g>

        <!-- container for axes -->
        <g ref='xAxis' class="axis axis--x" :transform='`translate(${margin.left}, ${this.margin.top + 5})`' />
        <g ref='yAxis' class="axis axis--y" :transform='`translate(${margin.left}, ${this.margin.top})`' />
        <g ref='xAxisBottom' class="axis axis--x axis--x-bottom" :transform='`translate(${margin.left}, ${this.margin.bottom + height - 5})`' />
        <g ref='yAxisRight' class="axis axis--y axis--y-right" :transform='`translate(${margin.left + width}, ${this.margin.top})`' />
      </svg>
    </div>

      <div id="schema-explanation" class="ml-2">
        <p>
          As part of the {{ site_name }} project, we coerce metadata about each of the datasets pulled from the repositories into a common format, based off of <a href="http://schema.org/Dataset" rel="noreferrer" target="_blank">schema.org's Dataset schema</a>.
        </p>
        <p>
          This schema is intended to be descriptive and flexible, encompassing 119 different properties. But not all of these properties are used equally within the repositories &mdash; or even at all.
        </p>
        <p>
        <span v-if="results" v-text="'Only ' + results.filter(d => d.total).length + ' properties are used at least once in any of the repositories. '"></span>
        Of those, only the <b>description</b> and <b>name</b> are nearly universally used. In other cases, a property is required in some data sources but absent in the others, like <b>variableMeasured</b> in omicsdi. For some variables, there seems to be a consensus on which synonym tends to be used: <b>citation</b> is commonly used, despite the fact that there is a similar property, <b>publication</b>, available in the schema.
        </p>
        <p>
          To promote greater uniformity in how biological datasets are described in their metadata, the NIAID Data Dissemination Working Group has developed a <a href="https://discovery.biothings.io/view/niaid/" target="_blank" rel="noreferrer">NIAID-specific dataset schema</a>. This schema focuses on a minimal set of metadata in the schema.org Dataset standard that we consider essential to describe and find biolgical datasets. Additionally, the schema extends the schema.org schema to add a few new properties specific to biological datasets.
        </p>

        <p class="mt-4">

          <a href="https://discovery.biothings.io/view/niaid/" target="_blank" rel="noreferrer"><small class="badge badge-pill badge-secondary pointer">View NIAID's Minimal Dataset Schema</small></a>
          <a href="https://discovery.biothings.io/guide/niaid/" target="_blank" rel="noreferrer"><small class="badge badge-pill badge-secondary pointer">Register a Dataset</small></a>
          <a href="about#sources"><small class="badge badge-pill badge-secondary pointer">View data sources</small></a>
        </p>
      </div>

    </div>

</div>
</div>
{% endblock %}

{% block extra_scripts %}
<script src="https://unpkg.com/vuex"></script>
<script src = "https://cdnjs.cloudflare.com/ajax/libs/vue/2.4.2/vue.min.js"></script>
<script src="https://unpkg.com/rxjs/bundles/rxjs.umd.js"></script>
<script src = "https://unpkg.com/vue/dist/vue.js"></script>
<script src="static/js/vue-rx.js"></script>
<script src = "https://cdnjs.cloudflare.com/ajax/libs/axios/0.18.0/axios.min.js" ></script>
<script src = "https://d3js.org/d3.v5.min.js" ></script>
<script src = "static/js/clean-facets.js" ></script>
<script src="https://unpkg.com/tippy.js@3/dist/tippy.all.min.js"></script>

  <script type = "module">
  var app = new Vue({
    el: '#schema',
    name: "Schema",

    data: function() {
      return {
        loading: false,
        filterZeros: true,

        chicletSize: 25,
        schemaTotal: 0,
        width: 0,
        height: 0,
        margin: {
          top: 75,
          right: 120,
          bottom: 75,
          left: 120
        },
        // colorScheme: d3.interpolateMagma,
        colorScheme: d3.interpolateYlGnBu,
        x: d3.scaleBand(),
        y: d3.scaleBand(),

        // repos: ["Harvard Dataverse", "NCBI GEO", "Zenodo", "Omics DI", "AVERAGE"],
        repos: {{repo_names}}.concat("AVERAGE"),
        // add in funding
        properties: ["text", "alternativeHeadline", "interactivityType", "expires", "catalog", "accessModeSufficient", "video", "schemaVersion", "additionalType", "review", "workTranslation", "author", "potentialAction", "workExample",
          "isBasedOn", "contentRating", "encodings", "publisher", "comment", "educationalUse", "isAccessibleForFree", "datasetTimeInterval", "thumbnailUrl", "genre", "variablesMeasured", "accountablePerson", "accessibilityControl", "funder",
          "isPartOf", "publication", "provider", "version", "fileFormat", "contributor", "accessibilityHazard", "publisherImprint", "contentReferenceTime", "accessMode", "awards", "reviews", "conditionsOfAccess", "abstract", "producer",
          "image", "contentLocation", "typicalAgeRange", "mainEntityOfPage", "audience", "alternateName", "sameAs", "exampleOfWork", "variableMeasured", "position", "accessibilityFeature", "mainEntity", "translationOfWork", "materialExtent",
          "correction", "dateCreated", "accessibilitySummary", "sdDatePublished", "issn", "headline", "distribution", "spatial", "hasPart", "editor", "name", "copyrightHolder", "identifier", "encodingFormat", "locationCreated", "award",
          "subjectOf", "mentions", "associatedMedia", "license", "keywords", "creator", "isFamilyFriendly", "includedDataCatalog", "temporalCoverage", "isBasedOnUrl", "commentCount", "url", "includedInDataCatalog", "sourceOrganization",
          "about", "disambiguatingDescription", "timeRequired", "encoding", "sponsor", "datePublished", "character", "spatialCoverage", "measurementTechnique", "citation", "discussionUrl", "aggregateRating", "releasedEvent", "sdLicense",
          "dateModified", "learningResourceType", "educationalAlignment", "description", "interactionStatistic", "translator", "audio", "accessibilityAPI", "sdPublisher", "material", "creativeWorkStatus", "recordedAt", "offers",
          "publishingPrinciples", "copyrightYear", "temporal", "inLanguage", "funding"
        ]
      }
    },
    methods: {
      prepData(results) {
        this.width = this.chicletSize * this.repos.length;
        this.height = this.chicletSize * results.length;

        // redefine scales
        this.x = d3.scaleBand()
        .domain(this.repos)
        .rangeRound([0, this.width])
        .paddingInner(0.05)
        .paddingOuter(0.05);

        this.y = d3.scaleBand()
        .domain(results.map(d => d.property))
        .rangeRound([0, this.height])
        .paddingInner(0.05)
        .paddingOuter(0.05);

        this.renderAxes();
      },
      renderAxes: function() {
      const xAxis = d3.axisBottom()
      .scale(this.x)
      .tickSizeOuter(0);

      const yAxis = d3.axisLeft()
      .scale(this.y)
        .tickSizeOuter(0);

      const xAxisBottom = d3.axisTop()
      .scale(this.x)
      .tickSizeOuter(0);

      const yAxisRight = d3.axisRight()
        .scale(this.y)
        .tickSizeOuter(0);

      const xTopRef = d3.select(this.$refs.xAxis);

      xTopRef
      .call(xAxis)
      .select('.domain').remove();

      xTopRef
      .selectAll("text")
      .attr("y", 0)
      .attr("x", 0)
      .attr("dx", "0.5em")
      .attr("dy", "0em")
      .attr("transform", "rotate(-60)");

      const xBottomRef = d3.select(this.$refs.xAxisBottom);

      xBottomRef.call(xAxisBottom)
      .select('.domain').remove();

      xBottomRef.selectAll("text")
      .attr("y", 0)
      .attr("x", 0)
      .attr("dx", "0.5em")
      .attr("dy", "0.5em")
      .attr("transform", "rotate(60)");

      d3.select(this.$refs.yAxis).call(yAxis)
        .select('.domain').remove();

      d3.select(this.$refs.yAxisRight).call(yAxisRight)
        .select('.domain').remove();
    },
      getSchemaDotorg() {
        axios.get('https://schema.org/Dataset.jsonld').then(function(response) {
          let properties = response.data["@graph"].filter(d => d['@type'] === "rdf:Property").map(d => d["@id"].replace("schema:", ""));
          console.log(properties)
        })
      },
      getPropertyCounts(property = null) {
        this.loading = true;

        let q_string = property ? `_exists_:${property}` : "__all__";

        var params = {
          "params": {
            "q": q_string,
            "size": 0,
            "facets": "_index",
            "facet_size": 15
          }
        }

        return (
          rxjs.from(axios.get("{{api_url}}" + 'query?', params)).pipe(
            rxjs.operators.pluck("data", "facets", "_index"),
            // rxjs.operators.tap(x => console.log(x)),
            rxjs.operators.map(result => {
              return ({
                "property": property,
                "total": result.total,
                "counts": cleanSources(result.terms)
              })
            })
          )
        );
      }
    },
    mounted() {
      // this.getSchemaDotorg();
      //
      tippy( '#heatmap-chart',{
              target:'rect',
              content: 'Loading...',
              maxWidth:'200px',
              placement:'auto',
              animation: 'fade',
              theme:'light',
              onShow(instance) {
                let info = instance.reference.dataset.tippyInfo;
                instance.setContent("<div class='text-muted m-0'>"+info+"</div>")
              }
            });

      tippy( '#nodata-heatmap',{
              target:'rect',
              content: 'Loading...',
              maxWidth:'200px',
              placement:'auto',
              animation: 'fade',
              theme:'light',
              onShow(instance) {
                let info = instance.reference.dataset.tippyInfo;
                instance.setContent("<div class='text-muted m-0'>"+info+"</div>")
              }
            });
    },
    observableMethods: {},
    subscriptions() {
      return {
        results: rxjs.forkJoin(
            [
              // call loop #1: loop over properties and assemble together an array of the frequency each property exists in each dataset.
              rxjs.forkJoin(...this.properties.map(this.getPropertyCounts)).pipe(
                rxjs.operators.tap(results => console.log(results)),
                rxjs.operators.map(results => {
                  this.schemaTotal = results.length;
                  return this.filterZeros ? results.filter(d => d.total) : results
                }),
                rxjs.operators.tap(_ => this.loading = false)),

              // call #2: get the totals for each dataset, to calc percentages.
              this.getPropertyCounts()
            ])
          .pipe(
            // join together the counts / variable / repository and the totals:
            // calculate percentages, fill colors based on percents.
            rxjs.operators.tap(results => console.log(results)),
            rxjs.operators.map(([properties, totals]) => {
              properties.forEach(property => {
                property.totalPct = property.total / totals.total;

                property.counts.forEach(repo => {
                  let repo_total = totals.counts.filter(total => total.key === repo.key);
                  if (repo_total.length === 1) {
                    repo.percent = repo.value / repo_total[0].value;
                    repo.fill = this.colorScheme(repo.percent);
                  }
                });

                // calculate average percentage of existence, taking into account the repos with no data.
                // Since using the average as well, ignoring it for the average count.
                property.avgPct = d3.sum(property.counts.map(d => d.percent))/(this.repos.length - 1);
                property.counts.push({key: "AVERAGE", value: property.total, percent: property.avgPct, fill: this.colorScheme(property.avgPct)})
              });

              properties.sort((a,b) => b.avgPct - a.avgPct);

              return (properties);
            }),
            // define the axes
            rxjs.operators.tap(results => this.prepData(results)),
            // calculate x/y position after axes created
            rxjs.operators.tap(results => {
              results.forEach(property => {

                property.counts.forEach(repo => {
                    repo.x = this.x(repo.key);
                    repo.y = this.y(property.property);
                });
            })
            return(results)
          }
          )
        )

    }
    }
  });
</script>

<style scoped>
.chiclet.no-data {
  opacity: 0.85;
}

rect {
  stroke: white;
  stroke-width: 0.5;
}

.chiclet {
  rx: 3px;
}

.slash-line {
  stroke: white;
  stroke: #212529;
  stroke-width: 0.75;
}

.axis--x text {
  text-anchor: start;
}

#color-legend rect {
  stroke-width: 0.5;
}

.legend-title {
  fill: #6c757d!important;
    font-size: 0.8em;
    font-weight: 300;
    dominant-baseline: hanging;
}

.legend-label {
  font-weight: 300;
  font-size: 0.8em;
  dominant-baseline: hanging;
}

.legend-label--min {
  text-anchor: start
}
.legend-label--max {
  text-anchor: end
}

#schema-explanation {
  flex: 1;
}
</style>
{% include "footer.html" %}
{% endblock %}
