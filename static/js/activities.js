/* Interactive lesson activities — sort, spot, inbox, password, branch.
 *
 * Each activity's container carries data-activity-kind and data-config (the id of
 * an adjacent <script type="application/json"> block written by Django's
 * json_script — inert data, CSP-safe). The matching controller renders into the
 * container and, when the learner completes it, fires `cy:solved` (bubbling) on
 * the task, which the room (lesson.js) treats like a correct answer.
 *
 * Tap-first and keyboard-operable by design; drag is only a bonus on the sort.
 * Served from static/ (script-src 'self') — no inline handlers.
 */
(function () {
  "use strict";

  var CONTROLLERS = {};

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  function solved(container) {
    container.dispatchEvent(new CustomEvent("cy:solved", { bubbles: true }));
  }

  function readConfig(container) {
    var node = document.getElementById(container.getAttribute("data-config"));
    if (!node) return null;
    try { return JSON.parse(node.textContent); } catch (e) { return null; }
  }

  // ---------------------------------------------------------------- SORT ----
  CONTROLLERS.SORT = function (root, cfg) {
    var total = cfg.items.length;
    var placed = 0;
    var selected = null;

    if (cfg.prompt) root.appendChild(el("p", "cy-act__prompt", cfg.prompt));

    var tray = el("div", "cy-sort__tray");
    root.appendChild(tray);

    var bucketsWrap = el("div", "cy-sort__buckets");
    var zones = {};
    cfg.buckets.forEach(function (b) {
      var bucket = el("div", "cy-sort__bucket");
      bucket.setAttribute("role", "button");
      bucket.setAttribute("tabindex", "0");
      bucket.setAttribute("aria-label", "Place in " + b.label);
      bucket.appendChild(el("div", "cy-sort__bucket-label", b.label));
      var zone = el("div", "cy-sort__zone");
      bucket.appendChild(zone);
      zones[b.id] = zone;
      function drop() { if (selected) place(selected, b.id); }
      bucket.addEventListener("click", drop);
      bucket.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); drop(); }
      });
      bucket.addEventListener("dragover", function (e) { e.preventDefault(); bucket.classList.add("is-over"); });
      bucket.addEventListener("dragleave", function () { bucket.classList.remove("is-over"); });
      bucket.addEventListener("drop", function (e) { e.preventDefault(); bucket.classList.remove("is-over"); drop(); });
      bucketsWrap.appendChild(bucket);
    });
    root.appendChild(bucketsWrap);

    var feedback = el("p", "cy-act__feedback");
    feedback.setAttribute("aria-live", "polite");
    root.appendChild(feedback);

    function select(chip) {
      if (selected) selected.classList.remove("is-selected");
      if (selected === chip) { selected = null; return; }
      selected = chip;
      chip.classList.add("is-selected");
    }

    function place(chip, bucketId) {
      var item = chip.__item;
      if (item.bucket === bucketId) {
        chip.classList.remove("is-selected");
        selected = null;
        var tag = el("span", "cy-sort__placed", item.text);
        tag.appendChild(el("span", "cy-sort__tick", " ✓"));
        zones[bucketId].appendChild(tag);
        tray.removeChild(chip);
        placed += 1;
        feedback.className = "cy-act__feedback is-good";
        feedback.textContent = item.why;
        if (placed === total) {
          feedback.textContent = "All sorted — nicely done.";
          solved(root);
        }
      } else {
        feedback.className = "cy-act__feedback is-bad";
        feedback.textContent = "Not quite — have another think about that one.";
        chip.classList.add("is-shake");
        window.setTimeout(function () { chip.classList.remove("is-shake"); }, 400);
      }
    }

    cfg.items.forEach(function (item) {
      var chip = el("button", "cy-sort__item", item.text);
      chip.type = "button";
      chip.__item = item;
      chip.setAttribute("draggable", "true");
      chip.addEventListener("click", function () { select(chip); });
      chip.addEventListener("dragstart", function () { select(chip); if (!selected) select(chip); });
      tray.appendChild(chip);
    });
  };

  // ---------------------------------------------------------------- SPOT ----
  CONTROLLERS.SPOT = function (root, cfg) {
    if (cfg.prompt) root.appendChild(el("p", "cy-act__prompt", cfg.prompt));

    var pair = el("div", "cy-spot__pair");
    var feedback = el("p", "cy-act__feedback");
    feedback.setAttribute("aria-live", "polite");

    function card(side, data) {
      var c = el("button", "cy-spot__card");
      c.type = "button";
      c.setAttribute("data-side", side);
      var head = el("div", "cy-spot__sender", data.sender || "");
      c.appendChild(head);
      c.appendChild(el("div", "cy-spot__text", data.text || ""));
      c.addEventListener("click", function () { pick(side, c); });
      return c;
    }

    var done = false;
    function pick(side, node) {
      if (done) return;
      if (side === cfg.fake) {
        done = true;
        node.classList.add("is-fake");
        Array.prototype.forEach.call(pair.children, function (n) {
          n.disabled = true;
          if (n.getAttribute("data-side") !== cfg.fake) n.classList.add("is-real");
        });
        feedback.className = "cy-act__feedback is-good";
        feedback.textContent = "That's the scam. " + cfg.why;
        solved(root);
      } else {
        feedback.className = "cy-act__feedback is-bad";
        feedback.textContent = "Look again — check the link, and whether it's pushing you to act fast.";
        node.classList.add("is-shake");
        window.setTimeout(function () { node.classList.remove("is-shake"); }, 400);
      }
    }

    pair.appendChild(card("left", cfg.left));
    pair.appendChild(card("right", cfg.right));
    root.appendChild(pair);
    root.appendChild(feedback);
  };

  // A kind with no controller yet (or a broken config) must never trap the
  // learner: show a gentle note and let them continue.
  function fallback(c) {
    if (c.querySelector(".cy-act__prompt")) return;
    c.appendChild(el("p", "cy-act__prompt", "Continue to carry on with the lesson."));
    solved(c);
  }

  // ---------------------------------------------------------------- init ----
  var containers = document.querySelectorAll("[data-activity]");
  Array.prototype.forEach.call(containers, function (c) {
    var fn = CONTROLLERS[c.getAttribute("data-activity-kind")];
    var cfg = readConfig(c);
    if (fn && cfg) {
      try { fn(c, cfg); } catch (e) { fallback(c); }
    } else {
      fallback(c);
    }
  });
})();
