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

  // ---------------------------------------------------------- .cy-br chrome ----
  // A realistic Chrome-style browser frame (tabs with favicon, omnibox with
  // security state, a bookmarks bar), built from a small `frame` spec so an
  // activity's own content sits inside real device chrome instead of a bare
  // card. Shared by NETMAP, SPOT, MAILSORT and HARDEN. frame:
  // {tab, fav, favbg, url_prefix, url, url_bold, insecure, marks:[{label,bg}]}
  // Returns the outer .cy-br node; call .appendChild on the returned __view.
  function buildBrowserFrame(frame) {
    var br = el("div", "cy-br");

    var tabs = el("div", "cy-br__tabs");
    var lights = el("span", "cy-br__lights");
    lights.appendChild(el("i")); lights.appendChild(el("i")); lights.appendChild(el("i"));
    tabs.appendChild(lights);
    var tab = el("span", "cy-br__tab is-on");
    var fav = el("b", "cy-br__fav", frame.fav || "");
    if (frame.favbg) fav.style.background = frame.favbg;
    tab.appendChild(fav);
    tab.appendChild(el("span", null, frame.tab || ""));
    tab.appendChild(el("i", "cy-br__x", "×"));
    tabs.appendChild(tab);
    tabs.appendChild(el("span", "cy-br__plus", "+"));
    br.appendChild(tabs);

    var bar = el("div", "cy-br__bar");
    bar.appendChild(el("span", "cy-br__nav", "← →"));
    bar.appendChild(el("span", "cy-br__reload", "↻"));
    var omni = el("span", "cy-br__omni");
    var lk = el("span", "cy-br__lk");
    lk.appendChild(icon(frame.insecure ? "i-eye" : "i-lock"));
    omni.appendChild(lk);
    if (frame.insecure) omni.appendChild(el("span", "cy-br__ns", "Not secure"));
    var urlSpan = el("span", "cy-br__url");
    urlSpan.appendChild(el("span", "g", frame.url_prefix || ""));
    urlSpan.appendChild(document.createTextNode(frame.url || ""));
    if (frame.url_bold) urlSpan.appendChild(el("b", null, frame.url_bold));
    omni.appendChild(urlSpan);
    bar.appendChild(omni);
    br.appendChild(bar);

    if (frame.marks && frame.marks.length) {
      var marks = el("div", "cy-br__marks");
      frame.marks.forEach(function (m) {
        var mk = el("span", "cy-br__mark");
        var b = el("b"); b.style.background = m.bg || "#888";
        mk.appendChild(b);
        mk.appendChild(document.createTextNode(m.label));
        marks.appendChild(mk);
      });
      br.appendChild(marks);
    }

    var view = el("div", "cy-br__view");
    br.appendChild(view);
    br.__view = view;
    return br;
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
      if (cfg.variant === "login" && data.tab) {
        // Photograph-grade: a full mini browser window per side, the address bar
        // (and its padlock / Not secure state) carrying the actual tell.
        var frame = {
          tab: data.tab, fav: (data.brand || "S").slice(0, 1).toUpperCase(),
          favbg: data.insecure ? "#c5221f" : "#1b4b82",
          url_prefix: data.insecure ? "http://" : "https://",
          url: data.url || "", insecure: !!data.insecure,
        };
        var br = buildBrowserFrame(frame);
        br.classList.add("cy-spot__br");
        var page = el("div", "cy-lgn");
        var card2 = el("div", "cy-lgn__card");
        card2.appendChild(el("div", "cy-lgn__brand", data.brand || "Sign in"));
        card2.appendChild(el("div", "cy-lgn__lbl", "Email address"));
        card2.appendChild(el("div", "cy-lgn__inp", "you@example.com"));
        card2.appendChild(el("div", "cy-lgn__lbl", "Password"));
        var pwd = el("div", "cy-lgn__inp");
        pwd.appendChild(el("span", "dots", "••••••••••"));
        card2.appendChild(pwd);
        card2.appendChild(el("div", "cy-lgn__btn", "Sign in"));
        page.appendChild(card2);
        br.__view.appendChild(page);

        var btn = el("button", "cy-spot__card cy-spot__card--frame");
        btn.type = "button";
        btn.setAttribute("data-side", side);
        btn.appendChild(br);
        btn.addEventListener("click", function () { pick(side, btn); });
        return btn;
      }
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
        var page2 = el("div", "cy-spot__page");
        page2.appendChild(el("div", "cy-spot__brand", data.brand || "Sign in"));
        page2.appendChild(el("div", "cy-spot__field"));
        page2.appendChild(el("div", "cy-spot__field"));
        page2.appendChild(el("div", "cy-spot__signin", "Sign in"));
        c.appendChild(page2);
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
  var AVATAR_BG = ["#1a73e8", "#137333", "#c5221f", "#8430ce", "#d56e0c", "#12805c"];
  function avatarColor(name) {
    var h = 0;
    for (var i = 0; i < name.length; i++) h = (h * 31 + name.charCodeAt(i)) >>> 0;
    return AVATAR_BG[h % AVATAR_BG.length];
  }

  CONTROLLERS.MAILSORT = function (root, cfg) {
    if (cfg.prompt) root.appendChild(el("p", "cy-act__prompt", cfg.prompt));
    var total = cfg.emails.length;
    var done = 0;

    var counter = el("p", "cy-mail__count");
    counter.setAttribute("aria-live", "polite");
    var feedback = el("p", "cy-act__feedback");
    feedback.setAttribute("aria-live", "polite");

    function buildRow(email, listEl, gmail) {
      var row = el("div", gmail ? "cy-gm__row" : "cy-mail__row");
      var settled = false;
      var correct = email.phish ? "phishing" : "genuine";
      var why = el("p", gmail ? "cy-gm__why" : "cy-mail__why");

      if (gmail) {
        var main = el("div", "cy-gm__main");
        var av = el("span", "cy-gm__avatar", (email.from || "?").slice(0, 1).toUpperCase());
        av.style.background = avatarColor(email.from || "?");
        main.appendChild(av);
        var body = el("div", "cy-gm__body");
        var head = el("div", "cy-gm__head");
        var fromWrap = el("span", "cy-gm__fromwrap");
        if (email.unread) fromWrap.appendChild(el("span", "cy-gm__dot"));
        fromWrap.appendChild(el("span", "cy-gm__from", email.from || ""));
        head.appendChild(fromWrap);
        head.appendChild(el("span", "cy-gm__time", email.time || ""));
        body.appendChild(head);
        if (email.addr) body.appendChild(el("div", "cy-gm__addr", email.addr));
        var subj = el("div", "cy-gm__subjline");
        subj.appendChild(el("span", "cy-gm__subject", email.subject || ""));
        subj.appendChild(el("span", "cy-gm__preview", ": " + (email.preview || "")));
        body.appendChild(subj);
        main.appendChild(body);
        row.appendChild(main);
        if (email.unread) row.classList.add("is-unread");
      } else {
        row.appendChild(el("span", "cy-mail__from", email.from));
        row.appendChild(el("p", "cy-mail__subject", email.subject));
        row.appendChild(el("p", "cy-mail__preview", email.preview));
      }

      var verdicts = el("div", gmail ? "cy-gm__verdicts" : "cy-mail__verdicts");
      [["genuine", "Genuine"], ["phishing", "Phishing"]].forEach(function (pair) {
        var b = el("button", (gmail ? "cy-gm__verdict cy-gm__verdict--" : "cy-mail__verdict cy-mail__verdict--") + pair[0], pair[1]);
        b.type = "button";
        b.addEventListener("click", function () {
          if (settled) return;
          if (pair[0] === correct) {
            settled = true;
            row.classList.add("is-settled", email.phish ? "is-phish" : "is-genuine");
            row.classList.remove("is-unread");
            b.classList.add("is-right");
            why.className = (gmail ? "cy-gm__why" : "cy-mail__why") + " is-good";
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
            why.className = (gmail ? "cy-gm__why" : "cy-mail__why") + " is-bad";
            why.textContent = "Look again at the sender and what it is asking, then try the other verdict.";
          }
        });
        verdicts.appendChild(b);
      });

      row.appendChild(verdicts);
      row.appendChild(why);
      listEl.appendChild(row);
    }

    if (cfg.gmail && cfg.frame) {
      // Photograph-grade: a real Gmail layout (sidebar, toolbar, avatar rows)
      // inside full browser chrome, instead of plain cards.
      var br = buildBrowserFrame(cfg.frame);
      var gm = el("div", "cy-gm");
      var side = el("div", "cy-gm__side");
      side.appendChild(el("span", "cy-gm__compose", "Compose"));
      [["Inbox", String(total), true], ["Starred", "", false], ["Sent", "", false], ["Trash", "", false]].forEach(function (s) {
        var item = el("span", "cy-gm__sideitem" + (s[2] ? " is-on" : ""));
        item.appendChild(el("span", null, s[0]));
        if (s[1]) item.appendChild(el("b", null, s[1]));
        side.appendChild(item);
      });
      gm.appendChild(side);
      var main2 = el("div", "cy-gm__mainpane");
      var toolbar = el("div", "cy-gm__toolbar");
      toolbar.appendChild(el("span", null, "Trust account · Inbox"));
      main2.appendChild(toolbar);
      var listEl = el("div", "cy-gm__list");
      cfg.emails.forEach(function (email) { buildRow(email, listEl, true); });
      main2.appendChild(listEl);
      gm.appendChild(main2);
      br.__view.appendChild(gm);

      root.appendChild(counter);
      root.appendChild(br);
      root.appendChild(feedback);
      update();
      return;
    }

    var listEl2 = el("div", "cy-mail");
    cfg.emails.forEach(function (email) { buildRow(email, listEl2, false); });
    root.appendChild(counter);
    root.appendChild(listEl2);
    root.appendChild(feedback);

    function update() { counter.textContent = done + " of " + total + " sorted"; }
    update();
  };

  // ------------------------------------------------------------ HARDEN ----
  // Secure a workspace step by step: each part starts "At risk" and you pick the
  // secure fix, watching it flip to "Secured". Each step carries its own options
  // (unlike CLASSIFY's shared categories). Solved when every part is secured.
  CONTROLLERS.HARDEN = function (root, cfg) {
    if (cfg.prompt) root.appendChild(el("p", "cy-act__prompt", cfg.prompt));
    var total = cfg.steps.length;
    var done = 0;

    var counter = el("p", "cy-harden__count");
    counter.setAttribute("aria-live", "polite");
    var feedback = el("p", "cy-act__feedback");
    feedback.setAttribute("aria-live", "polite");

    function buildStep(step, listEl, settingsUI) {
      var card = el("div", settingsUI ? "cy-rtr__row cy-rtr__row--fix" : "cy-harden__step");
      var settled = false;

      if (settingsUI) {
        var top = el("div", "cy-rtr__fixtop");
        var kwrap = el("span", "cy-rtr__k", step.label);
        if (step.value) kwrap.appendChild(el("small", null, step.risk || ""));
        top.appendChild(kwrap);
        var status = el("span", "cy-rtr__pill cy-rtr__pill--bad", step.value || "At risk");
        top.appendChild(status);
        card.appendChild(top);
        var opts = el("div", "cy-rtr__fixopts");
        var why = el("p", "cy-netmap__why");
        step.options.forEach(function (opt) {
          var b = el("button", "cy-rtr__btn cy-rtr__btn--opt", opt.text);
          b.type = "button";
          b.addEventListener("click", function () { settle(opt, b); });
          opts.appendChild(b);
        });
        card.appendChild(opts);
        card.appendChild(why);
      } else {
        var head = el("div", "cy-harden__head");
        head.appendChild(el("span", "cy-harden__label", step.label));
        var status2 = el("span", "cy-harden__status", "At risk");
        head.appendChild(status2);
        card.appendChild(head);
        if (step.risk) card.appendChild(el("p", "cy-harden__risk", step.risk));
        var opts2 = el("div", "cy-harden__opts");
        var why2 = el("p", "cy-harden__why");
        step.options.forEach(function (opt) {
          var b2 = el("button", "cy-harden__opt", opt.text);
          b2.type = "button";
          b2.addEventListener("click", function () { settle(opt, b2); });
          opts2.appendChild(b2);
        });
        card.appendChild(opts2);
        card.appendChild(why2);
        var status = status2, opts = opts2, why = why2;
      }

      function settle(opt, btn) {
        if (settled) return;
        if (opt.correct) {
          settled = true;
          card.classList.add(settingsUI ? "is-fixed" : "is-secured");
          status.textContent = "Secured";
          status.className = settingsUI ? "cy-rtr__pill cy-rtr__pill--ok" : "cy-harden__status";
          btn.classList.add("is-right");
          why.className = (settingsUI ? "cy-netmap__why" : "cy-harden__why") + " is-good";
          why.textContent = opt.why;
          Array.prototype.forEach.call(opts.children, function (o) { o.disabled = true; });
          done += 1;
          update();
          if (done === total) {
            feedback.className = "cy-act__feedback is-good";
            feedback.textContent = "Workspace secured. Every part locked down.";
            solved(root);
          }
        } else {
          btn.classList.add("is-wrong");
          btn.disabled = true;
          card.classList.add("is-shake");
          window.setTimeout(function () { card.classList.remove("is-shake"); }, 400);
          why.className = (settingsUI ? "cy-netmap__why" : "cy-harden__why") + " is-bad";
          why.textContent = opt.why || "That leaves a gap. Try the more secure option.";
        }
      }

      listEl.appendChild(card);
    }

    if (cfg.settings && cfg.frame) {
      // Photograph-grade: a real settings page (rows with a status pill that
      // flips to Secured) inside full browser chrome, instead of plain cards.
      var br = buildBrowserFrame(cfg.frame);
      var rtr = el("div", "cy-rtr cy-rtr--tap");
      var main = el("div", "cy-rtr__main cy-rtr__main--full");
      main.appendChild(el("p", "cy-rtr__h", "Security"));
      main.appendChild(el("p", "cy-rtr__lede", "Settings that need fixing before this account is safe."));
      cfg.steps.forEach(function (step) { buildStep(step, main, true); });
      rtr.appendChild(main);
      br.__view.appendChild(rtr);

      root.appendChild(counter);
      root.appendChild(br);
      root.appendChild(feedback);
      update();
      return;
    }

    var listEl2 = el("div", "cy-harden");
    cfg.steps.forEach(function (step) { buildStep(step, listEl2, false); });
    root.appendChild(counter);
    root.appendChild(listEl2);
    root.appendChild(feedback);

    function update() { counter.textContent = done + " of " + total + " secured"; }
    update();
  };

  // ------------------------------------------------------------ NETMAP ----
  // Find the weaknesses on a network map: each device is a node you can tap; the
  // weak ones reveal why and count toward the total. The spatial cousin of INBOX.
  // Solved when every weakness has been found.
  CONTROLLERS.NETMAP = function (root, cfg) {
    if (cfg.prompt) root.appendChild(el("p", "cy-act__prompt", cfg.prompt));
    var totalWeak = 0, found = 0;
    cfg.nodes.forEach(function (n) { if (n.weak) totalWeak += 1; });

    var counter = el("p", "cy-netmap__count");
    counter.setAttribute("aria-live", "polite");
    var feedback = el("p", "cy-act__feedback");
    feedback.setAttribute("aria-live", "polite");

    function update() { counter.textContent = found + " of " + totalWeak + " weaknesses found"; }
    function onSettle(node, why, n) {
      why.textContent = n.why;
      if (n.weak) {
        node.classList.add("is-weak");
        why.className = why.className.replace(/\bis-ok\b/, "") + " is-weak";
        found += 1;
        update();
        if (found === totalWeak) {
          feedback.className = "cy-act__feedback is-good";
          feedback.textContent = "That is every weakness found. You would spot these on a real network.";
          solved(root);
        }
      } else {
        node.classList.add("is-ok");
        why.className = why.className.replace(/\bis-weak\b/, "") + " is-ok";
      }
    }

    if (cfg.frame) {
      // Photograph-grade: a real router "Attached devices" table inside full
      // browser chrome. Each row is tappable; tapping reveals why underneath it.
      var br = buildBrowserFrame(cfg.frame);
      var rtr = el("div", "cy-rtr cy-rtr--tap");
      var main = el("div", "cy-rtr__main cy-rtr__main--full");
      main.appendChild(el("p", "cy-rtr__h", "Attached devices"));
      main.appendChild(el("p", "cy-rtr__lede", cfg.nodes.length + " devices connected through this router."));
      var wrap = el("div", "cy-rtr__tblwrap");
      var tbl = el("table", "cy-rtr__tbl cy-rtr__tbl--tap");
      var thead = el("thead");
      var hr = el("tr");
      ["Device", ""].forEach(function (h) { hr.appendChild(el("th", null, h)); });
      thead.appendChild(hr);
      tbl.appendChild(thead);
      var tbody = el("tbody");
      cfg.nodes.forEach(function (n) {
        var row = el("tr", "cy-rtr__row2");
        var tdDev = el("td");
        var btn = el("button", "cy-rtr__tapbtn", n.label);
        btn.type = "button";
        var detail = el("span", "cy-rtr__mac", n.detail || "");
        tdDev.appendChild(btn);
        tdDev.appendChild(document.createElement("br"));
        tdDev.appendChild(detail);
        var tdStat = el("td");
        var pill = el("span", "cy-rtr__pill cy-rtr__pill--tap", "Check");
        tdStat.appendChild(pill);
        row.appendChild(tdDev);
        row.appendChild(tdStat);
        var whyRow = el("tr", "cy-rtr__whyrow");
        var whyTd = el("td");
        whyTd.colSpan = 2;
        var why = el("p", "cy-netmap__why");
        whyTd.appendChild(why);
        whyRow.appendChild(whyTd);

        btn.addEventListener("click", function () {
          if (btn.disabled) return;
          btn.disabled = true;
          row.classList.add("is-settled");
          onSettle(row, why, n);
          pill.textContent = n.weak ? "Suspicious" : "Known";
          pill.className = "cy-rtr__pill " + (n.weak ? "cy-rtr__pill--bad" : "cy-rtr__pill--ok");
        });

        tbody.appendChild(row);
        tbody.appendChild(whyRow);
      });
      tbl.appendChild(tbody);
      wrap.appendChild(tbl);
      main.appendChild(wrap);
      rtr.appendChild(main);
      br.__view.appendChild(rtr);

      root.appendChild(counter);
      root.appendChild(br);
      root.appendChild(feedback);
      update();
      return;
    }

    var grid = el("div", "cy-netmap");
    cfg.nodes.forEach(function (n) {
      var cell = el("div", "cy-netmap__cell");
      var node = el("button", "cy-netmap__node");
      node.type = "button";
      node.appendChild(el("span", "cy-netmap__label", n.label));
      if (n.detail) node.appendChild(el("span", "cy-netmap__detail", n.detail));
      var why = el("p", "cy-netmap__why");

      node.addEventListener("click", function () {
        if (node.disabled) return;
        node.disabled = true;
        onSettle(node, why, n);
      });

      cell.appendChild(node);
      cell.appendChild(why);
      grid.appendChild(cell);
    });

    root.appendChild(counter);
    root.appendChild(grid);
    root.appendChild(feedback);
    update();
  };

  // ------------------------------------------------------------ SEQUENCE ----
  // Put steps in the correct order: they appear shuffled and you tap them 1..N
  // in sequence. A wrong tap nudges. Solved when all are placed in order.
  CONTROLLERS.SEQUENCE = function (root, cfg) {
    if (cfg.prompt) root.appendChild(el("p", "cy-act__prompt", cfg.prompt));
    var total = cfg.steps.length;
    var next = 1; // the order value expected next

    var counter = el("p", "cy-seq__count");
    counter.setAttribute("aria-live", "polite");
    var feedback = el("p", "cy-act__feedback");
    feedback.setAttribute("aria-live", "polite");

    // Shuffle a copy for display so the order is a genuine challenge.
    var shuffled = cfg.steps.slice();
    for (var i = shuffled.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = shuffled[i]; shuffled[i] = shuffled[j]; shuffled[j] = t;
    }

    var list = el("ol", "cy-seq");
    shuffled.forEach(function (step) {
      var li = el("li", "cy-seq__item");
      var btn = el("button", "cy-seq__btn");
      btn.type = "button";
      var num = el("span", "cy-seq__num");
      var bodyWrap = el("span", "cy-seq__body");
      bodyWrap.appendChild(el("span", "cy-seq__label", step.label));
      if (step.detail) bodyWrap.appendChild(el("span", "cy-seq__detail", step.detail));
      btn.appendChild(num);
      btn.appendChild(bodyWrap);

      btn.addEventListener("click", function () {
        if (btn.disabled) return;
        if (step.order === next) {
          btn.disabled = true;
          btn.classList.add("is-placed");
          num.textContent = next;
          next += 1;
          update();
          if (next > total) {
            feedback.className = "cy-act__feedback is-good";
            feedback.textContent = "That is the lifecycle in order. Well sequenced.";
            solved(root);
          }
        } else {
          btn.classList.add("is-wrong");
          window.setTimeout(function () { btn.classList.remove("is-wrong"); }, 400);
          feedback.className = "cy-act__feedback is-bad";
          feedback.textContent = "Not the next one. Which phase comes at step " + next + "?";
        }
      });

      li.appendChild(btn);
      list.appendChild(li);
    });

    root.appendChild(counter);
    root.appendChild(list);
    root.appendChild(feedback);

    function update() { counter.textContent = (next - 1) + " of " + total + " in order"; }
    update();
  };

  // ------------------------------------------------------------ RESPOND ----
  // Apply-it: several realistic situations, each with a few possible responses.
  // Pick the soundest action and see the consequence; a poor pick shows what
  // would happen and lets you try again. Solved when every situation is handled
  // on its sound response. The "do the right thing" workhorse.
  CONTROLLERS.RESPOND = function (root, cfg) {
    if (cfg.prompt) root.appendChild(el("p", "cy-act__prompt", cfg.prompt));
    var total = cfg.situations.length;
    var done = 0;

    var counter = el("p", "cy-respond__count");
    counter.setAttribute("aria-live", "polite");
    var feedback = el("p", "cy-act__feedback");
    feedback.setAttribute("aria-live", "polite");

    var list = el("div", "cy-respond");
    cfg.situations.forEach(function (sit) {
      var card = el("div", "cy-respond__sit");
      card.appendChild(el("p", "cy-respond__text", sit.text));

      var opts = el("div", "cy-respond__opts");
      var why = el("p", "cy-respond__why");
      var settled = false;

      sit.options.forEach(function (opt) {
        var b = el("button", "cy-respond__opt", opt.text);
        b.type = "button";
        b.addEventListener("click", function () {
          if (settled) return;
          if (opt.outcome === "good") {
            settled = true;
            card.classList.add("is-good");
            b.classList.add("is-right");
            why.className = "cy-respond__why is-good";
            why.textContent = opt.feedback;
            Array.prototype.forEach.call(opts.children, function (o) { o.disabled = true; });
            done += 1;
            update();
            if (done === total) {
              feedback.className = "cy-act__feedback is-good";
              feedback.textContent = "Every situation handled well. That is the judgement that keeps a workplace safe.";
              solved(root);
            }
          } else {
            b.classList.add(opt.outcome === "risky" ? "is-risky" : "is-wrong");
            b.disabled = true;
            card.classList.add("is-shake");
            window.setTimeout(function () { card.classList.remove("is-shake"); }, 400);
            why.className = "cy-respond__why is-bad";
            why.textContent = opt.feedback;
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

    function update() { counter.textContent = done + " of " + total + " handled"; }
    update();
  };

  // ------------------------------------------------------------ QUIZSET ----
  // A mixed knowledge-check: several sub-questions of different types (mcq,
  // truefalse, fill, match). Each grades on its own with instant feedback, a
  // hint and retry. Solved once every sub-question has been answered correctly.
  CONTROLLERS.QUIZSET = function (root, cfg) {
    if (cfg.prompt) root.appendChild(el("p", "cy-act__prompt", cfg.prompt));
    var qs = cfg.questions || [];
    var total = qs.length;
    var done = 0;

    var counter = el("p", "cy-qz__count");
    counter.setAttribute("aria-live", "polite");
    var feedback = el("p", "cy-act__feedback");
    feedback.setAttribute("aria-live", "polite");
    var list = el("div", "cy-qz");

    function update() { counter.textContent = done + " of " + total + " correct"; }
    function onCorrect() {
      done += 1;
      update();
      if (done === total) {
        feedback.className = "cy-act__feedback is-good";
        feedback.textContent = "Every one correct. That is the whole idea pulled together.";
        solved(root);
      }
    }
    function norm(s) { return String(s == null ? "" : s).trim().toLowerCase().replace(/\s+/g, " "); }
    function nudge(node, cls) {
      node.classList.add(cls || "is-shake");
      window.setTimeout(function () { node.classList.remove("is-shake"); }, 400);
    }

    function hintRow(card, hint) {
      if (!hint) return;
      var btn = el("button", "cy-qz__hint-toggle"); btn.type = "button";
      btn.appendChild(icon("i-star"));
      btn.appendChild(el("span", null, " Need a hint?"));
      var note = el("p", "cy-qz__hint"); note.hidden = true; note.textContent = hint;
      btn.addEventListener("click", function () { note.hidden = !note.hidden; });
      card.appendChild(btn);
      card.appendChild(note);
    }

    function makeMCQ(card, q) {
      var opts = el("div", "cy-qz__opts");
      var why = el("p", "cy-qz__why");
      var settled = false;
      (q.options || []).forEach(function (o) {
        var b = el("button", "cy-qz__opt", o[0]); b.type = "button";
        b.addEventListener("click", function () {
          if (settled) return;
          if (o[1]) {
            settled = true; b.classList.add("is-right");
            Array.prototype.forEach.call(opts.children, function (x) { x.disabled = true; });
            why.className = "cy-qz__why is-good"; why.textContent = o[2] || "Correct.";
            card.classList.add("is-good"); onCorrect();
          } else {
            b.classList.add("is-wrong"); b.disabled = true;
            why.className = "cy-qz__why is-bad"; why.textContent = o[2] || "Not quite. Try another.";
            nudge(card);
          }
        });
        opts.appendChild(b);
      });
      card.appendChild(opts); card.appendChild(why);
    }

    function makeTF(card, q) {
      var opts = el("div", "cy-qz__opts cy-qz__opts--tf");
      var why = el("p", "cy-qz__why");
      var settled = false;
      [["True", true], ["False", false]].forEach(function (pair) {
        var b = el("button", "cy-qz__opt", pair[0]); b.type = "button";
        b.addEventListener("click", function () {
          if (settled) return;
          if (pair[1] === !!q.answer) {
            settled = true; b.classList.add("is-right");
            Array.prototype.forEach.call(opts.children, function (x) { x.disabled = true; });
            why.className = "cy-qz__why is-good"; why.textContent = q.why || "Correct.";
            card.classList.add("is-good"); onCorrect();
          } else {
            b.classList.add("is-wrong"); b.disabled = true;
            why.className = "cy-qz__why is-bad"; why.textContent = q.why_wrong || q.why || "Not quite. Think it through and try the other.";
            nudge(card);
          }
        });
        opts.appendChild(b);
      });
      card.appendChild(opts); card.appendChild(why);
    }

    function makeFill(card, q) {
      var row = el("div", "cy-qz__fill");
      var input = document.createElement("input");
      input.type = "text"; input.className = "cy-qz__input";
      input.setAttribute("aria-label", "Your answer");
      if (q.placeholder) input.placeholder = q.placeholder;
      var b = el("button", "cy-btn cy-btn--primary cy-qz__check", "Check"); b.type = "button";
      var why = el("p", "cy-qz__why");
      var accept = [q.answer].concat(q.accept || []).map(norm);
      var settled = false;
      function grade() {
        if (settled) return;
        if (accept.indexOf(norm(input.value)) !== -1) {
          settled = true; input.disabled = true; b.disabled = true;
          input.classList.add("is-right");
          why.className = "cy-qz__why is-good"; why.textContent = q.why || ("Correct: " + q.answer + ".");
          card.classList.add("is-good"); onCorrect();
        } else {
          nudge(input);
          why.className = "cy-qz__why is-bad"; why.textContent = "Not quite. Check the spelling and try again.";
        }
      }
      b.addEventListener("click", grade);
      input.addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); grade(); } });
      row.appendChild(input); row.appendChild(b);
      card.appendChild(row); card.appendChild(why);
    }

    function makeMatch(card, q) {
      var pairs = q.pairs || [];
      var totalPairs = pairs.length, matched = 0;
      var sel = null;
      var why = el("p", "cy-qz__why");
      var grid = el("div", "cy-qz__match");
      var left = el("div", "cy-qz__col"), right = el("div", "cy-qz__col");

      function attempt(a, b) {
        if (a.i === b.i) {
          [a, b].forEach(function (x) { x.node.disabled = true; x.node.classList.remove("is-sel"); x.node.classList.add("is-matched"); });
          matched += 1; sel = null;
          if (matched === totalPairs) {
            why.className = "cy-qz__why is-good"; why.textContent = q.why || "All matched.";
            card.classList.add("is-good"); onCorrect();
          }
        } else {
          [a, b].forEach(function (x) { x.node.classList.add("is-wrong"); });
          (function (na, nb) { window.setTimeout(function () { na.classList.remove("is-wrong", "is-sel"); nb.classList.remove("is-wrong", "is-sel"); }, 450); })(a.node, b.node);
          sel = null;
          why.className = "cy-qz__why is-bad"; why.textContent = "Not a match. Try again.";
        }
      }
      function tap(col, i, node) {
        if (node.disabled) return;
        if (!sel) { sel = { col: col, i: i, node: node }; node.classList.add("is-sel"); return; }
        if (sel.node === node) { node.classList.remove("is-sel"); sel = null; return; }
        if (sel.col === col) { sel.node.classList.remove("is-sel"); sel = { col: col, i: i, node: node }; node.classList.add("is-sel"); return; }
        attempt(sel, { col: col, i: i, node: node });
      }
      pairs.forEach(function (p, idx) {
        var term = el("button", "cy-qz__term", p[0]); term.type = "button";
        term.addEventListener("click", function () { tap("L", idx, term); });
        left.appendChild(term);
      });
      var rights = pairs.map(function (p, i) { return { i: i, text: p[1] }; });
      for (var i = rights.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = rights[i]; rights[i] = rights[j]; rights[j] = t; }
      rights.forEach(function (r) {
        var def = el("button", "cy-qz__def", r.text); def.type = "button";
        def.addEventListener("click", function () { tap("R", r.i, def); });
        right.appendChild(def);
      });
      grid.appendChild(left); grid.appendChild(right);
      card.appendChild(grid); card.appendChild(why);
    }

    if (total === 0) { solved(root); return; }

    qs.forEach(function (q, idx) {
      var card = el("div", "cy-qz__card");
      var head = el("p", "cy-qz__q");
      head.appendChild(el("span", "cy-qz__n", String(idx + 1)));
      head.appendChild(el("span", "cy-qz__qtext", q.q || q.instruction || ""));
      card.appendChild(head);
      var type = (q.type || "mcq").toLowerCase();
      if (type === "truefalse" || type === "tf") makeTF(card, q);
      else if (type === "fill") makeFill(card, q);
      else if (type === "match") makeMatch(card, q);
      else makeMCQ(card, q);
      hintRow(card, q.hint);
      list.appendChild(card);
    });

    root.appendChild(counter);
    root.appendChild(list);
    root.appendChild(feedback);
    update();
  };

  // ------------------------------------------------------------ FIREWALL ----
  // Read an ordered firewall rule table (first match wins) and decide, for each
  // piece of traffic, whether it is Allowed or Blocked. A correct verdict flags
  // the rule that decided it. Solved when every item is judged correctly.
  CONTROLLERS.FIREWALL = function (root, cfg) {
    if (cfg.prompt) root.appendChild(el("p", "cy-act__prompt", cfg.prompt));

    // The rule table, kept on screen for reference above the traffic.
    var table = el("div", "cy-fwr");
    var head = el("div", "cy-fwr__row cy-fwr__row--head");
    head.appendChild(el("span", "cy-fwr__n", "#"));
    head.appendChild(el("span", "cy-fwr__act", "Action"));
    head.appendChild(el("span", "cy-fwr__desc", "Rule"));
    table.appendChild(head);
    cfg.rules.forEach(function (r) {
      var allow = r.action === "ALLOW";
      var row = el("div", "cy-fwr__row cy-fwr__row--" + (allow ? "allow" : "deny"));
      row.setAttribute("data-rule", r.n);
      row.appendChild(el("span", "cy-fwr__n", String(r.n)));
      row.appendChild(el("span", "cy-fwr__act", r.action));
      row.appendChild(el("span", "cy-fwr__desc", r.desc));
      table.appendChild(row);
    });
    root.appendChild(table);

    var total = cfg.traffic.length;
    var done = 0;
    var counter = el("p", "cy-classify__count");
    counter.setAttribute("aria-live", "polite");
    var feedback = el("p", "cy-act__feedback");
    feedback.setAttribute("aria-live", "polite");

    var list = el("div", "cy-fwq");
    cfg.traffic.forEach(function (item) {
      var card = el("div", "cy-fwq__item");
      card.appendChild(el("p", "cy-fwq__text", item.text));
      var opts = el("div", "cy-fwq__opts");
      var why = el("p", "cy-classify__why");
      var settled = false;

      [["ALLOW", "Allow"], ["BLOCK", "Block"]].forEach(function (pair) {
        var b = el("button", "cy-fwq__opt cy-fwq__opt--" + pair[0].toLowerCase(), pair[1]);
        b.type = "button";
        b.addEventListener("click", function () {
          if (settled) return;
          if (pair[0] === item.verdict) {
            settled = true;
            card.classList.add("is-correct");
            b.classList.add("is-right");
            var hit = table.querySelector('[data-rule="' + item.rule + '"]');
            if (hit) {
              hit.classList.add("is-hit");
              window.setTimeout(function () { hit.classList.remove("is-hit"); }, 1600);
            }
            why.className = "cy-classify__why is-good";
            why.textContent = item.why;
            Array.prototype.forEach.call(opts.children, function (o) { o.disabled = true; });
            done += 1;
            update();
            if (done === total) {
              feedback.className = "cy-act__feedback is-good";
              feedback.textContent = "Every packet judged correctly — you can read a rule set.";
              solved(root);
            }
          } else {
            b.classList.add("is-wrong");
            b.disabled = true;
            card.classList.add("is-shake");
            window.setTimeout(function () { card.classList.remove("is-shake"); }, 400);
            why.className = "cy-classify__why is-bad";
            why.textContent = "Not quite. Walk the rules from the top and stop at the first one that matches.";
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
    function update() { counter.textContent = done + " of " + total + " judged"; }
    update();
  };

  // ------------------------------------------------------------ TABLETOP ----
  // A staged incident-response exercise. A live situation board tracks the state
  // of the business (systems, data, the clock, notification) and updates as the
  // learner works the phases: detect, contain, eradicate, recover, review. A
  // poor call escalates the board but the exercise continues and teaches. Solved
  // once every stage has been worked through, ending in a short debrief.
  CONTROLLERS.TABLETOP = function (root, cfg) {
    if (cfg.prompt) root.appendChild(el("p", "cy-act__prompt", cfg.prompt));
    if (cfg.scenario) root.appendChild(el("p", "cy-tt__scenario", cfg.scenario));

    var board = el("div", "cy-board");
    board.setAttribute("aria-live", "polite");
    var cells = {};
    (cfg.board || []).forEach(function (ind) {
      var cell = el("div", "cy-board__cell is-" + (ind.state || "ok"));
      cell.appendChild(el("span", "cy-board__label", ind.label));
      var val = el("span", "cy-board__value", ind.value || "");
      cell.appendChild(val);
      cell.__value = val;
      cells[ind.id] = cell;
      board.appendChild(cell);
    });
    root.appendChild(board);

    var stageWrap = el("div", "cy-tt");
    var phase = el("p", "cy-tt__phase");
    var title = el("p", "cy-tt__title");
    var prompt = el("p", "cy-tt__prompt");
    prompt.setAttribute("aria-live", "polite");
    var choices = el("div", "cy-tt__choices");
    var feedback = el("p", "cy-act__feedback cy-tt__feedback");
    feedback.setAttribute("aria-live", "polite");
    stageWrap.appendChild(phase);
    stageWrap.appendChild(title);
    stageWrap.appendChild(prompt);
    stageWrap.appendChild(choices);
    stageWrap.appendChild(feedback);
    root.appendChild(stageWrap);

    var stages = cfg.stages || [];
    var idx = 0;
    var good = 0;

    function clear(node) { while (node.firstChild) node.removeChild(node.firstChild); }

    function applyBoard(set) {
      if (!set) return;
      Object.keys(set).forEach(function (id) {
        var cell = cells[id];
        if (!cell) return;
        var s = set[id];
        cell.className = "cy-board__cell is-" + (s.state || "ok") + " is-changed";
        if (s.value != null) cell.__value.textContent = s.value;
        window.setTimeout(function () { cell.classList.remove("is-changed"); }, 900);
      });
    }

    function renderStage() {
      if (idx >= stages.length) {
        phase.textContent = "Debrief";
        title.textContent = good === stages.length ? "Textbook response." : "Incident closed.";
        prompt.textContent = good === stages.length
          ? "You worked every phase the way the plan intends: detected fast, contained the spread, removed the cause, recovered cleanly, and met your obligations. That steadiness is what a rehearsed team looks like."
          : "You brought the incident to a close. Look back at any call that pushed the board into the red, and note which phase it belonged to. That review is itself the final phase of the lifecycle.";
        clear(choices);
        feedback.textContent = "";
        stageWrap.classList.add("is-complete");
        solved(root);
        return;
      }
      var st = stages[idx];
      phase.textContent = st.phase;
      title.textContent = st.title || "";
      prompt.textContent = st.prompt;
      clear(choices);
      feedback.textContent = "";
      feedback.className = "cy-act__feedback cy-tt__feedback";
      st.options.forEach(function (op) {
        var b = el("button", "cy-tt__choice", op.label);
        b.type = "button";
        b.addEventListener("click", function () { choose(st, op); });
        choices.appendChild(b);
      });
    }

    function choose(st, op) {
      Array.prototype.forEach.call(choices.children, function (b) { b.disabled = true; });
      if (op.outcome === "good") good += 1;
      applyBoard(op.board);
      feedback.className = "cy-act__feedback cy-tt__feedback is-" +
        (op.outcome === "good" ? "good" : "bad");
      feedback.textContent = op.consequence;
      var last = idx === stages.length - 1;
      var next = el("button", "cy-btn cy-btn--primary cy-tt__next",
        last ? "Close the incident" : "Next phase");
      next.type = "button";
      next.addEventListener("click", function () { idx += 1; renderStage(); });
      choices.appendChild(next);
    }

    renderStage();
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
