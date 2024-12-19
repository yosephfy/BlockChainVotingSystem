document.getElementById("loginForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const voter_id = document.getElementById("login_voter_id").value;
  const password = document.getElementById("login_password").value;

  const response = await fetch("/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ voter_id, password }),
  });

  const result = await response.json();
  if (response.ok) {
    alert("Login successful!");
    window.location.href = "/voter-section";
  } else {
    alert(result.error || "Login failed!");
  }
});
