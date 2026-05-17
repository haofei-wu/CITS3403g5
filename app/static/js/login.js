
function togglePassword(inputId = "password", button) {
    const passwordInput = document.getElementById(inputId);
    const toggleButton = button || document.querySelector(".login-show-btn");

    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        toggleButton.textContent = "Hide";
    } else {
        passwordInput.type = "password";
        toggleButton.textContent = "Show";
    }
}
