(function () {
  "use strict";
  // Mobile navigation toggle.
  var toggle = document.querySelector(".nav-toggle");
  var menu = document.getElementById("primary-menu");
  if (toggle && menu) {
    toggle.addEventListener("click", function () {
      var open = menu.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }
  // Process-step click-to-pin: activating a step fixes its bubble open.
  // Hover and keyboard focus already reveal the bubble via CSS; this adds a
  // persistent pin so the specifics can be read without holding position.
  var steps = document.querySelectorAll(".pstep");
  Array.prototype.forEach.call(steps, function (step) {
    var trigger = step.querySelector(".pstep__trigger");
    if (!trigger) { return; }
    trigger.addEventListener("click", function (ev) {
      // On fine-pointer devices, a first activation pins; the link still works
      // on the second activation. On touch, the bubble is always visible.
      if (window.matchMedia && window.matchMedia("(hover: hover)").matches) {
        if (!step.classList.contains("is-pinned")) {
          ev.preventDefault();
          Array.prototype.forEach.call(steps, function (s) { s.classList.remove("is-pinned"); });
          step.classList.add("is-pinned");
        }
      }
    });
  });
  document.addEventListener("click", function (ev) {
    if (!ev.target.closest || !ev.target.closest(".pstep")) {
      Array.prototype.forEach.call(steps, function (s) { s.classList.remove("is-pinned"); });
    }
  });
  document.addEventListener("keydown", function (ev) {
    if (ev.key === "Escape") {
      Array.prototype.forEach.call(steps, function (s) { s.classList.remove("is-pinned"); });
    }
  });
})();
