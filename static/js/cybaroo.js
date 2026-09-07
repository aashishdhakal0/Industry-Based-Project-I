/* Cybaroo — the only JavaScript on the platform.
 *
 * Two small jobs, each in its own IIFE so one returning early can't disable the
 * other:
 *   1. the mobile nav toggle (runs on every page)
 *   2. the stats count-up on the home page (runs only where the stats are)
 *
 * WHY THIS IS JS AND ALMOST NOTHING ELSE IS
 * -----------------------------------------
 * Every other piece of motion here is CSS: reveals and parallax use
 * scroll-driven animations, progress bars use keyframes. A count-up nearly
 * works in CSS too — @property can animate an integer and counter() can print
 * it — except counter() cannot format "84,700". It would render "84700", and a
 * number that reads wrong is worse than a number that doesn't move.
 *
 * Our CSP is script-src 'self', so this file is served from static/ and no CDN
 * is involved.
 *
 * PROGRESSIVE ENHANCEMENT, AND WHY IT MATTERS HERE
 * ------------------------------------------------
 * The real, final, formatted figure is already in the HTML. This script only
 * ever *replaces* it with a zero and animates back to it. So:
 *
 *   - JS disabled or broken   -> the true number renders. Always.
 *   - prefers-reduced-motion  -> we don't touch it. The true number renders.
 *   - No IntersectionObserver -> we don't touch it. The true number renders.
 *
 * These are real ASD figures on a public page for a real client. The failure
 * mode of a fancier approach — markup holding "0" and JS filling it in — is a
 * page that tells visitors Australia had zero cybercrime reports. The number
 * lives in the HTML for that reason, not for tidiness.
 */
(function () {
  "use strict";

  var targets = document.querySelectorAll("[data-count-to]");
  if (!targets.length) return;

  // Someone who asked for less motion is not asking for a static zero.
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  if (!("IntersectionObserver" in window)) return;

  function format(el, value) {
    var prefix = el.getAttribute("data-count-prefix") || "";
    var suffix = el.getAttribute("data-count-suffix") || "";
    return prefix + value.toLocaleString("en-AU") + suffix;
  }

  function animate(el) {
    var target = parseInt(el.getAttribute("data-count-to"), 10);
    if (isNaN(target)) return;

    var duration = 1400;
    var started = null;

    function frame(now) {
      if (started === null) started = now;
      var progress = Math.min((now - started) / duration, 1);
      // Cubic ease-out: fast enough to feel responsive, settles rather than
      // stopping dead. Matches --cy-ease closely enough to belong.
      var eased = 1 - Math.pow(1 - progress, 3);
      el.textContent = format(el, Math.round(target * eased));
      if (progress < 1) {
        requestAnimationFrame(frame);
      } else {
        // Land on the exact figure, never on a rounding artefact.
        el.textContent = format(el, target);
      }
    }

    requestAnimationFrame(frame);
  }

  var observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        animate(entry.target);
        observer.unobserve(entry.target); // count up once, not on every scroll past
      });
    },
    { threshold: 0.45 }
  );

  Array.prototype.forEach.call(targets, function (el) {
    el.textContent = format(el, 0);
    observer.observe(el);
  });
})();


/* The mobile nav toggle.
 *
 * The button ships with a `hidden` attribute; we remove it here, so a visitor
 * without JS never sees a control that does nothing — they use the same links
 * in the footer. aria-expanded is kept in sync for screen readers, and the
 * menu closes on Escape and when focus leaves it, which is what a keyboard user
 * expects of a disclosure.
 */
(function () {
  "use strict";

  var toggle = document.querySelector(".cy-nav__toggle");
  var panel = document.getElementById("cy-nav-menu");
  if (!toggle || !panel) return;

  toggle.hidden = false;

  function setOpen(open) {
    panel.classList.toggle("is-open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
  }

  toggle.addEventListener("click", function () {
    setOpen(toggle.getAttribute("aria-expanded") !== "true");
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
      setOpen(false);
      toggle.focus();
    }
  });

  // Tapping outside the open menu closes it — the standard "click away" that
  // stops the dropdown lingering over the page.
  document.addEventListener("click", function (event) {
    if (
      toggle.getAttribute("aria-expanded") === "true" &&
      !panel.contains(event.target) &&
      !toggle.contains(event.target)
    ) {
      setOpen(false);
    }
  });
})();


/* Lesson "mark complete" — progressive enhancement.
 *
 * The form works without JS (POST -> record -> redirect to the next lesson with
 * a flash). Here we intercept it, POST via fetch, play the reward animation,
 * then advance. Same endpoint, same server logic; this just avoids the reload
 * and gives the moment some weight.
 */
(function () {
  "use strict";

  var form = document.querySelector(".cy-complete");
  if (!form) return;

  var overlay = document.getElementById("cy-reward");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function go(url) {
    window.location.href = url;
  }

  function celebrate(data) {
    if (!overlay) return go(data.next_url);

    document.getElementById("cy-reward-points").textContent =
      "+" + (data.points_gained || 0);

    var badgeWrap = document.getElementById("cy-reward-badges");
    badgeWrap.innerHTML = "";
    (data.new_badges || []).forEach(function (b) {
      var el = document.createElement("div");
      el.className = "cy-reward__badge";
      el.innerHTML =
        '<svg class="cy-i" aria-hidden="true"><use href="#' + b.icon + '"/></svg>' +
        "<span>" + b.name + "</span>";
      badgeWrap.appendChild(el);
    });

    overlay.hidden = false;
    overlay.removeAttribute("aria-hidden");

    var cont = document.getElementById("cy-reward-go");
    cont.textContent = data.next_label || (data.module_done ? "Back to module" : "Next lesson");
    cont.focus();
    cont.onclick = function () {
      go(data.next_url);
    };
  }

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    var token = form.querySelector("[name=csrfmiddlewaretoken]").value;

    fetch(form.action, {
      method: "POST",
      headers: { "X-Requested-With": "fetch", "X-CSRFToken": token },
    })
      .then(function (r) {
        return r.json();
      })
      .then(function (data) {
        // Nothing earned (already complete): just move on.
        if (!data.points_gained) return go(data.next_url);
        if (reduce) return celebrate(data); // overlay, no burst (CSS handles it)
        celebrate(data);
      })
      .catch(function () {
        // Network failed — fall back to a normal submit.
        form.submit();
      });
  });
})();


/* The interactive simulation.
 *
 * Reads the scenario from the json_script block and builds the exercise into
 * #cy-sim. Two kinds are supported:
 *   - "scenes": a visual, scene-by-scene branching simulation (Modules 1 and 2).
 *     Each scene has a backdrop illustration, a narrative, and choices; picking
 *     one reveals its consequence, then a Continue advances to the next scene.
 *   - "inbox": the older judge-each-message exercise (the Module 3 to 6
 *     placeholders still use this).
 * A score/total/path is posted to the server, which stores the SimulationResult
 * and returns the reward. All markup is built here from our own origin script,
 * so it stays under script-src 'self' with no inline handlers (CSP-safe).
 */
(function () {
  "use strict";

  var root = document.getElementById("cy-sim");
  var dataEl = document.getElementById("cy-sim-data");
  if (!root || !dataEl) return;

  var scenario;
  try {
    scenario = JSON.parse(dataEl.textContent);
  } catch (e) {
    return;
  }

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }
  function iconEl(id) {
    var s = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    s.setAttribute("class", "cy-i");
    s.setAttribute("aria-hidden", "true");
    var u = document.createElementNS("http://www.w3.org/2000/svg", "use");
    u.setAttribute("href", "#" + id);
    s.appendChild(u);
    return s;
  }
  function escapeHtml(s) {
    var d = document.createElement("div");
    d.textContent = s == null ? "" : String(s);
    return d.innerHTML;
  }
  function postResult(score, total, path) {
    fetch(root.getAttribute("data-complete-url"), {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": root.getAttribute("data-csrf"),
      },
      body: JSON.stringify({ score: score, total: total, path: path }),
    })
      .then(function (r) { return r.json(); })
      .then(function () { window.location.href = root.getAttribute("data-module-url"); })
      .catch(function () { window.location.href = root.getAttribute("data-module-url"); });
  }

  // The glyph shown on each scene's "screen", so it reads at a glance.
  var BACKDROP_ICON = {
    email: "i-mail", attach: "i-book", ransom: "i-lock", win: "i-award",
    desk: "i-mail", phone: "i-target", wifi: "i-eye", inbox: "i-mail",
    leak: "i-eye", loss: "i-flame",
  };

  // ---------------------------------------------------------- scenes -------
  function runScenes(scenario) {
    var scenes = scenario.scenes || {};
    var start = scenario.start;
    if (!start || !scenes[start]) return;

    // How many decision scenes exist, for the progress stepper and the score.
    var decisionIds = Object.keys(scenes).filter(function (k) {
      return (scenes[k].choices || []).length > 0;
    });
    var total = decisionIds.length;
    var score = 0, step = 0, path = [], current = null;

    var stage = el("div", "cy-sc");
    root.innerHTML = "";
    root.appendChild(stage);

    // Build a realistic, device-framed screen from a scene's `screen` spec,
    // reusing the .cy-scr device chrome. Supports a browser / window / phone
    // frame with generic rows, an email, or a device list as its content, so
    // the learner reads a genuine interface rather than an icon.
    function sceneScreen(s) {
      var art = el("div", "cy-scn__art cy-scn__art--real");
      art.setAttribute("aria-hidden", "true");
      var chrome = s.chrome || "browser";
      var scr = el("div", "cy-scr cy-scr--" + chrome);

      if (chrome === "browser") {
        var top = el("div", "cy-scr__chrome");
        var dots = el("span", "cy-scr__dots");
        dots.appendChild(el("i")); dots.appendChild(el("i")); dots.appendChild(el("i"));
        top.appendChild(dots);
        var tab = el("div", "cy-scr__tab");
        tab.appendChild(el("b")); tab.appendChild(el("span", null, s.tab || s.title || ""));
        top.appendChild(tab);
        scr.appendChild(top);
        var addr = el("div", "cy-scr__addr");
        addr.appendChild(el("span", "cy-scr__nav", "← →"));
        var url = el("div", "cy-scr__url" + (s.secure === false ? " cy-scr__url--insecure" : ""));
        var lock = el("span", "cy-scr__lock"); lock.appendChild(iconEl("i-lock")); url.appendChild(lock);
        if (s.secure === false) url.appendChild(el("span", "cy-scr__insecure", "Not secure"));
        url.appendChild(el("span", null, s.url || ""));
        addr.appendChild(url); scr.appendChild(addr);
      } else if (chrome === "window") {
        var top2 = el("div", "cy-scr__chrome");
        var ttl = el("span", "cy-scr__title");
        ttl.appendChild(iconEl(s.icon || "i-shield"));
        ttl.appendChild(el("span", null, " " + (s.title || "")));
        top2.appendChild(ttl);
        top2.appendChild(el("span", "cy-scr__winctl", "− □ ✕"));
        scr.appendChild(top2);
        if (s.menu) scr.appendChild(el("div", "cy-scr__menu", s.menu));
      } else if (chrome === "phone") {
        var stat = el("div", "cy-scr__status");
        stat.appendChild(el("span", null, s.time || "9:41"));
        stat.appendChild(el("span", "cy-scr__sig", "••••"));
        scr.appendChild(stat);
        if (s.app) scr.appendChild(el("div", "cy-scr__appbar", s.app));
      }

      var body = el("div", "cy-scr__body");
      if (s.rows) {
        var rl = el("div", "cy-simrows");
        s.rows.forEach(function (r) {
          var row = el("div", "cy-simrow");
          row.appendChild(el("span", "cy-simrow__k", r.k));
          row.appendChild(el("span", "cy-simrow__v" + (r.flag ? " is-" + r.flag : ""), r.v));
          rl.appendChild(row);
        });
        body.appendChild(rl);
      }
      if (s.email) {
        var m = s.email, mail = el("div", "cy-simmail");
        mail.appendChild(el("div", "cy-simmail__subj", m.subject || ""));
        var meta = el("div", "cy-simmail__meta");
        meta.appendChild(el("span", "cy-simmail__from", m.from || ""));
        if (m.date) meta.appendChild(el("span", "cy-simmail__date", m.date));
        mail.appendChild(meta);
        if (m.preview) mail.appendChild(el("p", "cy-simmail__body", m.preview));
        if (m.attachment) {
          var att = el("span", "cy-simmail__att" + (m.attachmentBad ? " is-bad" : ""));
          att.appendChild(iconEl(m.attachmentBad ? "i-close" : "i-book"));
          att.appendChild(el("span", null, " " + m.attachment));
          mail.appendChild(att);
        }
        body.appendChild(mail);
      }
      if (s.items) {
        var il = el("div", "cy-simitems");
        s.items.forEach(function (it) {
          var row = el("div", "cy-simitem" + (it.flag ? " is-" + it.flag : ""));
          var meta2 = el("span", "cy-simitem__meta");
          meta2.appendChild(el("span", "cy-simitem__name", it.name));
          if (it.sub) meta2.appendChild(el("span", "cy-simitem__sub", it.sub));
          row.appendChild(meta2);
          if (it.tag) row.appendChild(el("span", "cy-simitem__tag", it.tag));
          il.appendChild(row);
        });
        body.appendChild(il);
      }
      scr.appendChild(body);
      art.appendChild(scr);
      return art;
    }

    function render(id) {
      var sc = scenes[id];
      if (!sc) return;
      current = id;
      var isDecision = (sc.choices || []).length > 0;
      if (isDecision) step += 1;
      stage.innerHTML = "";

      if (total) {
        var prog = el("div", "cy-sc__prog");
        for (var i = 1; i <= total; i++) {
          var cls = "cy-sc__dot" + (i < step ? " is-done" : i === step ? " is-current" : "");
          prog.appendChild(el("span", cls));
        }
        stage.appendChild(prog);
      }

      // The scene uses a UNIQUE class namespace (cy-scn), NOT cy-scene, which is
      // the landing-page hero animation and would stack these children into one
      // overlapping grid cell.
      var scene = el("div", "cy-scn cy-scn--" + (sc.backdrop || "email"));
      var art;
      if (sc.screen) {
        // A realistic, device-framed screen the learner must READ to decide.
        art = sceneScreen(sc.screen);
      } else {
        art = el("div", "cy-scn__art");
        art.setAttribute("aria-hidden", "true");
        var screen = el("div", "cy-scn__screen");
        var bar = el("div", "cy-scn__bar");
        bar.appendChild(el("span", "cy-scn__dots"));
        screen.appendChild(bar);
        var glass = el("div", "cy-scn__glass");
        var emblem = iconEl(BACKDROP_ICON[sc.backdrop] || "i-shield");
        emblem.setAttribute("class", "cy-i cy-scn__emblem");
        glass.appendChild(emblem);
        screen.appendChild(glass);
        art.appendChild(screen);
      }
      scene.appendChild(art);
      var body = el("div", "cy-scn__body");
      if (isDecision) body.appendChild(el("span", "cy-scn__step", "Scene " + step + " of " + total));
      if (sc.title) body.appendChild(el("h2", "cy-scn__title", sc.title));
      if (sc.narrative) body.appendChild(el("p", "cy-scn__narrative", sc.narrative));
      scene.appendChild(body);
      stage.appendChild(scene);

      if (!isDecision) {
        var band = score === total ? "good" : score >= Math.ceil(total / 2) ? "ok" : "bad";
        var outcome = el("div", "cy-sc__outcome cy-sc__outcome--" + band);
        outcome.appendChild(iconEl(band === "good" ? "i-award" : band === "ok" ? "i-check-circle" : "i-target"));
        outcome.appendChild(el("p", "cy-sc__score", "You made the sound call on " + score + " of " + total + "."));
        var done = el("button", "cy-btn cy-btn--primary cy-btn--lg", "Back to the module");
        done.type = "button";
        done.addEventListener("click", function () { done.disabled = true; postResult(score, total, path); });
        outcome.appendChild(done);
        stage.appendChild(outcome);
        return;
      }

      var choices = el("div", "cy-sc__choices");
      sc.choices.forEach(function (ch) {
        var b = el("button", "cy-sc__choice", ch.label);
        b.type = "button";
        b.addEventListener("click", function () { choose(sc, ch, choices, b); });
        choices.appendChild(b);
      });
      stage.appendChild(choices);
    }

    function choose(sc, ch, wrap, btn) {
      Array.prototype.forEach.call(wrap.children, function (b) { b.disabled = true; });
      btn.classList.add("is-chosen", "is-" + ch.outcome);
      if (ch.outcome === "good") score += 1;
      path.push({ scene: current, outcome: ch.outcome });

      var cons = el("div", "cy-sc__consequence cy-sc__consequence--" + ch.outcome);
      var head = el("div", "cy-sc__consequence-head");
      head.appendChild(iconEl(ch.outcome === "good" ? "i-check-circle" : ch.outcome === "bad" ? "i-close" : "i-star"));
      head.appendChild(el("span", "cy-sc__consequence-label",
        ch.outcome === "good" ? "Sound call" : ch.outcome === "bad" ? "That backfires" : "It depends"));
      cons.appendChild(head);
      cons.appendChild(el("p", "cy-sc__consequence-text", ch.consequence || ""));
      var next = el("button", "cy-btn cy-btn--primary cy-sc__next",
        scenes[ch.to] && !(scenes[ch.to].choices || []).length ? "See how it went" : "Continue");
      next.type = "button";
      next.addEventListener("click", function () { render(ch.to); });
      cons.appendChild(next);
      stage.appendChild(cons);
    }

    render(start);
  }

  // ---------------------------------------------------------- inbox --------
  function runInbox(scenario) {
    var items = (scenario && scenario.items) || [];
    if (!items.length) return;
    var path = [], judged = 0, score = 0;

    function makeCard(item) {
      var card = document.createElement("div");
      card.className = "cy-sim-mail";
      card.innerHTML =
        '<div class="cy-sim-mail__head">' +
        '<span class="cy-sim-mail__from">' + escapeHtml(item.from) + "</span>" +
        "</div>" +
        '<div class="cy-sim-mail__subject">' + escapeHtml(item.subject) + "</div>" +
        '<p class="cy-sim-mail__preview">' + escapeHtml(item.preview) + "</p>" +
        '<div class="cy-sim-mail__actions">' +
        '<button type="button" class="cy-btn cy-btn--ghost" data-choice="safe">This is safe</button>' +
        '<button type="button" class="cy-btn cy-btn--ghost" data-choice="scam">This is a scam</button>' +
        "</div>" +
        '<div class="cy-sim-mail__verdict" hidden></div>';

      var verdict = card.querySelector(".cy-sim-mail__verdict");
      var actions = card.querySelector(".cy-sim-mail__actions");

      actions.querySelectorAll("button").forEach(function (btn) {
        btn.addEventListener("click", function () {
          var said = btn.getAttribute("data-choice");
          var correct = (said === "scam") === !!item.scam;
          if (correct) score++;
          judged++;
          path.push({ id: item.id, said: said, correct: correct });
          actions.querySelectorAll("button").forEach(function (b) { b.disabled = true; });
          btn.classList.add("is-chosen");
          card.classList.add(correct ? "is-correct" : "is-wrong");
          var tells = (item.tells || []).map(function (t) { return "<li>" + escapeHtml(t) + "</li>"; }).join("");
          verdict.innerHTML =
            '<div class="cy-sim-mail__result">' +
            '<svg class="cy-i" aria-hidden="true"><use href="#' + (correct ? "i-check-circle" : "i-close") + '"/></svg>' +
            "<span>" + (correct ? "Correct — " : "Not quite — ") +
            (item.scam ? "this one is a scam." : "this one is safe.") + "</span></div>" +
            (tells ? "<ul>" + tells + "</ul>" : "");
          verdict.hidden = false;
          if (judged === items.length) showFinish();
        });
      });
      return card;
    }

    function showFinish() {
      var finish = document.createElement("div");
      finish.className = "cy-sim-finish";
      finish.innerHTML =
        '<p class="cy-sim-finish__score">You spotted <strong>' + score + " of " + items.length +
        "</strong> correctly.</p>" +
        '<button type="button" class="cy-btn cy-btn--primary" id="cy-sim-finish-btn">Finish</button>';
      root.appendChild(finish);
      document.getElementById("cy-sim-finish-btn").addEventListener("click", function () {
        this.disabled = true;
        postResult(score, items.length, path);
      });
    }

    var list = document.createElement("div");
    list.className = "cy-sim-list";
    items.forEach(function (item) { list.appendChild(makeCard(item)); });
    root.innerHTML = "";
    root.appendChild(list);
  }

  if (scenario && scenario.kind === "scenes") {
    runScenes(scenario);
  } else {
    runInbox(scenario);
  }
})();


/* The app sidebar drawer (mobile).
 *
 * On desktop the sidebar is always visible and this does nothing. Below the
 * breakpoint the appbar hamburger toggles the drawer + a backdrop, with
 * aria-expanded kept in sync, Escape to close, and a tap on the backdrop to
 * dismiss — what a drawer is expected to do.
 */
(function () {
  "use strict";

  var toggle = document.querySelector(".cy-appbar__toggle");
  var side = document.getElementById("cy-side");
  var backdrop = document.getElementById("cy-side-backdrop");
  if (!toggle || !side || !backdrop) return;

  function setOpen(open) {
    side.classList.toggle("is-open", open);
    backdrop.classList.toggle("is-open", open);
    backdrop.hidden = !open;
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    document.body.style.overflow = open ? "hidden" : "";
  }

  toggle.addEventListener("click", function () {
    setOpen(toggle.getAttribute("aria-expanded") !== "true");
  });
  backdrop.addEventListener("click", function () {
    setOpen(false);
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
      setOpen(false);
      toggle.focus();
    }
  });
})();


/* Show/hide password.
 *
 * Every password field on the platform (login, registration, both reset
 * forms) renders the same markup: the input wrapped in a
 * `.cy-field-control`, with a `<button type="button" data-password-toggle>`
 * pointed at it via `aria-controls`. type="button" is load-bearing — a
 * checkbox or a bare button without it would submit the form.
 *
 * A real <button> is used rather than a styled <span> or <div> specifically
 * so Enter and Space work for free: the browser gives a <button> both,
 * keyboard focus, and its place in the tab order without us wiring any of
 * that up ourselves.
 *
 * State lives only in the DOM (the input's `type` and the button's
 * aria-pressed/aria-label) and is never written to storage, so every page
 * load starts hidden — there is nothing to reset.
 */
(function () {
  "use strict";

  var toggles = document.querySelectorAll("[data-password-toggle]");
  if (!toggles.length) return;

  Array.prototype.forEach.call(toggles, function (btn) {
    var input = document.getElementById(btn.getAttribute("aria-controls"));
    var use = btn.querySelector("use");
    if (!input || !use) return;

    btn.addEventListener("click", function () {
      var shown = input.type === "text";
      input.type = shown ? "password" : "text";
      btn.setAttribute("aria-pressed", shown ? "false" : "true");
      btn.setAttribute("aria-label", shown ? "Show password" : "Hide password");
      use.setAttribute("href", shown ? "#i-eye" : "#i-eye-off");
    });
  });
})();
