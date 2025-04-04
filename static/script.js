document.getElementById('signup-form').addEventListener('submit', async function(e) {
    e.preventDefault();
  
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
    const errorMessage = document.getElementById('error-message');
  
    errorMessage.style.color = 'red';
  
    if (password !== confirmPassword) {
      errorMessage.innerText = "❌ Passwords do not match!";
      return;
    }
  
    try {
      const response = await fetch('http://127.0.0.1:5001/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });
  
      const result = await response.json();
  
      if (response.ok) {
        alert("✅ Registration successful! Redirecting to login...");
        window.location.href = "/static/login.html";
      } else {
        errorMessage.innerText = ❌ ${result.message};
      }
    } catch (error) {
      console.error("❌ Error during registration:", error);
      errorMessage.innerText = "❌ Could not connect to server.";
    }
  });
