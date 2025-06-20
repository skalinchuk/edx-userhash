(function () {
  if (!window.USER_HASH) return;

  /**
   * Create a grid of rotated hash strings that fills `block`.
   */
  function createWatermark(block) {
    // Avoid duplicates if the DOM refreshes
    if (block.querySelector(".userhash-overlay")) return;

    // Prepare overlay container
    const overlay = document.createElement("div");
    overlay.className = "userhash-overlay";

    const rect = block.getBoundingClientRect();
    // distance between repetitions
    const STEP_X = 360; // px
    const STEP_Y = 120; // px
    const SUBSTEP_X = 120; // px
    let counter = 0;

    // Build a lattice that fully covers the block, including rotated margins
    for (let y = -rect.height; y < rect.height * 2; y += STEP_Y) {
      counter = counter === 2 ? 0 : counter + 1
      for (let x = -rect.width; x < rect.width * 2; x += STEP_X) {
        const cell = document.createElement("span");
        cell.textContent = window.USER_HASH;
        cell.style.top = `${y}px`;
        cell.style.left = `${x + counter * SUBSTEP_X}px`;
        overlay.appendChild(cell);
      }
    }

    block.style.position = block.style.position || "relative";
    block.appendChild(overlay);
  }

  /**
   * Inject overlays for all existing and future X blocks
   */
  function watermarkAllProblems() {
    document.querySelectorAll("#main > .xblock").forEach(createWatermark);
  }

  /**
   * Create observer to monitor document changes and re-initialize overlay
   */
  function observePageForProblems(callback) {
    const observer = new MutationObserver(() => {
      callback();
    });

    observer.observe(document.body, {
      childList: true,
      subtree: true,
    });
  }

  document.addEventListener('DOMContentLoaded', () => {
    // Initial pass on page load
    watermarkAllProblems();
    observePageForProblems(() => {
      watermarkAllProblems();
    });
  });
})();
