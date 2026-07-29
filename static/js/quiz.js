/* Quiz stepper — progressive enhancement over a plain multi-question form.
 *
 * Without this file every question shows in one scrollable form and Submit
 * works. With it, questions become a one-at-a-time stepper with a progress bar,
 * and each answer is saved to the server as it's picked so a refresh mid-quiz
 * doesn't lose progress. No timer, by design.
 *
 * Served from static/ (script-src 'self'). The CSRF cookie is HttpOnly, so the
 * token is read from the form's hidden input and sent as the X-CSRFToken header.
 */
(function () {
  "use strict";

  var form = document.querySelector("[data-quiz]");
  if (!form) return;

  var questions = Array.prototype.slice.call(form.querySelectorAll("[data-quiz-q]"));
  if (!questions.length) return;

  var progress = form.querySelector("[data-quiz-progress]");
  var fill = form.querySelector("[data-quiz-fill]");
  var count = form.querySelector("[data-quiz-count]");
  var backBtn = form.querySelector("[data-quiz-back]");
  var nextBtn = form.querySelector("[data-quiz-next]");
  var submitBtn = form.querySelector("[data-quiz-submit]");
  var total = questions.length;
  var index = 0;

  var saveUrl = form.getAttribute("data-save-url");
  var tokenInput = form.querySelector("input[name=csrfmiddlewaretoken]");
  var token = tokenInput ? tokenInput.value : "";

  // Enter stepped mode: CSS hides all but the current question.
  form.classList.add("cy-quiz--stepped");
  if (progress) progress.hidden = false;
  if (backBtn) backBtn.hidden = false;
  if (nextBtn) nextBtn.hidden = false;

  function currentAnswered() {
    return !!questions[index].querySelector("input[type=radio]:checked");
  }

  function render() {
    for (var i = 0; i < questions.length; i++) {
      questions[i].classList.toggle("is-current", i === index);
    }
    var human = index + 1;
    if (fill) fill.style.width = (human / total) * 100 + "%";
    if (count) count.textContent = "Question " + human + " of " + total;

    if (backBtn) backBtn.disabled = index === 0;
    var last = index === total - 1;
    if (nextBtn) nextBtn.hidden = last;
    if (submitBtn) submitBtn.hidden = !last;
    // You must answer the current question before moving on.
    if (nextBtn) nextBtn.disabled = !currentAnswered();
    if (submitBtn && last) submitBtn.disabled = !currentAnswered();
  }

  function go(delta) {
    var next = index + delta;
    if (next < 0 || next >= total) return;
    index = next;
    render();
    var legend = questions[index].querySelector(".cy-quiz__q-text");
    if (legend && legend.scrollIntoView) legend.scrollIntoView({ block: "nearest" });
  }

  function save(questionId, answerId) {
    if (!saveUrl || !window.fetch) return;
    var body = new FormData();
    body.append("question", questionId);
    body.append("answer", answerId);
    fetch(saveUrl, {
      method: "POST",
      headers: { "X-CSRFToken": token, "X-Requested-With": "fetch" },
      body: body,
      credentials: "same-origin",
    }).catch(function () {
      /* Autosave is a convenience; the form submit is authoritative. */
    });
  }

  if (backBtn) backBtn.addEventListener("click", function () { go(-1); });
  if (nextBtn) nextBtn.addEventListener("click", function () { go(1); });

  form.addEventListener("change", function (e) {
    var input = e.target;
    if (!input || input.type !== "radio") return;
    var fieldset = input.closest("[data-quiz-q]");
    if (fieldset) save(fieldset.getAttribute("data-qid"), input.value);
    render();
  });

  render();
})();
