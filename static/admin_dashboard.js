// Manage Election
document.getElementById("startElection").addEventListener("click", async () => {
  const response = await fetch("/admin/start-election");
  const result = await response.json();
  document.getElementById("electionStatus").textContent =
    result.message || result.error;
});

document.getElementById("endElection").addEventListener("click", async () => {
  const response = await fetch("/admin/end-election");
  const result = await response.json();
  document.getElementById("electionStatus").textContent =
    result.message || result.error;
});

// View Registered Voters
document.getElementById("viewVoters").addEventListener("click", async () => {
  const response = await fetch("/admin/voters");
  const voters = await response.json();
  const voterList = document.getElementById("voterList");
  voterList.innerHTML = ""; // Clear previous list
  voters.forEach((voter) => {
    const listItem = document.createElement("li");
    listItem.textContent = `Voter ID: ${voter.voter_id}, Voted: ${
      voter.voted ? "Yes" : "No"
    }`;
    voterList.appendChild(listItem);
  });
});

// Visualize Results
document
  .getElementById("viewStatistics")
  .addEventListener("click", async () => {
    const response = await fetch("/admin/statistics");
    const stats = await response.json();

    if (stats.results) {
      const labels = Object.keys(stats.results);
      const data = Object.values(stats.results);

      const ctx = document.getElementById("resultsChart").getContext("2d");

      new Chart(ctx, {
        type: "pie",
        data: {
          labels: labels,
          datasets: [
            {
              label: "Votes by Candidate",
              data: data,
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
            tooltip: {
              callbacks: {
                label: function (tooltipItem) {
                  const value = data[tooltipItem.dataIndex];
                  const total = data.reduce((acc, curr) => acc + curr, 0);
                  const percentage = ((value / total) * 100).toFixed(2);
                  return `${value} votes (${percentage}%)`;
                },
              },
            },
          },
        },
      });
    } else {
      alert("No statistics available to display.");
    }
  });

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
      result.message || result.error;
  });

// Audit Blockchain
document
  .getElementById("auditBlockchain")
  .addEventListener("click", async () => {
    const response = await fetch("/admin/audit");
    const result = await response.json();
    document.getElementById("auditResult").textContent =
      result.message || result.error;
  });

// Generate Random Votes
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
    document.getElementById("generateVotesStatus").textContent =
      result.message || result.error;
  });

async function fetchElectionStatus() {
  const response = await fetch("/admin/statistics");
  const data = await response.json();
  document.getElementById("electionStatus").textContent =
    data.election_status || "Unknown";
}

fetchElectionStatus();
