import { fetchAPI, showAlert } from "./utils.js";

document
  .getElementById("adminLoginForm")
  .addEventListener("submit", async (e) => {
    e.preventDefault();

    // Retrieve form inputs
    const username = document.getElementById("admin_username").value;
    const password = document.getElementById("admin_password").value;

    // Make API request for admin login
    const response = await fetchAPI("/admin-login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

    // Handle response
    if (!response.error) {
      showAlert({
        message: "Login successful! Redirecting...",
        type: "success",
      });
      window.location.href = "/admin-dashboard";
    } else {
      showAlert({ error: response.error || "Login failed!", type: "error" });
    }
  });
