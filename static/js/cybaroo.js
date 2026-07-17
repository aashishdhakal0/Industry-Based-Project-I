/* Cybaroo — the only JavaScript on the platform.
 *
 * It animates the stats on the home page counting up as they scroll into view.
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
