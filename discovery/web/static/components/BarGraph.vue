<template v-if="dataLength">
<div class="d-flex align-items-center">
  <svg class='svg-bargraph' :width='width + margin.left + margin.right' :height='height + margin.top + margin.bottom'>
    <g :transform='`translate(${this.margin.left}, ${this.margin.top})`' id="bar-chart">
      <rect v-for="count in counts" :id="count.term" class="bar" :x="x(0)" :y="y(count.term)" :fill="colorScale(count.count)" :width="x(count.count) - x(0)" :height="y.bandwidth()"></rect>
    </g>

    <!-- container for axes -->
    <g ref='xAxis2' class="axis axis--x" :transform='`translate(${margin.left}, ${this.margin.top + 5})`' />
    <g ref='yAxis2' class="axis axis--y" :transform='`translate(${margin.left}, ${this.margin.top})`' />
  </svg>
</div>
</template>

 <script>
  const width = 150;
  const height = 125;
  const margin = {
  top: 5,
  right: 5,
  bottom: 5,
  left: 50
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
      data: [],
      x: d3.scaleLinear(),
      y: d3.scaleBand(),
      colorScale: null
    }
  },
  watch: {
    counts: function(newInput, oldInput) {
      console.log('newInput')
      this.prepData(newInput);
      this.renderAxes();
    },
    deep: true
  },
  methods: {
    prepData(data) {
      console.log("data in BarGraph")
      console.log(data)
      this.dataLength = data ? data.length : 0;
      if (this.dataLength) {
        console.log('hi data!')
        this.x = d3.scaleLinear()
        .range([0, this.width])
        .domain(d3.extent(data.map(d => d.count)));

        this.y = d3.scaleBand()
        .domain(data.map(d => d.term))
        .rangeRound([0, this.height])
        .paddingInner(0.05)
        .paddingOuter(0.05);

        this.colorScale = d3.scaleSequential(d3.interpolateRdPu)
        .domain(d3.extent(data.map(d => d.count)));

        this.renderAxes()

        console.log(this.colorScale)
    }
  },
  renderAxes() {
    console.log('rendering axes')

    const xAxis = d3.axisBottom()
    .scale(this.x)

    const yAxis = d3.axisLeft()
    .scale(this.y)
      .tickSizeOuter(0);

console.log(yAxis)
      const xTopRef = d3.select(this.$refs.xAxis2);

      xTopRef
      .call(xAxis)
      .select('.domain').remove();

      d3.select(".axis--y").call(yAxis)

  }
  },
  mounted() {
    console.log("hi bar graph!")
    console.log(this)
    console.log(this.counts)
    this.prepData(this.counts);
    this.renderAxes();
  }
}
</script>

<style scoped>
svg {
  /* background: tomato; */
}
</style>
