document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("scan-form");
  const button = document.getElementById("scan-btn");

  if (form && button) {
    form.addEventListener("submit", function () {
      // Disable the button and show spinner text
      button.disabled = true;
      button.innerHTML = `
        <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
        Scanning...
      `;
    });
  }
});
