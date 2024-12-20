import { fetchAPI, showAlert } from "./utils.js";

document
  .getElementById("registerForm")
  .addEventListener("submit", async (e) => {
    e.preventDefault();

    // Get form inputs
    const voter_id = document.getElementById("register_voter_id").value;
    const password = document.getElementById("register_password").value;

    // API request to register voter
    const response = await fetchAPI("/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ voter_id, password }),
    });

    // Handle response
    if (!response.error) {
      showAlert({
        message: "Registration successful! Redirecting to login...",
        type: "success",
      });
      window.location.href = "/login";
    } else {
      showAlert({
        error: response.error || "Registration failed!",
        type: "error",
      });
    }
  });
