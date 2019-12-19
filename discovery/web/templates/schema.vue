{% extends "main.html" %}
{% block content %}
{% include "header.html" %}
<style scoped>
svg {
  /* background: tomato; */
}

.chiclet.no-data {
  opacity: 0.85;
}

rect {
  stroke: white;
  stroke-width: 0.5;
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

</style>
<div id="schema" class="container d-flex" style="min-height:100vh">
  <div v-if=loading class="loader">
    <img src="/static/img/ripple.svg" />
  </div>

  <div class="jumbotron bg-light text-muted w-100">
    <h1 class="row" v-if="results" v-text="'There are ' + schemaTotal + ' schema.org Dataset properties'"></h1>
    <h1 class="row" v-if="results" v-text="'... but only ' + results.filter(d => d.total).length + ' are used in our dataset repositories.'"></h1>

    <div class="d-flex align-items-center">
      <svg id="heatmap" class='heatmap' :width='width + margin.left + margin.right' :height='height + margin.top + margin.bottom'>
        <defs>
          <linearGradient id="gradient-legend" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop v-for="n in 10" :offset="(n/10)*100 + '%'" :style="`stop-color:${colorScheme(n/10)}; stop-opacity:1`" />
          </linearGradient>
        </defs>

        <!-- legend -->
        <g id="color-legend" transform='translate(0, -10)'>
          <rect width="15" height="15" :y="margin.top - 60" :style="`fill: ${colorScheme(0)}; stroke: ${colorScheme(1)}`"></rect>
          <line :x1="0" :x2="15" :y1="margin.top - 60 + 15" :y2="margin.top - 60" class="slash-line" />
          <text :x="20" :y="margin.top - 60" class="legend-title">not used</text>

          <text :x="0" :y="margin.top - 40" class="legend-title">prevalence in source</text>
          <rect :width="margin.left - 7" height="15" :y="margin.top - 25"fill="url(#gradient-legend)" :style="`stroke: ${colorScheme(1)}`"></rect>
          <text :x="margin.left - 7" :y="margin.top - 7" class="legend-label legend-label--max">100%</text>
          <text :x="0" :y="margin.top - 7" class="legend-label legend-label--min">0</text>
        </g>

        <!-- blank chiclets to represent no data -->
        <g :transform='`translate(${this.margin.left}, ${this.margin.top})`' id="nodata-heatmap">
          <g v-for="property in results" class="property-row">
              <rect v-for="repo in repos" :id="property.property + '-' + repo + '-nodata'" class="chiclet no-data" :x="x(repo)" :y="y(property.property)" :width="x.bandwidth()" :height="y.bandwidth()" :fill="colorScheme(0)"></rect>
              <line v-for="repo in repos" :x1="x(repo)" :x2="x(repo) + x.bandwidth()" :y1="y(property.property) + y.bandwidth()" :y2="y(property.property)" class="slash-line" />
          </g>
        </g>

        <!-- heatmap of actual data -->
        <g :transform='`translate(${this.margin.left}, ${this.margin.top})`' id="heatmap-chart">
          <g v-for="property in results" :id="property.property" class="property-row">
              <rect v-for="repo in property.counts" :id="property.property + '-' + repo.key" class="chiclet" :x="repo.x" :y="repo.y" :fill="repo.fill" :width="x.bandwidth()" :height="y.bandwidth()"></rect>
          </g>
        </g>

        <!-- container for axes -->
        <g ref='xAxis' class="axis axis--x" :transform='`translate(${margin.left}, ${this.margin.top + 5})`' />
        <g ref='yAxis' class="axis axis--y" :transform='`translate(${margin.left}, ${this.margin.top})`' />
        <g ref='xAxisBottom' class="axis axis--x axis--x-bottom" :transform='`translate(${margin.left}, ${this.margin.bottom + height - 5})`' />
        <g ref='yAxisRight' class="axis axis--y axis--y-right" :transform='`translate(${margin.left + width}, ${this.margin.top})`' />
      </svg>
    </div>

</div>
</div>
{% endblock %}

{% block extra_scripts %}
<script src="https://unpkg.com/vuex">
</script>
<script src = "https://cdnjs.cloudflare.com/ajax/libs/vue/2.4.2/vue.min.js">
</script>
<script src="https://unpkg.com/rxjs/bundles/rxjs.umd.js"></script>
<script src = "https://unpkg.com/vue/dist/vue.js" >
</script>
<script src="/static/js/vue-rx.js"></script><script src = "https://cdnjs.cloudflare.com/ajax/libs/axios/0.18.0/axios.min.js" ></script>
  <script src = "https://d3js.org/d3.v5.min.js" ></script>
  <script src = "/static/js/clean-facets.js" ></script>

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

        repos: ["harvard dataverse", "ncbi geo", "zenodo", "omicsdi", "AVERAGE"],
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
          rxjs.from(axios.get('http://su07:8080/api/query?', params)).pipe(
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
{% include "footer.html" %}
{% endblock %}
