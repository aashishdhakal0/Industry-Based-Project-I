/* Interactive lesson room, TryHackMe-style: a scrollable page of numbered,
 * collapsible task panels with a progress bar.
 *
 * Without this file the panels render open (native <details>), the questions show
 * their answers as a study page, and a "mark lesson complete" button banks the
 * lesson. With it: each panel collapses, a Check button grades the question, the
 * activity panels complete on doing, each completion ticks the header, pops a
 * "+N XP" toast, fills the progress bar, and the last one fires the celebration.
 *
 * Served from static/ (script-src 'self'); CSRF read from the fallback form's
 * hidden input (the cookie is HttpOnly). activities.js fires cy:solved.
 */
(function () {
  "use strict";

  var room = document.querySelector("[data-room]");
  if (!room) return;
  var panels = Array.prototype.slice.call(room.querySelectorAll("[data-task]"));
  if (!panels.length) return;

  var fill = room.querySelector("[data-room-fill]");
  var pct = room.querySelector("[data-room-pct]");
  var xpEl = room.querySelector("[data-room-xp]");
  var nojs = room.querySelector(".cy-room2__nojs");
  var taskUrl = room.getAttribute("data-task-url");
  var nextUrl = room.getAttribute("data-next");
  var tokenInput = room.querySelector("input[name=csrfmiddlewaretoken]");
  var token = tokenInput ? tokenInput.value : "";
  var total = panels.length;

  room.classList.add("is-live");

  function isDone(p) { return p.getAttribute("data-done") === "1"; }
  function firstOpen() {
    for (var i = 0; i < panels.length; i++) if (!isDone(panels[i])) return i;
    return -1;
  }
  function doneCount() {
    var n = 0;
    panels.forEach(function (p) { if (isDone(p)) n += 1; });
    return n;
  }

  function updateProgress(pointsDone) {
    var percent = Math.round(doneCount() / total * 100);
    if (fill) fill.style.width = percent + "%";
    if (pct) pct.textContent = "Progress " + percent + "%";
    if (xpEl && pointsDone != null) xpEl.textContent = pointsDone;
  }

  function toast(points) {
    var t = document.createElement("div");
    t.className = "cy-room__toast";
    t.textContent = "+" + points + " XP";
    document.body.appendChild(t);
    t.addEventListener("animationend", function () { t.remove(); });
  }

  function go(url) { if (url) window.location.href = url; }

  function celebrate(reward) {
    var overlay = document.getElementById("cy-reward");
    if (!overlay) return go(nextUrl);
    document.getElementById("cy-reward-points").textContent = "+" + (reward.points_gained || 0);
    var meta = document.getElementById("cy-reward-meta");
    if (meta) {
      var bits = [];
      if (reward.level) bits.push("Level " + reward.level);
      if (reward.streak) bits.push(reward.streak + "-day streak");
      meta.textContent = bits.join(" · ");
    }
    var wrap = document.getElementById("cy-reward-badges");
    if (wrap) {
      wrap.textContent = "";
      (reward.new_badges || []).forEach(function (b) {
        var chip = document.createElement("span");
        chip.className = "cy-reward__badge";
        chip.textContent = b.name;
        wrap.appendChild(chip);
      });
    }
    overlay.hidden = false;
    overlay.removeAttribute("aria-hidden");
    document.getElementById("cy-reward-go").onclick = function () { go(nextUrl); };
  }

  function openNextAfter(panel) {
    var i = panels.indexOf(panel);
    for (var j = i + 1; j < panels.length; j++) {
      if (!isDone(panels[j])) {
        panels[j].open = true;
        var head = panels[j].querySelector(".cy-panel__head");
        if (head && head.scrollIntoView) head.scrollIntoView({ block: "nearest" });
        return;
      }
    }
  }

  function markDone(panel) {
    if (isDone(panel)) return;
    panel.setAttribute("data-done", "1");
    panel.classList.add("is-done");
    toast(parseInt(panel.getAttribute("data-points"), 10) || 0);

    function advance(data) {
      updateProgress(data ? data.lesson_points_done : null);
      if (data && data.lesson_completed && data.reward) {
        celebrate(data.reward);
      } else {
        panel.open = false;
        openNextAfter(panel);
      }
    }

    if (taskUrl && window.fetch) {
      var body = new FormData();
      body.append("task", panel.getAttribute("data-task-id"));
      fetch(taskUrl, {
        method: "POST",
        headers: { "X-CSRFToken": token, "X-Requested-With": "fetch" },
        body: body,
        credentials: "same-origin",
      }).then(function (r) { return r.json(); }).then(advance).catch(function () { advance(null); });
    } else {
      advance(null);
    }
  }

  function wireHint(panel) {
    var hint = panel.querySelector("[data-hint]");
    var toggle = panel.querySelector("[data-hint-toggle]");
    if (toggle) toggle.addEventListener("click", function () {
      if (hint) hint.hidden = false;
      toggle.hidden = true;
    });
    return hint;
  }

  function wireCheck(panel) {
    var checkBtn = panel.querySelector("[data-check]");
    var feedback = panel.querySelector("[data-feedback]");
    var hint = wireHint(panel);
    var toggle = panel.querySelector("[data-hint-toggle]");
    if (!checkBtn) return;
    checkBtn.addEventListener("click", function () {
      if (isDone(panel)) return;
      var opts = panel.querySelectorAll("[data-opt]");
      var chosen = null;
      Array.prototype.forEach.call(opts, function (o) {
        var inp = o.querySelector("input");
        if (inp && inp.checked) chosen = o;
      });
      if (!chosen) {
        if (feedback) { feedback.className = "cy-act__feedback is-bad"; feedback.textContent = "Pick an answer first."; }
        return;
      }
      var correct = chosen.getAttribute("data-correct") === "1";
      chosen.classList.add("is-revealed", correct ? "is-right" : "is-wrong");
      if (correct) {
        if (feedback) { feedback.className = "cy-act__feedback is-good"; feedback.textContent = "Correct."; }
        Array.prototype.forEach.call(opts, function (o) { var inp = o.querySelector("input"); if (inp) inp.disabled = true; });
        markDone(panel);
      } else {
        if (feedback) { feedback.className = "cy-act__feedback is-bad"; feedback.textContent = "Not quite. Read the note, take the hint, and try again."; }
        if (hint) hint.hidden = false;
        if (toggle) toggle.hidden = true;
      }
    });
  }

  function wireConcept(panel) {
    var btn = panel.querySelector("[data-complete]");
    if (btn) btn.addEventListener("click", function () { markDone(panel); });
  }

  panels.forEach(function (panel) {
    var kind = panel.getAttribute("data-kind");
    if (kind === "CHECK" || kind === "SCENARIO") wireCheck(panel);
    else if (kind === "CONCEPT") wireConcept(panel);
    // activities complete via cy:solved
  });

  room.addEventListener("cy:solved", function (e) {
    var panel = e.target;
    while (panel && panel !== room && !panel.hasAttribute("data-task")) panel = panel.parentNode;
    if (panel && panel !== room) markDone(panel);
  });

  // Collapse all, open the first incomplete panel. Hide the no-JS fallback while
  // there is still something to do (the celebration handles navigation); leave it
  // visible as "Next lesson" when the whole lesson is already complete.
  var open = firstOpen();
  panels.forEach(function (p, i) { p.open = (i === open); });
  if (nojs && open !== -1) nojs.hidden = true;
  updateProgress(null);
})();
