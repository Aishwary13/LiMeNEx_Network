var dagfuncs = window.dashAgGridFunctions = window.dashAgGridFunctions || {};

dagfuncs.pubmedLinkRenderer = function(params) {
    if (!params.value) return null;

    let pmids = params.value.toString().split(/[;, ]+/).filter(x => x);

    return React.createElement(
        'div',
        { style: { display: "flex", flexWrap: "wrap", gap: "6px" } },
        pmids.map(function(pmid, i){
            return React.createElement(
                'a',
                {
                    key: i,
                    href: "https://pubmed.ncbi.nlm.nih.gov/" + pmid,
                    target: "_blank",
                    style: { color:"#4fa3ff", textDecoration:"none" }
                },
                pmid
            );
        })
    );
};

dagfuncs.headerLinkRenderer = function(params) {
    const links = {
        "Chea": "https://maayanlab.cloud/chea3/",
        "Signor": "https://signor.uniroma2.it/",
        "Trrust": "https://www.grnpedia.org/trrust/",
        "Experiment": "https://signalingpathways.org/index.jsf"
    };

    const url = links[params.column.colId] || "#";

    // Return HTML string (safe for Dash AG Grid header bridge)
    return `<a href="${url}" target="_blank"
              style="color:#4fa3ff;text-decoration:none;font-weight:600;">
                ${params.displayName}
            </a>`;
};