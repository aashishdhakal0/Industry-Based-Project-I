/* Interactive lesson room — progressive enhancement over a readable study page.
 *
 * Without this file the lesson renders as a worked page (concepts, questions with
 * their answers and explanations shown) plus a "mark lesson complete" button.
 * With it, tasks become a one-at-a-time stepper: instant right/wrong feedback on
 * checks, points banked per task, an XP bar, and a celebration when the lesson
 * completes. Served from static/ (script-src 'self'); CSRF token read from the
 * form input (the cookie is HttpOnly).
 */
(function () {
  "use strict";

  var room = document.querySelector("[data-room]");
  if (!room) return;

  var tasks = Array.prototype.slice.call(room.querySelectorAll("[data-task]"));
  if (!tasks.length) return;

  var progress = room.querySelector("[data-room-progress]");
  var fill = room.querySelector("[data-room-fill]");
  var count = room.querySelector("[data-room-count]");
  var xpEl = room.querySelector("[data-room-xp]");
  var backBtn = room.querySelector("[data-room-back]");
  var primary = room.querySelector("[data-room-primary]");
  var completeBtn = room.querySelector("[data-room-complete]");

  var taskUrl = room.getAttribute("data-task-url");
  var nextUrl = room.getAttribute("data-next");
  var tokenInput = room.querySelector("input[name=csrfmiddlewaretoken]");
  var token = tokenInput ? tokenInput.value : "";
  var total = tasks.length;

  // Go live: CSS now hides the revealed answers and the no-JS button, and shows
  // the stepper chrome.
  room.classList.add("is-live");
  if (progress) progress.hidden = false;
  if (primary) primary.hidden = false;
  if (backBtn) backBtn.hidden = false;
  if (completeBtn) completeBtn.hidden = true;

  // Start on the first unfinished task.
  var index = 0;
  for (var i = 0; i < tasks.length; i++) {
    if (tasks[i].getAttribute("data-done") !== "1") { index = i; break; }
    index = i;
  }

  function isDone(el) { return el.getAttribute("data-done") === "1"; }
  function isLast(i) { return i === total - 1; }

  function setXp(value) { if (xpEl) xpEl.textContent = value; }

  function toast(points) {
    var t = document.createElement("div");
    t.className = "cy-room__toast";
    t.textContent = "+" + points + " XP";
    room.appendChild(t);
    // remove after the animation
    t.addEventListener("animationend", function () { t.remove(); });
  }

  function primaryLabel(el) {
    if (isDone(el)) return isLast(index) ? "Finish" : "Next";
    if (el.getAttribute("data-kind") === "CONCEPT") return "Got it";
    return "Continue";
  }

  function render() {
    for (var i = 0; i < tasks.length; i++) {
      tasks[i].classList.toggle("is-current", i === index);
    }
    var el = tasks[index];
    if (fill) fill.style.width = ((index + 1) / total) * 100 + "%";
    if (count) count.textContent = "Task " + (index + 1) + " of " + total;
    if (backBtn) backBtn.disabled = index === 0;

    if (primary) {
      primary.firstChild.nodeValue = primaryLabel(el) + " ";
      // A check/scenario must be answered correctly before Continue lights up.
      var needsAnswer = el.getAttribute("data-kind") !== "CONCEPT" && !isDone(el)
        && !el.getAttribute("data-solved");
      primary.disabled = needsAnswer;
    }
    var legend = el.querySelector(".cy-task__title") || el;
    if (legend.scrollIntoView) legend.scrollIntoView({ block: "nearest" });
  }

  function complete(el) {
    // Already recorded (revisiting): resolve without a round-trip.
    if (isDone(el)) return Promise.resolve(null);
    if (!taskUrl || !window.fetch) { el.setAttribute("data-done", "1"); return Promise.resolve(null); }
    var body = new FormData();
    body.append("task", el.getAttribute("data-task-id"));
    return fetch(taskUrl, {
      method: "POST",
      headers: { "X-CSRFToken": token, "X-Requested-With": "fetch" },
      body: body,
      credentials: "same-origin",
    }).then(function (r) { return r.json(); }).then(function (data) {
      el.setAttribute("data-done", "1");
      toast(parseInt(el.getAttribute("data-points"), 10) || 0);
      if (data) setXp(data.lesson_points_done);
      return data;
    }).catch(function () {
      el.setAttribute("data-done", "1");
      return null;
    });
  }

  function advanceOrFinish() {
    if (index < total - 1) { index += 1; render(); return; }
    go(nextUrl);
  }

  function onPrimary() {
    var el = tasks[index];
    if (isDone(el)) { advanceOrFinish(); return; }
    primary.disabled = true;
    complete(el).then(function (data) {
      if (data && data.lesson_completed && data.reward) {
        celebrate(data.reward, data.next_url);
      } else {
        advanceOrFinish();
      }
    });
  }

  // Instant feedback on a check/scenario option.
  function onOption(btn, task) {
    if (task.getAttribute("data-solved") === "1" || isDone(task)) return;
    var correct = btn.getAttribute("data-correct") === "1";
    btn.classList.add("is-revealed", correct ? "is-right" : "is-wrong");
    if (correct) {
      task.setAttribute("data-solved", "1");
      // reveal the correct one, lock the rest, and light up Continue
      Array.prototype.forEach.call(task.querySelectorAll(".cy-task__opt"), function (o) {
        o.classList.add("is-locked");
        if (o.getAttribute("data-correct") === "1") o.classList.add("is-revealed", "is-right");
      });
      if (primary) primary.disabled = false;
    }
  }

  function go(url) { if (url) window.location.href = url; }

  function celebrate(reward, url) {
    var overlay = document.getElementById("cy-reward");
    var dest = url || nextUrl;
    if (!overlay) return go(dest);
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
    var cont = document.getElementById("cy-reward-go");
    cont.onclick = function () { go(dest); };
  }

  if (primary) primary.addEventListener("click", onPrimary);
  if (backBtn) backBtn.addEventListener("click", function () {
    if (index > 0) { index -= 1; render(); }
  });

  // Interactive activities (activities.js) announce completion by firing
  // cy:solved on their task. Treat it exactly like a correct check answer:
  // mark the task solved so Continue lights up.
  room.addEventListener("cy:solved", function (e) {
    var task = e.target;
    while (task && task !== room && !task.hasAttribute("data-task")) task = task.parentNode;
    if (!task || task === room) return;
    task.setAttribute("data-solved", "1");
    if (task.classList.contains("is-current")) render();
  });

  tasks.forEach(function (task) {
    Array.prototype.forEach.call(task.querySelectorAll(".cy-task__opt"), function (btn) {
      btn.addEventListener("click", function () { onOption(btn, task); });
    });
  });

  // Tasks already done on load count as solved (so Continue is enabled).
  tasks.forEach(function (t) { if (isDone(t)) t.setAttribute("data-solved", "1"); });

  render();
})();
