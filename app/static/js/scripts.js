// Bootstrap form validation script
document.addEventListener("DOMContentLoaded", function () {
    "use strict";

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

        // Optional: Real-time validation
        const inputs = form.querySelectorAll("input, textarea, select");
        Array.from(inputs).forEach((input) => {
            input.addEventListener("input", () => {
                input.setCustomValidity("");
                if (!input.checkValidity()) {
                    input.classList.add("is-invalid");
                } else {
                    input.classList.remove("is-invalid");
                }
            });
        });
    });
});
