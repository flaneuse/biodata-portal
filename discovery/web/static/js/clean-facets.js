// function to clean and return results from a facet call
cleanFacets = function(sources) {
  let filtered = sources.filter(d => d.term.includes("_search"));
  filtered.forEach(d => {
    d.term = d.term.replace("_search", "").replace("_transformed", "").replace(/_\d/, "").replace("_", " ");
  });

  let nested = d3.nest().key(d => d.term).rollup(values => d3.sum(values, d => d.count)).entries(filtered);

  return (nested);
}
