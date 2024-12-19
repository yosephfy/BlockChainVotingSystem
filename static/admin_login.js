document
  .getElementById("adminLoginForm")
  .addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = document.getElementById("admin_username").value;
    const password = document.getElementById("admin_password").value;

    const response = await fetch("/admin-login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

    const result = await response.json();
    if (response.ok) {
      alert("Login successful!");
      window.location.href = "/admin-dashboard";
    } else {
      alert(result.error || "Login failed!");
    }
  });
