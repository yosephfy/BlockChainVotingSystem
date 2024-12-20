import {
  fetchAPI,
  showAlert,
  updateElementText,
  destroyChart,
  initializePieChart,
} from "./utils.js";

let resultsChart = null;

// Handle Casting Vote
document.getElementById("voteForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const candidate = document.getElementById("candidate").value;

  const response = await fetchAPI("/cast-vote", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ candidate }),
  });
  showAlert(response);
});

// Handle Viewing Results
document.getElementById("viewResults").addEventListener("click", async () => {
  try {
    const response = await fetchAPI("/results");
    if (response.status === "error") {
      updateElementText("resultMessage", response.message);
      return;
    }

    const results = response.data;
    const candidates = Object.keys(results);
    const votes = Object.values(results);

    // Calculate percentages
    const totalVotes = votes.reduce((sum, count) => sum + count, 0);
    const percentages = votes.map((count) =>
      totalVotes > 0 ? ((count / totalVotes) * 100).toFixed(2) : 0
    );

    // Update Candidate Details
    const resultsContainer = document.getElementById("results");
    resultsContainer.innerHTML = ""; // Clear previous content
    candidates.forEach((candidate, index) => {
      const candidateInfo = document.createElement("p");
      candidateInfo.textContent = `${candidate}: ${votes[index]} votes (${percentages[index]}%)`;
      resultsContainer.appendChild(candidateInfo);
    });

    // Update chart
    const ctx = document.getElementById("resultsChart").getContext("2d");
    destroyChart(resultsChart);
    resultsChart = initializePieChart(ctx, candidates, votes);

    updateElementText("resultMessage", ""); // Clear errors
  } catch (error) {
    console.error("Error fetching results:", error);
    updateElementText("resultMessage", "Failed to fetch results.");
  }
});

// Display election status dynamically
async function updateElectionStatus() {
  const response = await fetchAPI("/admin/statistics");
  const status = response.data?.election_status || "Unknown";
  updateElementText("electionStatus", status);
}
updateElectionStatus();
