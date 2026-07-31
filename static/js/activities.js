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

  var SVGNS = "http://www.w3.org/2000/svg";
  function icon(id) {
    // Inline sprite reference — no emoji (Cybaroo house rule), CSP-safe.
    var svg = document.createElementNS(SVGNS, "svg");
    svg.setAttribute("class", "cy-i");
    svg.setAttribute("aria-hidden", "true");
    var use = document.createElementNS(SVGNS, "use");
    use.setAttribute("href", "#" + id);
    svg.appendChild(use);
    return svg;
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
      if (cfg.variant === "login") {
        // A mini login-page mockup: an address bar (the tell) and a decorative form.
        c.classList.add("cy-spot__card--login");
        var bar = el("div", "cy-spot__urlbar");
        var lock = el("span", "cy-spot__lock");
        lock.appendChild(icon("i-lock"));
        bar.appendChild(lock);
        bar.appendChild(el("span", "cy-spot__url", data.url || ""));
        c.appendChild(bar);
        var page = el("div", "cy-spot__page");
        page.appendChild(el("div", "cy-spot__brand", data.brand || "Sign in"));
        page.appendChild(el("div", "cy-spot__field"));
        page.appendChild(el("div", "cy-spot__field"));
        page.appendChild(el("div", "cy-spot__signin", "Sign in"));
        c.appendChild(page);
      } else {
        c.appendChild(el("div", "cy-spot__sender", data.sender || ""));
        c.appendChild(el("div", "cy-spot__text", data.text || ""));
      }
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

  // --------------------------------------------------------------- INBOX ----
  CONTROLLERS.INBOX = function (root, cfg) {
    if (cfg.prompt) root.appendChild(el("p", "cy-act__prompt", cfg.prompt));

    var card = el("div", "cy-inbox");
    var totalBad = 0, found = 0;

    cfg.parts.forEach(function (part) {
      if (part.bad) totalBad += 1;
      var row = el("div", "cy-inbox__row");
      row.appendChild(el("span", "cy-inbox__zone", part.zone));
      var btn = el("button", "cy-inbox__part", part.text);
      btn.type = "button";
      var note = el("span", "cy-inbox__why");
      btn.addEventListener("click", function () {
        if (btn.disabled) return;
        btn.disabled = true;
        note.textContent = part.why;
        if (part.bad) {
          btn.classList.add("is-bad");
          note.classList.add("is-bad");
          found += 1;
          update();
          if (found === totalBad) {
            feedback.className = "cy-act__feedback is-good";
            feedback.textContent = "That's all the tells — you'd spot this in real life.";
            solved(root);
          }
        } else {
          btn.classList.add("is-ok");
          note.classList.add("is-ok");
        }
      });
      row.appendChild(btn);
      row.appendChild(note);
      card.appendChild(row);
    });
    root.appendChild(card);

    var counter = el("p", "cy-inbox__count");
    var feedback = el("p", "cy-act__feedback");
    feedback.setAttribute("aria-live", "polite");
    root.appendChild(counter);
    root.appendChild(feedback);

    function update() {
      counter.textContent = found + " of " + totalBad + " tells found";
    }
    update();
  };

  // ------------------------------------------------------------ PASSWORD ----
  CONTROLLERS.PASSWORD = function (root, cfg) {
    if (cfg.prompt) root.appendChild(el("p", "cy-act__prompt", cfg.prompt));
    var common = (cfg.common || []).map(function (s) { return String(s).toLowerCase(); });
    var done = false;

    var wrap = el("div", "cy-pw");
    var input = el("input", "cy-pw__input");
    input.type = "text";
    input.setAttribute("autocomplete", "off");
    input.setAttribute("autocapitalize", "off");
    input.setAttribute("spellcheck", "false");
    input.setAttribute("aria-label", "Try a password");
    input.setAttribute("placeholder", "Type a password to test…");
    wrap.appendChild(input);

    var meter = el("div", "cy-pw__meter");
    var bar = el("div", "cy-pw__bar");
    meter.appendChild(bar);
    wrap.appendChild(meter);
    var label = el("p", "cy-pw__label", "Start typing…");
    wrap.appendChild(label);

    var checks = [
      { key: "len", text: "At least 12 characters", test: function (v) { return v.length >= 12; } },
      { key: "mix", text: "A mix of character types, or a few words", test: function (v) {
          var classes = 0;
          if (/[a-z]/.test(v)) classes++;
          if (/[A-Z]/.test(v)) classes++;
          if (/[0-9]/.test(v)) classes++;
          if (/[^a-zA-Z0-9]/.test(v)) classes++;
          return classes >= 2 || v.trim().indexOf(" ") > 0;
      } },
      { key: "common", text: "Not a common or guessable password", test: function (v) {
          var low = v.toLowerCase();
          return v.length > 0 && common.indexOf(low) === -1;
      } },
    ];
    var list = el("ul", "cy-pw__checks");
    checks.forEach(function (c) {
      c.node = el("li", "cy-pw__check", c.text);
      list.appendChild(c.node);
    });
    wrap.appendChild(list);

    if (cfg.tips && cfg.tips.length) {
      var tips = el("ul", "cy-pw__tips");
      cfg.tips.forEach(function (t) { tips.appendChild(el("li", null, t)); });
      wrap.appendChild(tips);
    }

    var feedback = el("p", "cy-act__feedback");
    feedback.setAttribute("aria-live", "polite");
    wrap.appendChild(feedback);
    root.appendChild(wrap);

    function grade() {
      var v = input.value;
      var passed = 0;
      checks.forEach(function (c) {
        var ok = c.test(v);
        c.node.classList.toggle("is-pass", ok);
        if (ok) passed += 1;
      });
      var strength = v.length === 0 ? "" : passed <= 1 ? "weak" : passed === 2 ? "fair" : "strong";
      bar.setAttribute("data-strength", strength);
      label.textContent = strength ? "Strength: " + strength : "Start typing…";
      label.className = "cy-pw__label is-" + (strength || "none");
      if (strength === "strong" && !done) {
        done = true;
        feedback.className = "cy-act__feedback is-good";
        feedback.textContent = "That's a strong one — long, mixed and not guessable.";
        solved(root);
      }
    }
    input.addEventListener("input", grade);
  };

  // -------------------------------------------------------------- BRANCH ----
  CONTROLLERS.BRANCH = function (root, cfg) {
    if (cfg.prompt) root.appendChild(el("p", "cy-act__prompt", cfg.prompt));

    var box = el("div", "cy-branch");
    var scene = el("p", "cy-branch__scene");
    scene.setAttribute("aria-live", "polite");
    var choices = el("div", "cy-branch__choices");
    var feedback = el("p", "cy-act__feedback cy-branch__feedback");
    feedback.setAttribute("aria-live", "polite");
    box.appendChild(scene);
    box.appendChild(choices);
    box.appendChild(feedback);
    root.appendChild(box);

    function clear(node) { while (node.firstChild) node.removeChild(node.firstChild); }

    function renderNode(id) {
      var node = cfg.nodes[id];
      if (!node) return;
      scene.textContent = node.text;
      clear(choices);
      feedback.textContent = "";
      feedback.className = "cy-act__feedback cy-branch__feedback";

      if (!node.choices || node.choices.length === 0) {
        box.classList.add("is-complete");
        scene.classList.add("is-ending");
        solved(root);
        return;
      }
      node.choices.forEach(function (ch) {
        var b = el("button", "cy-branch__choice", ch.label);
        b.type = "button";
        b.addEventListener("click", function () { choose(ch); });
        choices.appendChild(b);
      });
    }

    function choose(ch) {
      // Lock the current choices.
      Array.prototype.forEach.call(choices.children, function (b) { b.disabled = true; });
      if (ch.feedback) {
        feedback.className = "cy-act__feedback cy-branch__feedback is-" +
          (ch.outcome === "good" ? "good" : ch.outcome === "bad" ? "bad" : "neutral");
        feedback.textContent = ch.feedback;
        var next = el("button", "cy-btn cy-btn--primary cy-branch__next", "Continue");
        next.type = "button";
        next.addEventListener("click", function () { renderNode(ch.to); });
        choices.appendChild(next);
      } else {
        renderNode(ch.to);
      }
    }

    renderNode(cfg.start);
  };

  // ------------------------------------------------------------ CLASSIFY ----
  // Read one alert/event at a time and pick its category. Distinct from SORT:
  // each event is a card diagnosed on the spot, with teaching feedback. Solved
  // when every event is correctly categorised.
  CONTROLLERS.CLASSIFY = function (root, cfg) {
    if (cfg.prompt) root.appendChild(el("p", "cy-act__prompt", cfg.prompt));
    var total = cfg.events.length;
    var done = 0;

    var counter = el("p", "cy-classify__count");
    counter.setAttribute("aria-live", "polite");
    var feedback = el("p", "cy-act__feedback");
    feedback.setAttribute("aria-live", "polite");

    var list = el("div", "cy-classify");
    cfg.events.forEach(function (event) {
      var card = el("div", "cy-classify__event");
      card.appendChild(el("p", "cy-classify__text", event.text));

      var opts = el("div", "cy-classify__opts");
      var why = el("p", "cy-classify__why");
      var settled = false;

      cfg.categories.forEach(function (cat) {
        var b = el("button", "cy-classify__opt", cat.label);
        b.type = "button";
        b.addEventListener("click", function () {
          if (settled) return;
          if (cat.id === event.category) {
            settled = true;
            card.classList.add("is-correct");
            b.classList.add("is-right");
            why.className = "cy-classify__why is-good";
            why.textContent = event.why;
            Array.prototype.forEach.call(opts.children, function (o) { o.disabled = true; });
            done += 1;
            update();
            if (done === total) {
              feedback.className = "cy-act__feedback is-good";
              feedback.textContent = "All classified — that is the recognising-threats skill in action.";
              solved(root);
            }
          } else {
            b.classList.add("is-wrong");
            b.disabled = true;
            card.classList.add("is-shake");
            window.setTimeout(function () { card.classList.remove("is-shake"); }, 400);
            why.className = "cy-classify__why is-bad";
            why.textContent = "Not that one. Look at the signature again and try another.";
          }
        });
        opts.appendChild(b);
      });

      card.appendChild(opts);
      card.appendChild(why);
      list.appendChild(card);
    });

    root.appendChild(counter);
    root.appendChild(list);
    root.appendChild(feedback);

    function update() { counter.textContent = done + " of " + total + " classified"; }
    update();
  };

  // ------------------------------------------------------------ MAILSORT ----
  // A realistic mixed inbox: mark each whole email Genuine or Phishing, with the
  // verdict and its tells revealed as you go. Distinct from INBOX (which inspects
  // the parts within a single message). Solved when every email is sorted right.
  CONTROLLERS.MAILSORT = function (root, cfg) {
    if (cfg.prompt) root.appendChild(el("p", "cy-act__prompt", cfg.prompt));
    var total = cfg.emails.length;
    var done = 0;

    var counter = el("p", "cy-mail__count");
    counter.setAttribute("aria-live", "polite");
    var feedback = el("p", "cy-act__feedback");
    feedback.setAttribute("aria-live", "polite");

    var listEl = el("div", "cy-mail");
    cfg.emails.forEach(function (email) {
      var row = el("div", "cy-mail__row");
      row.appendChild(el("span", "cy-mail__from", email.from));
      row.appendChild(el("p", "cy-mail__subject", email.subject));
      row.appendChild(el("p", "cy-mail__preview", email.preview));

      var verdicts = el("div", "cy-mail__verdicts");
      var why = el("p", "cy-mail__why");
      var settled = false;
      var correct = email.phish ? "phishing" : "genuine";

      [["genuine", "Genuine"], ["phishing", "Phishing"]].forEach(function (pair) {
        var b = el("button", "cy-mail__verdict cy-mail__verdict--" + pair[0], pair[1]);
        b.type = "button";
        b.addEventListener("click", function () {
          if (settled) return;
          if (pair[0] === correct) {
            settled = true;
            row.classList.add("is-settled", email.phish ? "is-phish" : "is-genuine");
            b.classList.add("is-right");
            why.className = "cy-mail__why is-good";
            why.textContent = (email.phish ? "Phishing. " : "Genuine. ") + email.why;
            Array.prototype.forEach.call(verdicts.children, function (o) { o.disabled = true; });
            done += 1;
            update();
            if (done === total) {
              feedback.className = "cy-act__feedback is-good";
              feedback.textContent = "Inbox triaged. Every message sorted correctly.";
              solved(root);
            }
          } else {
            b.classList.add("is-wrong");
            b.disabled = true;
            row.classList.add("is-shake");
            window.setTimeout(function () { row.classList.remove("is-shake"); }, 400);
            why.className = "cy-mail__why is-bad";
            why.textContent = "Look again at the sender and what it is asking, then try the other verdict.";
          }
        });
        verdicts.appendChild(b);
      });

      row.appendChild(verdicts);
      row.appendChild(why);
      listEl.appendChild(row);
    });

    root.appendChild(counter);
    root.appendChild(listEl);
    root.appendChild(feedback);

    function update() { counter.textContent = done + " of " + total + " sorted"; }
    update();
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
