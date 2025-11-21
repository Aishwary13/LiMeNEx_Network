// // assets/cytoscape-pop-close.js
// (function() {
//   const POP_CONTAINER_ID = 'cytoscape-tap-edge-data-output';

//   function attachClickHandler() {
//     const container = document.getElementById(POP_CONTAINER_ID);
//     if (!container) return;

//     // delegate clicks for any close button that appears inside the container
//     container.addEventListener('click', function(event) {
//       const target = event.target;
//       if (!target) return;
//       // match either the button id or the class
//       if (target.classList && target.classList.contains('pop-close-btn')) {
//         // Hide & clear the popup immediately
//         container.style.display = 'none';
//         container.innerHTML = '';
//       }
//     }, false);
//   }

//   // Try attach once DOM is ready; also use interval to catch late-mounted containers
//   if (document.readyState === 'complete' || document.readyState === 'interactive') {
//     attachClickHandler();
//   } else {
//     document.addEventListener('DOMContentLoaded', attachClickHandler);
//   }

//   // safety: try again until we find the container (matches dynamic mounting)
//   const tryInterval = setInterval(function() {
//     if (document.getElementById(POP_CONTAINER_ID)) {
//       attachClickHandler();
//       clearInterval(tryInterval);
//     }
//   }, 300);
// })();
