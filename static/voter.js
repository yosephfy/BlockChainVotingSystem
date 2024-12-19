// Handle Casting Vote
document.getElementById("voteForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const candidate = document.getElementById("candidate").value;

  const response = await fetch("/cast-vote", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ candidate }),
  });

  const result = await response.json();
  alert(result.message || result.error);
});

// Handle Viewing Results
document.getElementById("viewResults").addEventListener("click", async () => {
  const response = await fetch("/results");
  if (response.ok) {
    const results = await response.json();
    document.getElementById("results").textContent = JSON.stringify(
      results,
      null,
      2
    );
    document.getElementById("resultMessage").textContent = ""; // Clear any error
  } else {
    const error = await response.json();
    document.getElementById("resultMessage").textContent = error.error;
    document.getElementById("results").textContent = ""; // Clear previous results
  }
});

// Display election status dynamically
async function updateElectionStatus() {
  const response = await fetch("/admin/statistics");
  const stats = await response.json();
  document.getElementById("electionStatus").textContent = stats.election_status;
}
updateElectionStatus();
