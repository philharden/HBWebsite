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
  // SDLC wheel: hovering or focusing a phase updates the detail line beneath
  // it. Clicking a phase navigates to its service page (native link behavior).
  var detail = document.getElementById("wheel-detail");
  var segs = document.querySelectorAll(".wseg");
  function setActive(seg) {
    Array.prototype.forEach.call(segs, function (s) { s.classList.remove("is-active"); });
    if (!seg) { return; }
    seg.classList.add("is-active");
    if (detail) {
      var name = seg.getAttribute("data-num") + " · " + seg.getAttribute("data-label");
      var tip = seg.getAttribute("data-tip") || "";
      detail.innerHTML = "";
      var ns = document.createElement("span");
      ns.className = "wheel__detail-name";
      ns.textContent = name;
      var ts = document.createElement("span");
      ts.className = "wheel__detail-text";
      ts.textContent = " — " + tip;
      detail.appendChild(ns);
      detail.appendChild(ts);
    }
  }
  Array.prototype.forEach.call(segs, function (seg) {
    seg.addEventListener("mouseenter", function () { setActive(seg); });
    seg.addEventListener("focus", function () { setActive(seg); });
  });
})();
