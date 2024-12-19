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
let resultsChart = null;

document.getElementById("viewResults").addEventListener("click", async () => {
  try {
    const response = await fetch("/results");
    if (response.ok) {
      const results = await response.json();
      const candidates = Object.keys(results);
      const votes = Object.values(results);

      // Calculate percentages
      const totalVotes = votes.reduce((sum, count) => sum + count, 0);
      const percentages = votes.map((count) =>
        ((count / totalVotes) * 100).toFixed(2)
      );

      // Update Candidate Details
      const resultsContainer = document.getElementById("results");
      resultsContainer.innerHTML = ""; // Clear previous content
      candidates.forEach((candidate, index) => {
        const candidateInfo = document.createElement("p");
        candidateInfo.textContent = `${candidate}: ${votes[index]} votes (${percentages[index]}%)`;
        resultsContainer.appendChild(candidateInfo);
      });

      // Destroy the existing chart if it exists
      if (resultsChart) {
        resultsChart.destroy();
      }

      // Create a new chart
      const ctx = document.getElementById("resultsChart").getContext("2d");
      resultsChart = new Chart(ctx, {
        type: "pie",
        data: {
          labels: candidates,
          datasets: [
            {
              label: "Votes by Candidate",
              data: votes,
              backgroundColor: [
                "#FF6384",
                "#36A2EB",
                "#FFCE56",
                "#4BC0C0",
                "#9966FF",
                "#FF9F40",
              ],
              hoverOffset: 4,
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: "top",
            },
          },
        },
      });

      document.getElementById("resultMessage").textContent = ""; // Clear errors
    } else {
      const error = await response.json();
      document.getElementById("resultMessage").textContent = error.error;
    }
  } catch (error) {
    console.error("Error fetching results:", error);
    document.getElementById("resultMessage").textContent =
      "Failed to fetch results.";
  }
});

// Display election status dynamically
async function updateElectionStatus() {
  const response = await fetch("/admin/statistics");
  const stats = await response.json();
  document.getElementById("electionStatus").textContent = stats.election_status;
}
updateElectionStatus();
