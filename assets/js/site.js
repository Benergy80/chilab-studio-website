(function () {
  var toggle = document.querySelector("[data-theme-toggle]");
  if (toggle) {
    toggle.addEventListener("click", function () {
      var next = document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
      document.documentElement.setAttribute("data-theme", next);
      try { localStorage.setItem("chilab-theme", next); } catch (e) {}
    });
  }

  var filters = document.getElementById("filters");
  if (filters) {
    filters.addEventListener("click", function (event) {
      var button = event.target.closest("button");
      if (!button) return;
      var category = button.dataset.cat;
      filters.querySelectorAll("button").forEach(function (item) {
        item.setAttribute("aria-pressed", String(item === button));
      });
      document.querySelectorAll("[data-cat]").forEach(function (item) {
        if (item.tagName === "BUTTON") return;
        item.style.display = category === "all" || item.dataset.cat === category ? "" : "none";
      });
    });
  }

  var preview = document.getElementById("index-preview-img");
  var rows = document.querySelectorAll(".index-row[data-preview]");
  if (preview && rows.length) {
    rows.forEach(function (row) {
      row.addEventListener("mouseenter", function () {
        preview.src = row.dataset.preview;
      });
      row.addEventListener("focus", function () {
        preview.src = row.dataset.preview;
      });
    });
  }
})();
