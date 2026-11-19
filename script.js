(function () {
  "use strict";
  var cfg = window.FOXCREST || {};
  var prices = cfg.prices || { walkthrough: 300, campaignFirstMonth: 800, campaignMonthly: 1000 };
  var money = function (n) { return "$" + n.toLocaleString("en-US"); };

  // ---------- Year + shared settings ----------
  document.getElementById("year").textContent = new Date().getFullYear();
  document.querySelectorAll("[data-cfg]").forEach(function (el) {
    var v = cfg[el.dataset.cfg];
    if (v) el.textContent = v;
  });

  // ---------- Contact details ----------
  if (cfg.email) {
    var e = document.getElementById("contact-email");
    e.href = "mailto:" + cfg.email;
    e.querySelector("span").textContent = cfg.email;
  }
  if (cfg.phone) {
    var p = document.getElementById("contact-phone");
    p.href = "tel:" + cfg.phone.replace(/[^\d+]/g, "");
    p.querySelector("span").textContent = cfg.phone;
  }

  // ---------- Mobile nav ----------
  var toggle = document.querySelector(".nav-toggle");
  var links = document.getElementById("nav-links");
  toggle.addEventListener("click", function () {
    var open = links.classList.toggle("is-open");
    toggle.setAttribute("aria-expanded", String(open));
  });
  links.addEventListener("click", function (ev) {
    if (ev.target.tagName === "A") {
      links.classList.remove("is-open");
      toggle.setAttribute("aria-expanded", "false");
    }
  });

  // ---------- Portfolio ----------
  function youTubeId(url) {
    var m = url.match(/(?:youtu\.be\/|v=|embed\/|shorts\/)([\w-]{11})/);
    return m ? m[1] : null;
  }
  function vimeoId(url) {
    var m = url.match(/vimeo\.com\/(?:video\/)?(\d+)/);
    return m ? m[1] : null;
  }
  function embedFor(url) {
    var yt = youTubeId(url);
    if (yt) return '<iframe src="https://www.youtube-nocookie.com/embed/' + yt + '?autoplay=1&rel=0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen title="Property walkthrough"></iframe>';
    var vm = vimeoId(url);
    if (vm) return '<iframe src="https://player.vimeo.com/video/' + vm + '?autoplay=1" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen title="Property walkthrough"></iframe>';
    return '<video src="' + url + '" controls autoplay playsinline></video>';
  }
  function esc(s) {
    return String(s || "").replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  var grid = document.getElementById("portfolio");
  var hues = [18, 32, 150, 200, 12, 40];
  (cfg.portfolio || []).forEach(function (item, i) {
    var thumb = item.thumbnail;
    if (!thumb && item.video && youTubeId(item.video)) {
      thumb = "https://img.youtube.com/vi/" + youTubeId(item.video) + "/hqdefault.jpg";
    }
    var card = document.createElement(item.video ? "button" : "div");
    card.className = "work" + (item.video ? "" : " is-soon");
    card.dataset.type = item.type || "house";
    if (item.video) {
      card.type = "button";
      card.setAttribute("aria-label", "Play walkthrough: " + item.title);
      card.addEventListener("click", function () { openVideo(item.video); });
    }
    var bg = thumb
      ? 'style="background-image:url(\'' + esc(thumb) + '\')"'
      : 'style="--h:' + hues[i % hues.length] + '"';
    card.innerHTML =
      '<div class="work-thumb' + (thumb ? " has-img" : "") + '" ' + bg + ">" +
        '<svg class="house-art" viewBox="0 0 120 80" aria-hidden="true"><path d="M20 70V38L60 12l40 26v32z"/><rect x="50" y="46" width="20" height="24"/><rect x="30" y="44" width="12" height="10"/><rect x="78" y="44" width="12" height="10"/></svg>' +
        (item.video
          ? '<span class="play"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></span>'
          : '<span class="soon">Video coming soon</span>') +
      "</div>" +
      '<div class="work-body">' +
        "<h3>" + esc(item.title) + "</h3>" +
        "<p>" + esc(item.details) + "</p>" +
        (item.location ? '<p class="loc">' + esc(item.location) + "</p>" : "") +
      "</div>";
    grid.appendChild(card);
  });

  document.querySelectorAll(".filter").forEach(function (btn) {
    btn.addEventListener("click", function () {
      document.querySelectorAll(".filter").forEach(function (b) {
        b.classList.remove("is-active");
        b.setAttribute("aria-pressed", "false");
      });
      btn.classList.add("is-active");
      btn.setAttribute("aria-pressed", "true");
      var f = btn.dataset.filter;
      grid.querySelectorAll(".work").forEach(function (c) {
        c.hidden = f !== "all" && c.dataset.type !== f;
      });
    });
  });

  // ---------- Video modal ----------
  var modal = document.getElementById("video-modal");
  var modalBody = modal.querySelector(".modal-body");
  function openVideo(url) {
    modalBody.innerHTML = embedFor(url);
    if (modal.showModal) modal.showModal(); else window.open(url, "_blank");
  }
  function closeVideo() { modal.close(); }
  modal.querySelector(".modal-close").addEventListener("click", closeVideo);
  modal.addEventListener("click", function (ev) { if (ev.target === modal) closeVideo(); });
  modal.addEventListener("close", function () { modalBody.innerHTML = ""; });

  // ---------- Live estimate ----------
  var wInput = document.getElementById("walkthroughs");
  var cInput = document.getElementById("campaign");
  var totalEl = document.getElementById("estimate-total");
  var breakEl = document.getElementById("estimate-break");

  function estimate() {
    var w = Math.max(0, Math.min(50, parseInt(wInput.value, 10) || 0));
    var m = parseInt(cInput.value, 10) || 0;
    var walk = w * prices.walkthrough;
    var camp = m > 0 ? prices.campaignFirstMonth + (m - 1) * prices.campaignMonthly : 0;
    var lines = [];
    if (w) lines.push(w + " walkthrough" + (w > 1 ? "s" : "") + " × " + money(prices.walkthrough));
    if (m) lines.push(m + "-month campaign (" + money(prices.campaignFirstMonth) + " first month" +
      (m > 1 ? " + " + (m - 1) + " × " + money(prices.campaignMonthly) : "") + ")");
    totalEl.textContent = money(walk + camp);
    breakEl.textContent = lines.length ? lines.join(" + ") : "Choose a service to see an estimate";
    return { total: walk + camp, summary: lines.join(" + ") || "None selected" };
  }
  wInput.addEventListener("input", estimate);
  cInput.addEventListener("change", estimate);
  estimate();

  // Plan buttons preselect the form
  document.querySelectorAll("[data-plan]").forEach(function (a) {
    a.addEventListener("click", function () {
      if (a.dataset.plan === "campaign") {
        if (cInput.value === "0") cInput.value = "1";
        if (wInput.value === "0") wInput.value = "1";
      } else {
        cInput.value = "0";
        if (wInput.value === "0") wInput.value = "1";
      }
      estimate();
    });
  });

  // ---------- Form submit ----------
  var form = document.getElementById("quote-form");
  var status = document.getElementById("form-status");

  form.addEventListener("submit", function (ev) {
    ev.preventDefault();
    status.className = "form-status";
    var name = form.elements.name.value.trim();
    var email = form.elements.email.value.trim();
    if (!name || !/^\S+@\S+\.\S+$/.test(email)) {
      status.textContent = "Please add your name and a valid email address.";
      status.classList.add("is-error");
      (!name ? form.elements.name : form.elements.email).focus();
      return;
    }
    if (!form.elements.consent.checked) {
      status.textContent = "Please tick the box to agree to our Terms and Privacy Policy.";
      status.classList.add("is-error");
      form.elements.consent.focus();
      return;
    }
    var est = estimate();
    var data = {
      name: name,
      email: email,
      phone: form.elements.phone.value.trim(),
      role: form.elements.role.value,
      address: form.elements.address.value.trim(),
      walkthroughs: wInput.value,
      campaign_months: cInput.value,
      estimate: money(est.total) + " (" + est.summary + ")",
      message: form.elements.message.value.trim(),
      agreed_to_terms: "yes (" + new Date().toISOString() + ")",
    };

    if (cfg.formEndpoint) {
      var btn = form.querySelector("button[type=submit]");
      btn.disabled = true;
      btn.textContent = "Sending…";
      fetch(cfg.formEndpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify(data),
      })
        .then(function (r) {
          if (!r.ok) throw new Error("bad status");
          form.reset();
          estimate();
          status.textContent = "Thanks, " + name + "! Your request is in. We'll be in touch shortly.";
          status.classList.add("is-ok");
        })
        .catch(function () {
          status.textContent = "Something went wrong. Please email us directly at " + (cfg.email || "") + ".";
          status.classList.add("is-error");
        })
        .finally(function () {
          btn.disabled = false;
          btn.textContent = "Send my quote request";
        });
    } else {
      var body = [
        "Name: " + data.name,
        "Email: " + data.email,
        "Phone: " + (data.phone || "-"),
        "I am a: " + data.role,
        "Property: " + (data.address || "-"),
        "Walkthroughs: " + data.walkthroughs,
        "Campaign months: " + data.campaign_months,
        "Estimate: " + data.estimate,
        "Agreed to Terms & Privacy: " + data.agreed_to_terms,
        "",
        data.message,
      ].join("\n");
      window.location.href = "mailto:" + (cfg.email || "") +
        "?subject=" + encodeURIComponent("Quote request from " + name) +
        "&body=" + encodeURIComponent(body);
      status.textContent = "Your email app should open with your request ready to send.";
      status.classList.add("is-ok");
    }
  });
})();
