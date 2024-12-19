let resultsChart = null;

async function fetchDashboardData() {
  try {
    const response = await fetch("/admin/statistics");
    const data = await response.json();

    document.getElementById("electionStatus").textContent =
      data.election_status || "Unknown";

    document.getElementById("totalVotes").textContent = data.total_votes;

    const candidates = Object.keys(data.results);
    const votes = Object.values(data.results);
    const totalVotes = data.total_votes;

    // Calculate percentages and display them
    const candidatesWithPercentages = candidates.map((candidate, index) => {
      const percentage = ((votes[index] / totalVotes) * 100).toFixed(2);
      return `${candidate} (${percentage}%)`;
    });

    // Update the DOM with candidate names and percentages
    document.getElementById("candidatesList").textContent =
      candidatesWithPercentages.length > 0
        ? candidatesWithPercentages.join(", ")
        : "None";

    const voterResponse = await fetch("/admin/voters");
    const voters = await voterResponse.json();
    document.getElementById("registeredVoters").textContent = voters.length;

    if (resultsChart) {
      resultsChart.destroy();
    }

    const ctx = document.getElementById("resultsChart").getContext("2d");
    resultsChart = new Chart(ctx, {
      type: "pie",
      data: {
        labels: candidates,
        datasets: [
          {
            label: "Votes by Candidate",
            data: Object.values(data.results),
            backgroundColor: [
              "#FF6384",
              "#36A2EB",
              "#FFCE56",
              "#4BC0C0",
              "#9966FF",
              "#FF9F40",
            ],
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

    const auditResponse = await fetch("/admin/audit");
    const auditResult = await auditResponse.json();
    document.getElementById("auditResult").textContent =
      auditResult.message || "Audit unavailable";
  } catch (error) {
    console.error("Error fetching dashboard data:", error);
  }
}

document.getElementById("startElection").addEventListener("click", async () => {
  const response = await fetch("/admin/start-election");
  const result = await response.json();
  alert(result.message || result.error);
  fetchDashboardData();
});

document.getElementById("endElection").addEventListener("click", async () => {
  const response = await fetch("/admin/end-election");
  const result = await response.json();
  alert(result.message || result.error);
  fetchDashboardData();
});

document.getElementById("refreshData").addEventListener("click", () => {
  fetchDashboardData();
});

document
  .getElementById("generateVotesForm")
  .addEventListener("submit", async (e) => {
    e.preventDefault();
    const numVotes = document.getElementById("numVotes").value;
    const response = await fetch("/admin/generate-random-votes", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ numVotes }),
    });
    const result = await response.json();
    alert(result.message || result.error);
    fetchDashboardData();
  });

fetchDashboardData();

// Reset Vote Count
document
  .getElementById("resetVoteCount")
  .addEventListener("click", async () => {
    const response = await fetch("/admin/reset-results");
    const result = await response.json();
    document.getElementById("resetVoteStatus").textContent =
      result.message || result.error;
  });

// Remove All Voters
document
  .getElementById("removeAllVoters")
  .addEventListener("click", async () => {
    const response = await fetch("/admin/remove-voters", { method: "DELETE" });
    const result = await response.json();
    document.getElementById("removeVotersStatus").textContent =
      result.message || result.error || "";
  });
