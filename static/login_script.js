document.getElementById("login-form").addEventListener("submit", async function (e) {
    e.preventDefault();
    
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();
    const errorMessage = document.getElementById("error-message");
    
    errorMessage.textContent = ""; // Clear previous errors

    if (!email || !password) {
        errorMessage.textContent = "Please enter both email and password.";
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:5001/login", {  // Flask server runs on port 5001
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password }),
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem("userToken", data.token);  // Store JWT token securely
            window.location.href = "index.html";  // Redirect to home page after login
        } else {
            errorMessage.textContent = data.message || "Invalid login credentials.";
        }
    } catch (error) {
        console.error("Login Error:", error);
        errorMessage.textContent = "Unable to connect to the server. Try again later.";
    }
});
