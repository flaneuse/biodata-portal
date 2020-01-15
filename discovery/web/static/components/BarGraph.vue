<template>
<div class="d-flex align-items-center" v-if="colorScale">
  <svg class='svg-bargraph' :width='width + margin.left + margin.right' :height='height + margin.top + margin.bottom'>
    <g :transform='`translate(${this.margin.left}, ${this.margin.top})`' id="bar-chart">
      <rect :data-tippy-info='`<b>${count.key}</b>: ${count.value.toLocaleString()}`' v-for="count in counts" :id="count.key" :key="count.key" class="bar" :x="x(0)" :y="y(count.key)" :width="x(count.value) - x(0)" :height="y.bandwidth()"></rect>
      <text :data-tippy-info='`<b>${count.key}</b>: ${count.value.toLocaleString()}`' v-for="count in counts" :key="count.key + '_label'" class="y-axis--label" :x="x(0) - 4" :y="y(count.key)+y.bandwidth()/2" v-text="count.label" v-bind:style="{ fontSize: count.fontSize  + 'px' }"></text>
      <!-- <rect v-for="count in counts" :id="count.key" class="bar" :x="x(0)" :y="y(count.key)" :fill="colorScale(count.value)" :width="x(count.value) - x(0)" :height="y.bandwidth()"></rect> -->
    </g>

    <!-- container for axes -->
    <!-- <g ref='xAxis' class="axis axis--x" :transform='`translate(${margin.left}, ${this.margin.top + 5})`' />
    <g ref='yAxis' class="axis axis--y" :transform='`translate(${margin.left}, ${this.margin.top})`' /> -->

  </svg>
</div>
</template>

 <script>
  const width = 100;
  const height = 125;
  const margin = {
  top: 5,
  right: 5,
  bottom: 5,
  left: 100
};

module.exports = {
  name: 'app-bar-graph',
  props: ['counts'],
  data() {
    return {
      width,
      height,
      margin,
      dataLength: 0,
      fontSizeMax: 14,
      data: [],
      x: d3.scaleLinear(),
      y: d3.scaleBand(),
      colorScale: null
    }
  },
  watch: {
    counts: function(newInput, oldInput) {
      this.prepData(newInput);
      this.renderAxes();
    },
    deep: true
  },
  methods: {
    prepData() {
      let lengthThreshold = 13;
      let data = this.counts;

      this.dataLength = data ? data.length : 0;

      if (this.dataLength) {
        this.x = d3.scaleLinear()
        .range([0, this.width])
        .domain([0, d3.max(data.map(d => d.value))]);

        this.y = d3.scaleBand()
        .domain(data.map(d => d.key))
        .rangeRound([0, this.height])
        .paddingInner(0.05)
        .paddingOuter(0.05);

        this.colorScale = d3.scaleSequential(d3.interpolateRdPu)
        .domain(d3.extent(data.map(d => d.value)));

        data.forEach(d => {
          d['fontSize'] = this.y.bandwidth()*0.95 > this.fontSizeMax ? this.fontSizeMax : this.y.bandwidth()*0.95;
          d['label'] = d.key.length > lengthThreshold ? d.key.slice(0, lengthThreshold) + "..." : d.key;
        })
    }
  },
  // renderAxes: function() {
  //   const xAxis = d3.axisBottom()
  //   .scale(this.x).ticks(10);
  //
  //   const yAxis = d3.axisLeft()
  //   .scale(this.y)
  //
  //   const xAx = d3.select(this.$refs.xAxis)
  //   xAx.remove();
  //
  //   d3.select(this.$refs.yAxis).call(yAxis);
  // }
  },
  mounted() {
    this.prepData();
    // this.renderAxes();
    //
    tippy('body',
    {
        target:'text',
        content: 'Loading...',
        maxWidth:'200px',
        placement:'right',
        animation: 'fade',
        theme:'light',
        onShow(instance) {
          let info = instance.reference.dataset.tippyInfo;
          instance.setContent("<div class='text-muted m-0'>"+info+"</div>")
        }
      });

    tippy('#niaid-diseases',
    {
        target:'rect',
        content: 'Loading...',
        maxWidth:'200px',
        placement:'right',
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
text.y-axis--label {
  fill: #78828a;
  dominant-baseline: middle;
  text-anchor: end;
}

rect {
  fill: #939ba2;
}

svg {
  /* background: tomato; */
}
</style>
