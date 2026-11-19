/* Fills business details from config.js into the legal pages. */
(function () {
  "use strict";
  var cfg = window.FOXCREST || {};
  document.querySelectorAll("[data-cfg]").forEach(function (el) {
    var v = cfg[el.dataset.cfg];
    if (v) el.textContent = v;
  });
  document.querySelectorAll("[data-cfg-email]").forEach(function (el) {
    if (!cfg.email) return;
    var subj = el.getAttribute("data-subject");
    el.href = "mailto:" + cfg.email + (subj ? "?subject=" + encodeURIComponent(subj) : "");
    if (!el.hasAttribute("data-keep-text")) el.textContent = cfg.email;
  });
  var y = document.getElementById("year");
  if (y) y.textContent = new Date().getFullYear();
})();
