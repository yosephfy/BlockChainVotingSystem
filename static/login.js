import { fetchAPI, showAlert } from "./utils.js";

document.getElementById("loginForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  // Retrieve form inputs
  const voter_id = document.getElementById("login_voter_id").value;
  const password = document.getElementById("login_password").value;

  // Make API request for login
  const response = await fetchAPI("/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ voter_id, password }),
  });

  // Handle response
  if (!response.error) {
    showAlert({ message: "Login successful! Redirecting...", type: "success" });
    window.location.href = "/voter-section";
  } else {
    showAlert({ error: response.error || "Login failed!", type: "error" });
  }
});
