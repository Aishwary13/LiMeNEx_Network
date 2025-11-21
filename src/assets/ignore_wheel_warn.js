(function(){
  // Silences the Cytoscape wheel-sensitivity warning printed by dash-cytoscape
  // Only ignores the specific, known warning message so other warnings still appear.
  try {
    const origWarn = console.warn.bind(console);
    console.warn = function(...args) {
      try {
        if (args.length > 0 && typeof args[0] === 'string' && args[0].includes('You have set a custom wheel sensitivity')) {
          // drop this specific warning
          return;
        }
      } catch (e) {
        // ignore errors in the filter and forward original warn
      }
      origWarn(...args);
    };
  } catch (e) {
    // If anything goes wrong, fail silently so we don't break the app.
  }
})();
