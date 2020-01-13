<template>
<div class="d-flex align-items-center" id="donut-container">
  <svg class='donut' :width='width + margin.left + margin.right' :height='height + margin.top + margin.bottom'>
    <g :transform='`translate(${this.margin.left + this.width / 2}, ${this.height / 2 + this.margin.top})`' id="donut-chart">
      <path :data-tippy-info='`<b>${arc.data.key}</b>: ${arc.data.value.toLocaleString()} datasets`' v-for="arc in arcs" :d="arc.path" :fill="arc.fill" :id="arc.data.key" :key="arc.data.key"></path>
      <!-- <text v-for="arc in arcs" :x="arc.centroid[0]" :y="arc.centroid[1]" v-text="arc.data.key" class="donut-label"></text> -->
    </g>
  </svg>
  <ul class="donut-labels">
    <li v-for="arc in arcs" v-text="arc.data.key" v-bind:style="{ color: arc.fill}" :id="arc.data.key + '_label'" :key="arc.data.key + '_label'">
    </li>
  </ul>
</div>
</template>
 <script >
const hole_frac = 0.5;
const margin = {
  top: 5,
  right: 5,
  bottom: 5,
  left: 5
}

module.exports = {
  name: 'app-donut',
  props: ['source_counts', 'width'],
  data() {
    return {
      height:0,
      margin,
      hole_frac,
      dataLength: 0,
      arcs: [],
      colorScale: null
    }
  },
  watch: {
    source_counts: function(newInput, oldInput) {
      console.log('newInput')
      this.prepData(newInput);
    },
    deep: true
  },
  methods: {
    prepData(data) {
      this.height = this.width;

      this.dataLength = data ? data.length : 0;
      if (this.dataLength) {
        // angle calculation for pie chart
         this.arcs = d3.pie()
          .sort(null)
          .value(function(d) { return d.value; })
          (data);

        // path calculation to cut out the donut hole
        let arc = d3.arc()
          .innerRadius(this.height / 2 * this.hole_frac)
          .outerRadius(this.height / 2 - 1);

        // color scale
        let colorScale = d3.scaleOrdinal()
          .domain(['omicsdi', 'ncbi geo', 'zenodo', 'harvard dataverse'])
          // .domain(data.map(d => d.key))
          .range(d3.schemeTableau10);
          // .range(d3.quantize(t => d3.interpolateSpectral(t * 0.8 + 0.1), data.length).reverse());

        // calculate path, fill color.
        this.arcs.forEach(slice => {
          slice['path'] = arc(slice);
          slice['centroid'] = arc.centroid(slice);
          slice['fill'] = colorScale(slice.data.key);
        })
      }
    }
  },
  mounted() {
    this.prepData(this.source_counts);

    tippy( '#donut-container',{
        target:'path',
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
  }
}
</script>

<style scoped>
.donut path {
  stroke: black;
  stroke-width: 0.25;
}

.donut-label {
  text-anchor: middle;
}

.container {
  margin-top: 45px;
}

.donut-labels {
  list-style: none;
  padding-left: 10px;
  margin: 0;
  text-align: left;
}

.donut-labels li {
  font-weight: 700;
  line-height: 1.25em;
}
</style>
