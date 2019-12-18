<template>
<div class="d-flex align-items-center">
  <svg class='donut' :width='width + margin.left + margin.right' :height='height + margin.top + margin.bottom'>
    <g :transform='`translate(${this.margin.left + this.width / 2}, ${this.height / 2 + this.margin.top})`' id="donut-chart">
    </g>
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
  left: 35
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
      colorScale: null
    }
  },
  watch: {
    counts: function(newInput, oldInput) {
      console.log('newInput')
      this.prepData(newInput);
    },
    deep: true
  },
  methods: {
    prepData(data) {
      console.log("data in BarGraph")
      console.log(data)
      this.dataLength = data ? data.length : 0;
      if (this.dataLength) {
    }
  }
  },
  mounted() {
    console.log("hi bar graph!")
    console.log(this)
    console.log(this.counts)
    this.prepData(this.counts);
  }
}
</script>

<style scoped>
svg {
  background: tomato;
}
</style>
