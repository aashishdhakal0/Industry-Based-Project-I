/* Interactive lesson room, TryHackMe-style: a scrollable page of numbered,
 * collapsible task panels with a progress bar.
 *
 * A panel can hold more than one interactive: an optional mid-panel check, and
 * an end interactive (a check or an activity). Each is a "slot"; the panel
 * completes (ticks, banks its XP, fills the bar, opens the next) only when every
 * slot is satisfied. Without JS the panels render open, questions show as a
 * study page, and a "mark lesson complete" button banks the lesson.
 *
 * Served from static/ (script-src 'self'); CSRF read from the fallback form's
 * hidden input. activities.js fires cy:solved.
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

  // --- Task index rail: numbered tasks with live done/current status, and jump
  // to any task on click. Kept in sync with the panels below.
  var tasklistItems = {};
  Array.prototype.forEach.call(
    document.querySelectorAll("[data-tasklist-item]"),
    function (item) { tasklistItems[item.getAttribute("data-for")] = item; }
  );
  var tasklistDone = document.querySelector("[data-tasklist-done]");

  function panelById(id) {
    for (var i = 0; i < panels.length; i++) {
      if (panels[i].getAttribute("data-task-id") === id) return panels[i];
    }
    return null;
  }

  function isDone(p) { return p.getAttribute("data-done") === "1"; }

  function syncTasklist() {
    var currentSet = false;
    panels.forEach(function (p) {
      var item = tasklistItems[p.getAttribute("data-task-id")];
      if (!item) return;
      var done = isDone(p);
      var current = !done && !currentSet;
      if (current) currentSet = true;
      item.classList.toggle("is-done", done);
      item.classList.toggle("is-current", current);
    });
    if (tasklistDone) tasklistDone.textContent = doneCount();
  }

  Array.prototype.forEach.call(
    document.querySelectorAll("[data-task-jump]"),
    function (link) {
      link.addEventListener("click", function (e) {
        var panel = panelById(link.getAttribute("data-task-jump"));
        if (!panel) return;
        e.preventDefault();
        panel.open = true;
        var head = panel.querySelector(".cy-panel__head");
        if (head && head.scrollIntoView) head.scrollIntoView({ behavior: "smooth", block: "start" });
      });
    }
  );

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
    syncTasklist();
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
    var goBtn = document.getElementById("cy-reward-go");
    var nextLabel = room.getAttribute("data-next-label");
    if (goBtn && nextLabel) goBtn.textContent = nextLabel;
    if (goBtn) goBtn.onclick = function () { go(nextUrl); };
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

  function markPanelDone(panel) {
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

  // Each panel has one or more slots (check blocks, activities, a mark-complete).
  // The panel is done only when every slot is satisfied.
  function satisfySlot(panel) {
    if (isDone(panel)) return;
    panel.__slotsDone = (panel.__slotsDone || 0) + 1;
    if (panel.__slotsDone >= panel.__slotsTotal) markPanelDone(panel);
  }

  function wireCheckBlock(panel, block) {
    var checkBtn = block.querySelector("[data-check]");
    var feedback = block.querySelector("[data-feedback]");
    var hint = block.querySelector("[data-hint]");
    var toggle = block.querySelector("[data-hint-toggle]");
    if (toggle) toggle.addEventListener("click", function () {
      if (hint) hint.hidden = false;
      toggle.hidden = true;
    });
    if (!checkBtn) return;
    var solved = false;
    checkBtn.addEventListener("click", function () {
      if (solved) return;
      var opts = block.querySelectorAll("[data-opt]");
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
        solved = true;
        block.classList.add("is-solved");
        if (feedback) { feedback.className = "cy-act__feedback is-good"; feedback.textContent = "Correct."; }
        Array.prototype.forEach.call(opts, function (o) { var inp = o.querySelector("input"); if (inp) inp.disabled = true; });
        satisfySlot(panel);
      } else {
        if (feedback) { feedback.className = "cy-act__feedback is-bad"; feedback.textContent = "Not quite. Read the note, take the hint, and try again."; }
        if (hint) hint.hidden = false;
        if (toggle) toggle.hidden = true;
      }
    });
  }

  panels.forEach(function (panel) {
    var blocks = panel.querySelectorAll("[data-check-block]");
    var activities = panel.querySelectorAll("[data-activity]");
    var completes = panel.querySelectorAll("[data-complete]");
    panel.__slotsTotal = blocks.length + activities.length + completes.length;
    panel.__slotsDone = 0;
    Array.prototype.forEach.call(blocks, function (b) { wireCheckBlock(panel, b); });
    Array.prototype.forEach.call(completes, function (b) {
      b.addEventListener("click", function () { satisfySlot(panel); });
    });
    // activity slots complete via cy:solved (below)
  });

  room.addEventListener("cy:solved", function (e) {
    var panel = e.target;
    while (panel && panel !== room && !panel.hasAttribute("data-task")) panel = panel.parentNode;
    if (panel && panel !== room) satisfySlot(panel);
  });

  // Collapse all, open the first incomplete panel; hide the no-JS fallback while
  // there is still something to do (the celebration handles navigation).
  var open = firstOpen();
  panels.forEach(function (p, i) { p.open = (i === open); });
  if (nojs && open !== -1) nojs.hidden = true;
  updateProgress(null);
})();
