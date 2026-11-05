(function () {
  "use strict";

  var STORAGE_KEY = "broker-removal-checklist-v1";
  var boxes = Array.prototype.slice.call(document.querySelectorAll('.checklist input[type="checkbox"]'));
  var fill = document.getElementById("progressFill");
  var bar = document.getElementById("progressBar");
  var label = document.getElementById("progressLabel");
  var filterBox = document.getElementById("filterBox");

  function safeParse(text) {
    try {
      var data = JSON.parse(text);
      return data && typeof data === "object" ? data : {};
    } catch (e) {
      return {};
    }
  }

  function load() {
    var saved = safeParse(window.localStorage.getItem(STORAGE_KEY) || "{}");
    boxes.forEach(function (box) {
      box.checked = saved[box.dataset.key] === true;
    });
  }

  function save() {
    var data = {};
    boxes.forEach(function (box) {
      data[box.dataset.key] = box.checked;
    });
    try {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
    } catch (e) {
      // Private-browsing / storage disabled: progress just won't persist.
    }
  }

  function updateProgress() {
    var total = boxes.length;
    var done = boxes.filter(function (b) { return b.checked; }).length;
    var pct = total === 0 ? 0 : Math.round((done / total) * 100);
    if (fill) { fill.style.width = pct + "%"; }
    if (bar) { bar.setAttribute("aria-valuenow", String(pct)); }
    if (label) { label.textContent = done + " of " + total + " done (" + pct + "%)"; }
  }

  function updateStyles() {
    boxes.forEach(function (box) {
      var li = box.closest("li");
      if (li) { li.classList.toggle("done", box.checked); }
    });
  }

  boxes.forEach(function (box) {
    box.addEventListener("change", function () {
      updateStyles();
      updateProgress();
      save();
    });
  });

  if (filterBox) {
    filterBox.addEventListener("input", function () {
      var q = filterBox.value.trim().toLowerCase();
      document.querySelectorAll(".checklist li").forEach(function (li) {
        var hit = q === "" || li.textContent.toLowerCase().indexOf(q) !== -1;
        li.style.display = hit ? "" : "none";
      });
    });
  }

  var resetBtn = document.getElementById("uncheckAll");
  if (resetBtn) {
    resetBtn.addEventListener("click", function () {
      if (!window.confirm("Clear all checkmarks? (Your checklist page stays; only the ticks are reset.)")) {
        return;
      }
      boxes.forEach(function (box) { box.checked = false; });
      updateStyles();
      updateProgress();
      save();
    });
  }

  var printBtn = document.getElementById("printBtn");
  if (printBtn) {
    printBtn.addEventListener("click", function () { window.print(); });
  }

  var copyIcs = document.getElementById("copyIcs");
  var copyMsg = document.getElementById("copyMsg");
  if (copyIcs && copyMsg) {
    copyIcs.addEventListener("click", function () {
      var text = document.getElementById("icsText").textContent;
      function done(ok) {
        copyMsg.textContent = ok ? "Copied — save as broker-recheck.ics and import." : "Copy failed — select the text and copy manually.";
        window.setTimeout(function () { copyMsg.textContent = ""; }, 5000);
      }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(
          function () { done(true); },
          function () { done(false); }
        );
      } else {
        var ta = document.createElement("textarea");
        ta.value = text;
        document.body.appendChild(ta);
        ta.select();
        var ok = false;
        try { ok = document.execCommand("copy"); } catch (e) { ok = false; }
        document.body.removeChild(ta);
        done(ok);
      }
    });
  }

  load();
  updateStyles();
  updateProgress();
})();
