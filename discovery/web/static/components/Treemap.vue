<template>
<div id="treemap-container">
  <svg class='treemap' :width='width' :height='height'>
    <g v-for="d in leaves" :transform='`translate(${d.x0}, ${d.y0})`'>
      <a :href="`/${route}#${d.anchor}`">
        <rect :data-tippy-info="`${d.data.id}: ${d.value} results`" :width="d.x1-d.x0" :height="d.y1 - d.y0" :fill="d.fill"></rect>
        <text :data-tippy-info="`${d.data.id}: ${d.value} results`" text-anchor='middle' :dy="(d.y1 - d.y0)/2" :dx="(d.x1 - d.x0)/2" v-if="d.value > 900" class="treemap-text" v-text="d.data.id">
      </text>
      </a>
    </g>
  </svg>
</div>
</template>

<script>
const width = 800;
const height = 350;
const margin = {
  top: 5,
  right: 5,
  bottom: 5,
  left: 5
}

module.exports = {
  name: 'app-treemap',
  props: ['results', 'route'],
  data() {
    return {
      width,
      height,
      margin,
      numLeaves: 0,
      colorScale: null,
      leaves: []
    }
  },
  watch: {
    results: function(newInput, oldInput) {
      this.calculateScales();
      this.prepData();
    },
    deep: true
  },
  methods: {
    // d3 scale functions
    calculateScales() {
      this.colorScale = d3.scaleOrdinal()
        .domain(this.results.map(d => d.disease))
        .range(d3.quantize(t => d3.interpolateSpectral(t * 0.8 + 0.1), this.results.length).reverse());

      this.leaves.forEach(d => d['words'] = d.data.split(/\s+/));

      let nested_root = [{
        key: "parent",
        parent: "",
        value: 0
      }];

      this.results.forEach(d => {
        nested_root.push({
          key: d.disease,
          value: d.total,
          parent: "parent"
        })
      })

      // Stratifying data into a one-layer hierarchy for treemap.
      let hierarchy = d3.stratify()
        .id(d => d.key)
        .parentId(d => d.parent)(nested_root)
        .sum(d => d.value);

      this.numLeaves = nested_root.length;
    },

    // create tree objects
    prepData() {
      let colorScale = d3.scaleOrdinal()
        .domain(this.results.map(d => d.disease))
        .range(d3.quantize(t => d3.interpolateSpectral(t * 0.8 + 0.1), this.results.length))

      this.numLeaves = 8;
      var self = this;
      if (self.results && self.results && self.results.length > 0) {
        // Need to have a root object for the hierarchy to relate to
        // Creating a dummy "parent root"
        let nested_root = [{
          key: "parent",
          parent: "",
          value: 0
        }];

        self.results.forEach(d => {
          nested_root.push({
            key: d.disease,
            value: d.total,
            parent: "parent"
          })
        })

        // Stratifying data into a one-layer hierarchy for treemap.
        self.hierarchy = d3.stratify()
          .id(d => d.key)
          .parentId(d => d.parent)(nested_root)
          .sum(d => d.value);

        self.treemap = data => d3.treemap()
          .tile(d3.treemapBinary)
          .size([self.width, self.height])
          .padding(1)
          .round(true)
          (d3.hierarchy(data)
            .sort((a, b) => b.value - a.value));

        self.root = self.treemap(self.hierarchy);
        self.leaves = self.root.leaves();

        self.leaves.forEach(d => {
          d.fill = colorScale(d.data.id);
          d.anchor = d.data.id.replace(/\s+/g, "-");
        })

      }
    }
  },
  mounted() {
    this.calculateScales();
    this.prepData();


    tippy( '#treemap-container',{
        target:'.treemap rect',
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

    tippy( '.treemap',{
        target:'text',
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
.treemap-text {
  fill: white;
  font-size: 20px;
  dominant-baseline: middle;
}

rect {
  stroke: white;
  stroke-width: 1;
}
</style>
