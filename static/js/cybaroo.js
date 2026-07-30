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


/* The interactive simulation: a phishing inbox.
 *
 * Reads the scenario from the json_script block and builds the exercise into
 * #cy-sim. Judge each message safe or scam, see why, then a score is posted to
 * the server (which stores the SimulationResult and returns the reward).
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
  var items = (scenario && scenario.items) || [];
  if (!items.length) return;

  var path = [];
  var judged = 0;
  var score = 0;

  function icon(id) {
    return '<svg class="cy-i" aria-hidden="true"><use href="#' + id + '"/></svg>';
  }

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
        var saidScam = said === "scam";
        var correct = saidScam === !!item.scam;
        if (correct) score++;
        judged++;
        path.push({ id: item.id, said: said, correct: correct });

        actions.querySelectorAll("button").forEach(function (b) {
          b.disabled = true;
        });
        btn.classList.add("is-chosen");

        card.classList.add(correct ? "is-correct" : "is-wrong");
        var tells = (item.tells || [])
          .map(function (t) {
            return "<li>" + escapeHtml(t) + "</li>";
          })
          .join("");
        verdict.innerHTML =
          '<div class="cy-sim-mail__result">' +
          icon(correct ? "i-check-circle" : "i-close") +
          "<span>" +
          (correct ? "Correct — " : "Not quite — ") +
          (item.scam ? "this one is a scam." : "this one is safe.") +
          "</span></div>" +
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
      '<p class="cy-sim-finish__score">You spotted <strong>' +
      score +
      " of " +
      items.length +
      "</strong> correctly.</p>" +
      '<button type="button" class="cy-btn cy-btn--primary" id="cy-sim-finish-btn">Finish</button>';
    root.appendChild(finish);

    document.getElementById("cy-sim-finish-btn").addEventListener("click", function () {
      var btn = this;
      btn.disabled = true;
      fetch(root.getAttribute("data-complete-url"), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": root.getAttribute("data-csrf"),
        },
        body: JSON.stringify({ score: score, total: items.length, path: path }),
      })
        .then(function (r) {
          return r.json();
        })
        .then(function () {
          window.location.href = root.getAttribute("data-module-url");
        })
        .catch(function () {
          window.location.href = root.getAttribute("data-module-url");
        });
    });
  }

  function escapeHtml(s) {
    var d = document.createElement("div");
    d.textContent = s == null ? "" : String(s);
    return d.innerHTML;
  }

  var list = document.createElement("div");
  list.className = "cy-sim-list";
  items.forEach(function (item) {
    list.appendChild(makeCard(item));
  });
  root.innerHTML = "";
  root.appendChild(list);
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
