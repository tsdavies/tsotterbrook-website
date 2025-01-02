document.addEventListener("DOMContentLoaded", function () {
  try {
    ("use strict");

    const forms = document.querySelectorAll(".needs-validation");

    Array.from(forms).forEach((form) => {
      form.addEventListener(
        "submit",
        (event) => {
          if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
          }
          form.classList.add("was-validated");
        },
        false
      );

      const inputs = form.querySelectorAll("input, textarea, select");
      Array.from(inputs).forEach((input) => {
        input.addEventListener("blur", () => {
          if (!input.checkValidity()) {
            input.classList.add("is-invalid");
          } else {
            input.classList.remove("is-invalid");
          }
        });
      });
    });

    if (typeof bootstrap !== "undefined" && bootstrap.Tooltip) {
      var tooltipTriggerList = [].slice.call(
        document.querySelectorAll('[data-bs-toggle="tooltip"]')
      );
      tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
      });
    } else {
      console.warn("Bootstrap Tooltip not found");
    }
  } catch (error) {
    console.error("Error in form validation script:", error);
  }
});
