encodeES = function(str) {
  // ES reserved chars from https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#_reserved_characters
  //
  /*
  Test searches:
   Madagascar (2014): Household Survey on Complementary Feeding Practices, Use of Micronutrient Powder and Anemia Levels of Infants Between 6 and 23 Months of Age. Round 2.
   RNA Sequencing of Wild Type and CCR2-/- mouse esophageal tumor transcriptomes
   CCR2+ vs. CCR2- murine hematopoietic stem cells
   TGFb1/SMAD3
   Mycobacterium tuberculosis PtpA ChIP-chip on U937 cells using Monoclonal ANTI-FLAG(R) M2 antibody
   [transfected with 10ng of empty vector (pcDNA3.1+)]
  */


  // let transformed = str;
  let transformed = str.replace(/([\-\=\!\*\+\&\|\(\)\[\]\{\}\^\~\?\:\/])/g, "\\$1");

  // reserved_chars.forEach(char => {
  //   console.log(transformed.replace(new RegExp(`\${char}`, "g"), `\${char}`));
  // })
  //


  return (transformed)
}
