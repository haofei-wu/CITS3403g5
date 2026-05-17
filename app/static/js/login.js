
function togglePassword() {
    const passwordInput = document.getElementById("password");
    const button = document.querySelector(".login-show-btn");

    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        button.textContent = "Hide";
    } else {
        passwordInput.type = "password";
        button.textContent = "Show";
    }
}

document.addEventListener("DOMContentLoaded", () => {

    const togglePassword =
        document.getElementById("toggle-password");

    const passwordInput =
        document.getElementById("password");

    if (togglePassword && passwordInput) {

        togglePassword.addEventListener("click", () => {

            if (passwordInput.type === "password") {

                passwordInput.type = "text";

                togglePassword.textContent = "🙈";
            }

            else {

                passwordInput.type = "password";

                togglePassword.textContent = "👁️";
            }
        });
    }
});
