// function to clean and return results from a facet call
// returns an object array: [{variable: funder, counts: [{key: NIH, value: 1231}]}]
cleanFacets = function(facets, facetSize = null) {
  let cleanedFacets = [];

  cleanedFacets.push({
    "variable": "funder",
    // "searchVariable": ["funder.name.keyword", "funding.funder.name.keyword"],
    "counts": combineFunders(facets, facetSize)
  })


  let facetVars = ["variableMeasured.keyword", "measurementTechnique.keyword", "keywords.keyword"];
  facetVars.forEach(varName => {
    let summary = {};
    summary['variable'] = varName.replace(".keyword", "");
    // summary['searchVariable'] = [varName];
    // basically a shim to convert term/count to key/value for consistency.
    summary['counts'] = d3.nest().key(d => d.term).rollup(values => d3.sum(values, d => d.count)).entries(facets[varName]['terms']).sort((a, b) => b.value - a.value);
    cleanedFacets.push(summary)
  })

  return (cleanedFacets)
}

cleanSources = function(sources) {
  sources.forEach(d => {
    d.term = d.term.replace("_search", "").replace("_transformed", "").replace(/_\d/, "").replace("_", " ");
  });

  let nested = d3.nest().key(d => d.term).rollup(values => d3.sum(values, d => d.count)).entries(sources);

  return (nested);
}

combineFunders = function(facets, facetSize) {
  let combined = facets['funder.name.keyword']['terms'].concat(facets['funding.funder.name.keyword']['terms']);
  let nested = d3.nest().key(d => d.term).rollup(values => d3.sum(values, d => d.count)).entries(combined).sort((a, b) => b.value - a.value);

  if (facetSize) {
    nested = nested.slice(0, facetSize);
  }

  return (nested);
}

getQueryFilters = function(selectedFilters) {
  console.log(selectedFilters)
  let query_string = Object.keys(selectedFilters)
  .filter(id => selectedFilters[id].length > 0)
  .map(id => reduceQuery(id, selectedFilters))
  .join(" AND ")

  console.log(query_string);

  return(query_string)
}

reduceQuery = function(id, selectedFilters) {
  let query_values = `("${selectedFilters[id].join('","')}")`;
  let query_string;
  if(id === "funder") {
    query_string = `(funder.name.keyword:${query_values} OR funding.funder.name.keyword:${query_values})`;
  } else {
    query_string = `${id}.keyword:${query_values}`;
  }
  return(query_string)
}
