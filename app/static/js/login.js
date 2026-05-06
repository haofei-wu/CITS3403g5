
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
