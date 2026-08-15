/* Administrator console enhancements. CSP-safe (served from 'self', no inline
   handlers). Everything here is progressive enhancement: with JS off, the forms
   still post and the toasts still show, they just don't get the confirm step or
   the auto-dismiss. */
(function () {
  "use strict";

  // --- Inline confirmation on important actions ----------------------------
  // A form with data-confirm="Are you sure?" gets a two-step confirm: the first
  // submit is intercepted and replaced with a Confirm / Cancel pair; only the
  // Confirm actually posts. Keeps the same guarded POST underneath.
  Array.prototype.forEach.call(
    document.querySelectorAll("form[data-confirm]"),
    function (form) {
      var armed = false;
      form.addEventListener("submit", function (e) {
        if (armed) return; // second time through: let it post
        e.preventDefault();
        if (form.querySelector(".cy-confirm")) return;

        var bar = document.createElement("div");
        bar.className = "cy-confirm";

        var msg = document.createElement("span");
        msg.className = "cy-confirm__msg";
        msg.textContent = form.getAttribute("data-confirm");

        var yes = document.createElement("button");
        yes.type = "button";
        yes.className = "cy-btn cy-btn--danger cy-btn--sm";
        yes.textContent = form.getAttribute("data-confirm-yes") || "Confirm";

        var no = document.createElement("button");
        no.type = "button";
        no.className = "cy-btn cy-btn--ghost cy-btn--sm";
        no.textContent = "Cancel";

        yes.addEventListener("click", function () {
          armed = true;
          if (form.requestSubmit) form.requestSubmit();
          else form.submit();
        });
        no.addEventListener("click", function () {
          bar.parentNode && bar.parentNode.removeChild(bar);
        });

        bar.appendChild(msg);
        bar.appendChild(yes);
        bar.appendChild(no);
        form.appendChild(bar);
      });
    }
  );

  // --- Auto-dismiss toasts --------------------------------------------------
  Array.prototype.forEach.call(
    document.querySelectorAll("[data-toast]"),
    function (toast) {
      var close = document.createElement("button");
      close.type = "button";
      close.className = "cy-toast__close";
      close.setAttribute("aria-label", "Dismiss");
      close.textContent = "×";
      close.addEventListener("click", function () {
        dismiss(toast);
      });
      toast.appendChild(close);
      window.setTimeout(function () {
        dismiss(toast);
      }, 5000);
    }
  );

  function dismiss(toast) {
    if (!toast.parentNode) return;
    toast.classList.add("is-leaving");
    window.setTimeout(function () {
      toast.parentNode && toast.parentNode.removeChild(toast);
    }, 220);
  }

  // --- Theme toggle (light / dark) -----------------------------------------
  // The toggle is a real POST form (works with JS off: it posts and reloads).
  // With JS, we flip the theme instantly and persist it via fetch, no reload.
  var root = document.querySelector(".cy-app--console");
  Array.prototype.forEach.call(
    document.querySelectorAll("form[data-theme-toggle]"),
    function (form) {
      form.addEventListener("submit", function (e) {
        if (!root || !window.fetch) return; // no root / old browser → normal post
        e.preventDefault();
        var current = root.getAttribute("data-theme") === "light" ? "light" : "dark";
        var next = current === "dark" ? "light" : "dark";
        root.setAttribute("data-theme", next);
        var hidden = form.querySelector('input[name="theme"]');
        if (hidden) hidden.value = current; // keep the no-JS fallback correct
        var token = form.querySelector('input[name="csrfmiddlewaretoken"]');
        fetch(form.getAttribute("action"), {
          method: "POST",
          headers: {
            "X-CSRFToken": token ? token.value : "",
            "X-Requested-With": "fetch",
            "Content-Type": "application/x-www-form-urlencoded",
          },
          body: "theme=" + next,
        });
      });
    }
  );

  // --- Metric toggle on the main chart -------------------------------------
  // Buttons [data-metric] show the matching [data-series] pane; no data fetch,
  // every series is already rendered server-side.
  Array.prototype.forEach.call(
    document.querySelectorAll(".cy-c-metrictoggle"),
    function (group) {
      var section = group.closest(".cy-c-section") || document;
      group.addEventListener("click", function (e) {
        var btn = e.target.closest("[data-metric]");
        if (!btn) return;
        var key = btn.getAttribute("data-metric");
        Array.prototype.forEach.call(
          group.querySelectorAll("[data-metric]"),
          function (b) {
            var on = b === btn;
            b.classList.toggle("is-active", on);
            b.setAttribute("aria-pressed", on ? "true" : "false");
          }
        );
        Array.prototype.forEach.call(
          section.querySelectorAll("[data-series]"),
          function (pane) {
            pane.classList.toggle("is-hidden", pane.getAttribute("data-series") !== key);
          }
        );
      });
    }
  );
})();
