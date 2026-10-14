/* Catalyst Capital Management | Residential Lending site scripts */
(function () {
  "use strict";

  /* Published program limits (from catalystccm.com program summaries and term sheets).
     Edit here to update the estimator and the application checks site-wide. */
  var PROGRAMS = {
    construction: {
      name: "Ground-Up Construction", min: 1000000, max: 10000000, ltc: 0.80, ltv: 0.70,
      costA: "Land or lot cost", costB: "Construction budget (hard and soft)", value: "As-completed value",
      rate: "SOFR + 5.00%", term: "Up to 36 months"
    },
    flip: {
      name: "Fix & Flip", min: 350000, max: 5000000, ltc: 0.95, ltv: 0.75,
      costA: "Purchase price", costB: "Rehab budget", value: "After-repair value (ARV)",
      rate: "Fixed, from 10%", term: "Up to 24 months"
    },
    bridge: {
      name: "Bridge", min: 500000, max: 10000000, ltc: 0.85, ltv: 0.75,
      costA: "Purchase price or payoff", costB: "Renovation budget (if any)", value: "Appraised value",
      rate: "From 9%", term: "Up to 36 months"
    }
  };

  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var num = function (v) { var n = parseFloat(String(v || "").replace(/[^0-9.]/g, "")); return isNaN(n) ? 0 : n; };
  var usd = function (n) { return "$" + Math.round(n).toLocaleString("en-US"); };
  var pct = function (n) { return isFinite(n) && n > 0 ? (n * 100).toFixed(1) + "%" : "–"; };

  /* Money inputs: format with thousands separators as the user types */
  function bindMoney(el) {
    el.addEventListener("input", function () {
      var pos = el.selectionStart, before = el.value.length;
      var raw = el.value.replace(/[^0-9]/g, "");
      el.value = raw ? Number(raw).toLocaleString("en-US") : "";
      var diff = el.value.length - before;
      try { el.setSelectionRange(pos + diff, pos + diff); } catch (e) {}
    });
  }
  $$("input[data-money]").forEach(bindMoney);

  /* Header: mobile toggle and dropdown */
  var toggle = $(".nav-toggle");
  if (toggle) toggle.addEventListener("click", function () {
    var open = document.body.classList.toggle("nav-open");
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
  });
  $$(".dd").forEach(function (dd) {
    var btn = $("button", dd);
    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      var open = dd.classList.toggle("open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
    if (window.matchMedia("(hover: hover) and (min-width: 961px)").matches) {
      dd.addEventListener("mouseenter", function () { dd.classList.add("open"); btn.setAttribute("aria-expanded", "true"); });
      dd.addEventListener("mouseleave", function () { dd.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); });
    }
  });
  document.addEventListener("click", function () { $$(".dd.open").forEach(function (d) { d.classList.remove("open"); }); });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") { $$(".dd.open").forEach(function (d) { d.classList.remove("open"); }); document.body.classList.remove("nav-open"); }
  });

  /* Tabs */
  $$("[data-tabs]").forEach(function (root) {
    var tabs = $$("[role=tab]", root);
    tabs.forEach(function (t, i) {
      t.addEventListener("click", function () { select(i); });
      t.addEventListener("keydown", function (e) {
        if (e.key === "ArrowRight" || e.key === "ArrowLeft") {
          var n = (i + (e.key === "ArrowRight" ? 1 : tabs.length - 1)) % tabs.length;
          select(n); tabs[n].focus();
        }
      });
    });
    function select(i) {
      tabs.forEach(function (t, j) {
        t.setAttribute("aria-selected", i === j ? "true" : "false");
        t.tabIndex = i === j ? 0 : -1;
        $("#" + t.getAttribute("aria-controls")).hidden = i !== j;
      });
    }
  });

  /* Scroll reveal */
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -8% 0px" });
    $$(".reveal").forEach(function (el) { io.observe(el); });
  } else { $$(".reveal").forEach(function (el) { el.classList.add("in"); }); }

  /* Loan estimator */
  $$("[data-estimator]").forEach(function (root) {
    var key = root.getAttribute("data-program") || "construction";
    var segBtns = $$(".seg button", root);
    var a = $("[name=est_a]", root), b = $("[name=est_b]", root), v = $("[name=est_v]", root);

    function setProgram(k) {
      key = k;
      segBtns.forEach(function (sb) { sb.setAttribute("aria-pressed", sb.getAttribute("data-k") === k ? "true" : "false"); });
      var p = PROGRAMS[k];
      $("[data-lbl=a]", root).textContent = p.costA;
      $("[data-lbl=b]", root).textContent = p.costB;
      $("[data-lbl=v]", root).textContent = p.value;
      $("[data-out=caps]", root).textContent = "Up to " + Math.round(p.ltc * 100) + "% of cost and " + Math.round(p.ltv * 100) + "% of value";
      calc();
    }
    segBtns.forEach(function (sb) { sb.addEventListener("click", function () { setProgram(sb.getAttribute("data-k")); }); });

    function calc() {
      var p = PROGRAMS[key];
      var cost = num(a.value) + num(b.value), val = num(v.value);
      var out = function (n) { return $("[data-out=" + n + "]", root); };
      var warn = out("warn"); warn.hidden = true;
      if (!cost || !val) {
        out("loan").textContent = "$0";
        ["cost", "equity", "ltc", "ltv", "bind"].forEach(function (n) { out(n).textContent = "–"; });
        out("apply").href = "/apply/?program=" + key;
        return;
      }
      var byCost = cost * p.ltc, byValue = val * p.ltv;
      var loan = Math.min(byCost, byValue, p.max);
      var bind = loan === p.max ? "Program maximum" : (byCost <= byValue ? "Loan-to-cost" : "Loan-to-value");
      out("loan").textContent = usd(loan);
      out("cost").textContent = usd(cost);
      out("equity").textContent = usd(Math.max(cost - loan, 0));
      out("ltc").textContent = pct(loan / cost);
      out("ltv").textContent = pct(loan / val);
      out("bind").textContent = bind;
      if (loan < p.min) {
        warn.hidden = false;
        warn.textContent = "This estimate is below the " + p.name + " program minimum of " + usd(p.min) + ". Reach out anyway; we can tell you quickly whether another structure fits.";
      }
      var q = "?program=" + key + "&a=" + num(a.value) + "&b=" + num(b.value) + "&v=" + val + "&loan=" + Math.round(loan);
      out("apply").href = "/apply/" + q;
    }
    [a, b, v].forEach(function (el) { el.addEventListener("input", calc); });
    setProgram(key);
  });

  /* Application wizard */
  var form = $("#loan-application");
  if (form) {
    var steps = $$(".form-step", form), prog = $$(".progress li"), cur = 0;
    var back = $("[data-back]", form), next = $("[data-next]", form), submit = $("[data-submit]", form);

    function show(i) {
      cur = i;
      steps.forEach(function (s, j) { s.hidden = j !== i; });
      prog.forEach(function (p, j) { p.classList.toggle("active", j === i); p.classList.toggle("done", j < i); });
      back.hidden = i === 0;
      next.hidden = i === steps.length - 1;
      submit.hidden = i !== steps.length - 1;
      if (i === steps.length - 1) buildReview();
      var top = form.getBoundingClientRect().top + window.scrollY - 110;
      if (window.scrollY > top) window.scrollTo({ top: top, behavior: "smooth" });
    }
    function validStep(i) {
      var ok = true, first = null;
      $$("[required]", steps[i]).forEach(function (el) {
        var f = el.closest(".field") || el.closest(".check-wrap");
        var good;
        if (el.type === "radio") good = !!$("[name='" + el.name + "']:checked", steps[i]);
        else if (el.type === "checkbox") good = el.checked;
        else good = el.checkValidity() && String(el.value).trim() !== "";
        if (f) f.classList.toggle("invalid", !good);
        if (!good) { ok = false; first = first || el; }
      });
      if (first) first.focus({ preventScroll: false });
      return ok;
    }
    form.addEventListener("input", function (e) {
      var f = e.target.closest(".invalid"); if (f) f.classList.remove("invalid");
      updateLabels(); metrics();
    });
    form.addEventListener("change", function () { updateLabels(); metrics(); });
    next.addEventListener("click", function () { if (validStep(cur)) show(cur + 1); });
    back.addEventListener("click", function () { show(cur - 1); });
    form.addEventListener("submit", function (e) {
      if (!validStep(cur)) { e.preventDefault(); return; }
      $$("input[data-money]", form).forEach(function (el) { el.value = el.value.replace(/,/g, ""); });
      submit.disabled = true; submit.textContent = "Submitting…";
    });

    function progKey() { var r = $("[name=program]:checked", form); return r ? r.value : "construction"; }
    function updateLabels() {
      var p = PROGRAMS[progKey()];
      $("[data-flbl=a]", form).textContent = p.costA;
      $("[data-flbl=b]", form).textContent = p.costB;
      $("[data-flbl=v]", form).textContent = p.value;
    }
    function metrics() {
      var p = PROGRAMS[progKey()];
      var cost = num(form.cost_a.value) + num(form.cost_b.value), val = num(form.value_completed.value), loan = num(form.loan_amount.value);
      var set = function (n, txt, over) { var el = $("[data-m=" + n + "]", form); el.querySelector("b").textContent = txt; el.classList.toggle("over", !!over); };
      set("cost", cost ? usd(cost) : "–");
      set("ltc", cost && loan ? pct(loan / cost) : "–", cost && loan / cost > p.ltc + 1e-9);
      set("ltv", val && loan ? pct(loan / val) : "–", val && loan / val > p.ltv + 1e-9);
      var hint = $("[data-m=hint]", form);
      hint.textContent = "Program guide: up to " + Math.round(p.ltc * 100) + "% loan-to-cost and " + Math.round(p.ltv * 100) + "% loan-to-value, " + usd(p.min) + " to " + usd(p.max) + ". Requests above the guide are still reviewed.";
    }
    function buildReview() {
      var p = PROGRAMS[progKey()];
      var rows = [
        ["Program", p.name],
        ["Purpose", form.purpose.value || "–"],
        ["Property", [form.street.value, form.city.value, form.state.value].filter(Boolean).join(", ") || "–"],
        ["Property type", form.property_type.value || "–"],
        ["Total cost", usd(num(form.cost_a.value) + num(form.cost_b.value))],
        [p.value, form.value_completed.value ? usd(num(form.value_completed.value)) : "–"],
        ["Loan requested", form.loan_amount.value ? usd(num(form.loan_amount.value)) : "–"]
      ];
      $("#review-list").innerHTML = rows.map(function (r) { return "<dt>" + r[0] + "</dt><dd>" + String(r[1]).replace(/</g, "&lt;") + "</dd>"; }).join("");
    }

    /* Prefill from the estimator or a program page */
    var qs = new URLSearchParams(location.search);
    if (qs.get("program") && PROGRAMS[qs.get("program")]) {
      var r = $("[name=program][value=" + qs.get("program") + "]", form); if (r) r.checked = true;
    }
    var fill = function (name, key) { if (qs.get(key) && num(qs.get(key)) > 0) form[name].value = Number(num(qs.get(key))).toLocaleString("en-US"); };
    fill("cost_a", "a"); fill("cost_b", "b"); fill("value_completed", "v"); fill("loan_amount", "loan");
    updateLabels(); metrics(); show(0);
  }

  /* Footer year */
  $$("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
