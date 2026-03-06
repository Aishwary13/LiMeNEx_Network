from dash.dependencies import Input, Output

def uniprot_and_lipid_redirect_callback():
    return [
    """
    function(data1, data2, data3) {

        function isInvalidLink(link) {
            return (
                link === null ||
                link === undefined ||
                link === "" ||
                link === "nan" ||
                link === "NaN"
            );
        }

        const ctx = dash_clientside.callback_context;

        if (!ctx.triggered.length) {
            return window.dash_clientside.no_update;
        }

        const propId = ctx.triggered[0].prop_id;

        // Extract component id JSON
        const idStr = propId.split(".")[0];
        let compId;

        try {
            compId = JSON.parse(idStr);
        } catch(e) {
            return window.dash_clientside.no_update;
        }

        let activeData = null;

        if (compId.index === "console-1") {
            activeData = data1;
        } else if (compId.index === "console-2") {
            activeData = data2;
        } else if (compId.index === "console-3") {
            activeData = data3;
        }

        if (!activeData) {
            return window.dash_clientside.no_update;
        }

        if ('uniprotAcc' in activeData) {

            if (isInvalidLink(activeData.uniprotAcc)) {

                const node = activeData.label || activeData.id || "Unknown";
                const type = activeData.type || "Unknown";

                window.open(
                    `/not-available?node=${encodeURIComponent(node)}&type=${encodeURIComponent(type)}`,
                    "_blank"
                );

                return window.dash_clientside.no_update;
            }

            window.open(
                `https://www.uniprot.org/uniprotkb/${activeData.uniprotAcc}`,
                "_blank"
            );

        } else if ('link' in activeData) {

            if (isInvalidLink(activeData.link)) {

                const node = activeData.label || activeData.id || "Unknown";
                const type = activeData.type || "Unknown";

                window.open(
                    `/not-available?node=${encodeURIComponent(node)}&type=${encodeURIComponent(type)}`,
                    "_blank"
                );

                return window.dash_clientside.no_update;
            }

            window.open(activeData.link, "_blank");
        }

        return window.dash_clientside.no_update;
    }
    """,
    Output("dummy-output-store", "data"),
    Input({'type': 'cy-graph','index':'console-1'}, "tapNodeData"),
    Input({'type': 'cy-graph','index':'console-2'}, "tapNodeData"),
    Input({'type': 'cy-graph','index':'console-3'}, "tapNodeData"),
]
    
    
def recenter_cytoscape_graph():
    
    return [
"""
function(n1, n2, n3) {

    const ctx =
        dash_clientside.callback_context ||
        window.dash_clientside.callback_context;

    if (!ctx || !ctx.triggered.length) {
        return window.dash_clientside.no_update;
    }

    // ✅ Which button triggered?
    const trigger = ctx.triggered[0].prop_id.split('.')[0];

    let consoleIndex = null;

    if (trigger === "reset-btn-1") consoleIndex = "1";
    if (trigger === "reset-btn-2") consoleIndex = "2";
    if (trigger === "reset-btn-3") consoleIndex = "3";

    if (!consoleIndex) {
        return window.dash_clientside.no_update;
    }

    console.log("Resetting console:", consoleIndex);

    // ✅ Find matching cytoscape
    const cytoElement =
        document.querySelector(
            `[id*="console-${consoleIndex}"][id*="cy-graph"]`
        );

    if (!cytoElement || !cytoElement._cyreg) {
        console.error("❌ Cytoscape not ready");
        return window.dash_clientside.no_update;
    }

    const cy = cytoElement._cyreg.cy;

    const checkReady = setInterval(function () {

        if (cy.nodes().length > 0) {

            cy.animate({
                fit: {
                    eles: cy.elements(),
                    padding: 50
                },
                duration: 250
            });

            clearInterval(checkReady);
        }

    }, 100);

    setTimeout(() => clearInterval(checkReady), 3000);

    return window.dash_clientside.no_update;
}
""",
Output('reset-dummy-store', 'data'),
Input('reset-btn-1', 'n_clicks'),
Input('reset-btn-2', 'n_clicks'),
Input('reset-btn-3', 'n_clicks'),

]