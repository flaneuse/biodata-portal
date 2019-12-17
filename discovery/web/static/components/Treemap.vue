

<template>
  <div>
<!-- <h1 v-text="leaves.length"></h1> -->

    <svg class='treemap' :width='width' :height='height'>
      <g v-for="d in leaves" :transform='`translate(${d.x0}, ${d.y0})`'>
         <rect :width="d.x1-d.x0" :height="d.y1 - d.y0" :fill="d.fill"></rect>
         <text v-text="d.data" text-anchor='middle' :dy="(d.y1 - d.y0)/2" :dx="(d.x1 - d.x0)/2" v-if="d.value > 900"></text>
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
  props: ['results'],
  data() {
    return {
      width,
      height,
      margin,
      numLeaves: 0,
      colorScale: null,
      leaves:[{"x0":1,"x1":231,"y0":1,"y1":221,"value":8807,"data":"E. coli","fill":"rgb(209, 60, 75)"},{"x0":1,"x1":231,"y0":222,"y1":349,"value":5107,"data":"Fungal Diseases","fill":"rgb(218, 72, 74)"},{"x0":232,"x1":394,"y0":1,"y1":180,"value":5066,"data":"Tuberculosis","fill":"rgb(226, 83, 74)"},{"x0":232,"x1":394,"y0":181,"y1":349,"value":4744,"data":"Group A Streptococcal Infections","fill":"rgb(233, 95, 73)"},{"x0":395,"x1":520,"y0":1,"y1":210,"value":4564,"data":"Sexually Transmitted Diseases","fill":"rgb(239, 107, 73)"},{"x0":521,"x1":608,"y0":1,"y1":210,"value":3173,"data":"Autoimmune Diseases","fill":"rgb(243, 120, 76)"},{"x0":395,"x1":512,"y0":211,"y1":349,"value":2840,"data":"HIV/AIDS","fill":"rgb(246, 134, 80)"},{"x0":513,"x1":608,"y0":211,"y1":349,"value":2287,"data":"Malaria ","fill":"rgb(249, 148, 86)"},{"x0":609,"x1":730,"y0":1,"y1":91,"value":1918,"data":"Influenza","fill":"rgb(251, 161, 93)"},{"x0":609,"x1":730,"y0":92,"y1":164,"value":1561,"data":"Hepatitis","fill":"rgb(252, 175, 101)"},{"x0":731,"x1":799,"y0":1,"y1":85,"value":1014,"data":"Asthma","fill":"rgb(253, 187, 110)"},{"x0":731,"x1":799,"y0":86,"y1":164,"value":938,"data":"Cholera","fill":"rgb(253, 199, 119)"},{"x0":609,"x1":667,"y0":165,"y1":249,"value":872,"data":"Primary Immune Deficiency Diseases (PIDDs)","fill":"rgb(254, 210, 129)"},{"x0":668,"x1":707,"y0":165,"y1":249,"value":581,"data":"Tickborne Diseases","fill":"rgb(254, 220, 139)"},{"x0":609,"x1":658,"y0":250,"y1":300,"value":444,"data":"Leishmaniasis","fill":"rgb(254, 229, 150)"},{"x0":659,"x1":707,"y0":250,"y1":300,"value":441,"data":"Shigellosis","fill":"rgb(254, 236, 160)"},{"x0":609,"x1":659,"y0":301,"y1":349,"value":431,"data":"Schistosomiasis (Bilharzia)","fill":"rgb(253, 242, 169)"},{"x0":660,"x1":707,"y0":301,"y1":349,"value":406,"data":"Plague","fill":"rgb(252, 247, 175)"},{"x0":708,"x1":755,"y0":165,"y1":207,"value":352,"data":"MERS & SARS","fill":"rgb(249, 249, 176)"},{"x0":756,"x1":799,"y0":165,"y1":207,"value":321,"data":"Dengue Fever","fill":"rgb(245, 250, 174)"},{"x0":708,"x1":738,"y0":208,"y1":256,"value":265,"data":"Gonorrhea","fill":"rgb(239, 248, 169)"},{"x0":739,"x1":769,"y0":208,"y1":256,"value":263,"data":"Ebola & Marburg","fill":"rgb(232, 246, 164)"},{"x0":770,"x1":799,"y0":208,"y1":256,"value":255,"data":"Eczema (Atopic Dermatitis)","fill":"rgb(223, 242, 160)"},{"x0":708,"x1":740,"y0":257,"y1":299,"value":245,"data":"Zika Virus","fill":"rgb(212, 238, 159)"},{"x0":741,"x1":770,"y0":257,"y1":299,"value":224,"data":"Respiratory Syncytial Virus (RSV)","fill":"rgb(200, 233, 159)"},{"x0":771,"x1":799,"y0":257,"y1":299,"value":212,"data":"Pertussis (Whooping Cough)","fill":"rgb(187, 228, 160)"},{"x0":708,"x1":727,"y0":300,"y1":349,"value":168,"data":"Prion Diseases","fill":"rgb(173, 222, 162)"},{"x0":728,"x1":761,"y0":300,"y1":325,"value":154,"data":"West Nile Virus","fill":"rgb(158, 216, 163)"},{"x0":728,"x1":761,"y0":326,"y1":349,"value":138,"data":"Lyme Disease","fill":"rgb(143, 210, 164)"},{"x0":762,"x1":784,"y0":300,"y1":326,"value":107,"data":"Leprosy (Hansen's Disease)","fill":"rgb(128, 203, 165)"},{"x0":785,"x1":799,"y0":300,"y1":326,"value":71,"data":"Autoimmune Lymphoproliferative Syndrome (ALPS)","fill":"rgb(114, 195, 167)"},{"x0":762,"x1":780,"y0":327,"y1":338,"value":39,"data":"Food Allergy","fill":"rgb(100, 185, 170)"},{"x0":762,"x1":780,"y0":339,"y1":349,"value":37,"data":"Syphilis","fill":"rgb(87, 174, 174)"},{"x0":781,"x1":799,"y0":327,"y1":336,"value":33,"data":"Rocky Mountain Spotted Fever","fill":"rgb(77, 162, 177)"},{"x0":781,"x1":793,"y0":337,"y1":349,"value":29,"data":"Smallpox","fill":"rgb(69, 149, 180)"},{"x0":794,"x1":799,"y0":337,"y1":349,"value":13,"data":"STAT3 Dominant-Negative Disease","fill":"rgb(66, 136, 181)"}]
    }
  },
  watch: {
    results: function(newInput, oldInput) {
      console.log(newInput)
      console.log('counts changed!')
      this.calculateScales();
      this.prepData();
      this.sayHi();
    },
    deep: true
  },
  methods: {
    // d3 scale functions
    calculateScales() {
      console.log('calling scales')
      // this.leaves = [{x0: 1, x1: 156, y0:1, y1: 146}, {x0: 157, x1: 246, y0:1, y1: 146}]
      // if (this.results && !this.results.length) {
      this.colorScale = d3.scaleOrdinal()
        .domain(this.results.map(d => d.disease))
        .range(d3.quantize(t => d3.interpolateSpectral(t * 0.8 + 0.1), this.results.length).reverse())
      // }

      let nested_root = [{
        key: "parent",
        parent: "",
        value: 0
      }];

console.log(this.results.length)
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
      console.log('calling prep data')

      let colorScale = d3.scaleOrdinal()
        .domain(this.results.map(d => d.disease))
        .range(d3.quantize(t => d3.interpolateSpectral(t * 0.8 + 0.1), this.results.length))

      this.numLeaves = 8;
      var self = this;
      if(self.results && self.results && self.results.length > 0){
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

        // console.log(this.hierarchy)

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
      })


      console.log(self.leaves)
      console.log(colorScale.domain())
      console.log(colorScale)
      console.log(d3.quantize(t => d3.interpolateSpectral(t * 0.8 + 0.1), this.results.length))
      console.log(self.leaves.length)
      console.log(this)
    }}
  },
  mounted() {
    console.log('Hello World')
    console.log(this)
    this.calculateScales();
    this.prepData();
  }
}


//
// export default {
//   name: 'app',
//   components: {
//     Histogram,
//     AreaChart,
//   },
//   data() {
//     // register any data we want to track changes of
//     return {
//     }
//   },
//   mounted() {
//     console.log("treemap")
//   },
//   methods: {}
// }
</script>

<style scoped>
.treemap {
  /* background: tomato; */
}
rect {
  /* fill: yellow; */
  stroke: white;
  stroke-width: 1;
}
</style>
