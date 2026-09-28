/* A playful frontend gate, not access control. Unlock state is never stored. */
(() => {
  "use strict";
  const form = document.getElementById("lock-form");
  const input = document.getElementById("lock-date");
  const error = document.getElementById("lock-error");
  const lock = document.getElementById("love-lock");
  const content = document.getElementById("site-content");

  input.addEventListener("input", () => {
    const original = input.value;
    const caret = input.selectionStart ?? original.length;
    const digitsBeforeCaret = original
      .slice(0, caret)
      .replace(/\D/g, "").length;
    const digits = original.replace(/\D/g, "").slice(0, 8);
    input.value = [digits.slice(0, 2), digits.slice(2, 4), digits.slice(4, 8)]
      .filter(Boolean)
      .join("/");
    // Keep editing in the middle of the date predictable, including Backspace.
    let position = 0;
    let seen = 0;
    while (position < input.value.length && seen < digitsBeforeCaret) {
      if (/\d/.test(input.value[position])) seen++;
      position++;
    }
    input.setSelectionRange(position, position);
    input.removeAttribute("aria-invalid");
    error.textContent = "";
  });

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    if (input.value !== "21/08/2026") {
      error.textContent = /^\d{2}\/\d{2}\/\d{4}$/.test(input.value)
        ? "Sai gòi bxa oi, nhớ lại nèooo"
        : "Em nhập đủ ngày, tháng và năm theo dạng xx/xx/xxxx nhé.";
      input.setAttribute("aria-invalid", "true");
      input.focus();
      return;
    }
    content.hidden = false;
    content.inert = false;
    lock.hidden = true;
    input.value = "";
    const heading = document.getElementById("hero-title");
    heading.setAttribute("tabindex", "-1");
    heading.focus({ preventScroll: true });
    window.scrollTo({ top: 0, behavior: "instant" });
  });
})();
