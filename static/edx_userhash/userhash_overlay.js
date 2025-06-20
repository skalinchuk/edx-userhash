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
    const STEP = 180;                 // distance between repetitions (px)

    // Build a lattice that fully covers the block, including rotated margins
    for (let y = -rect.height; y < rect.height * 2; y += STEP) {
      for (let x = -rect.width; x < rect.width * 2; x += STEP) {
        const cell = document.createElement("span");
        cell.textContent = window.USER_HASH;
        cell.style.top = `${y}px`;
        cell.style.left = `${x}px`;
        overlay.appendChild(cell);
      }
    }

    block.style.position = block.style.position || "relative";
    block.appendChild(overlay);
  }

  /**
   * Inject overlays for all current and future CAPA blocks
   */
  function watermarkAllProblems() {
    document.querySelectorAll(".problem").forEach(createWatermark);
  }

  // Initial pass on page load
  watermarkAllProblems();

  // When CAPA re-renders (submissions, hints, etc.)
  document.addEventListener("new_content_loaded", watermarkAllProblems, true);
})();
