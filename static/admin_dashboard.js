import {
  updateElementText,
  fetchAPI,
  showAlert,
  destroyChart,
  initializePieChart,
} from "./utils.js";

let resultsChart = null;

async function fetchDashboardData() {
  try {
    // Fetch election statistics
    const statsResponse = await fetchAPI("/admin/statistics");
    if (statsResponse.error) throw new Error(statsResponse.error);

    const data = statsResponse.data || {};
    const { election_status = "Unknown", total_votes = 0, results = {} } = data;

    updateElementText("electionStatus", election_status);
    updateElementText("totalVotes", total_votes);

    const candidates = Object.keys(results);
    const votes = Object.values(results);

    const candidatesWithPercentages = candidates.map((candidate, index) => {
      const percentage =
        total_votes > 0 ? ((votes[index] / total_votes) * 100).toFixed(2) : 0;
      return `${candidate} (${percentage}%)`;
    });

    updateElementText(
      "candidatesList",
      candidatesWithPercentages.length > 0
        ? candidatesWithPercentages.join(", ")
        : "None"
    );

    // Fetch registered voters count
    const votersResponse = await fetchAPI("/admin/voters");
    if (votersResponse.error) throw new Error(votersResponse.error);

    updateElementText("registeredVoters", votersResponse.length || 0);

    // Update chart
    const ctx = document.getElementById("resultsChart").getContext("2d");
    destroyChart(resultsChart);
    resultsChart = initializePieChart(ctx, candidates, votes);

    // Fetch blockchain audit result
    const auditResponse = await fetchAPI("/admin/audit");
    updateElementText(
      "auditResult",
      auditResponse.message || "Audit unavailable"
    );
  } catch (error) {
    console.error("Error fetching dashboard data:", error);
  }
}

document.getElementById("startElection").addEventListener("click", async () => {
  const response = await fetchAPI("/admin/start-election");
  showAlert(response);
  fetchDashboardData();
});

document.getElementById("endElection").addEventListener("click", async () => {
  const response = await fetchAPI("/admin/end-election");
  showAlert(response);
  fetchDashboardData();
});

document
  .getElementById("refreshData")
  .addEventListener("click", fetchDashboardData);

document
  .getElementById("generateVotesForm")
  .addEventListener("submit", async (e) => {
    e.preventDefault();
    const numVotes = document.getElementById("numVotes").value;
    const response = await fetchAPI("/admin/generate-random-votes", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ numVotes }),
    });
    showAlert(response);
    fetchDashboardData();
  });

document
  .getElementById("resetVoteCount")
  .addEventListener("click", async () => {
    const response = await fetchAPI("/admin/reset-results");
    updateElementText("resetVoteStatus", response.message || response.error);
  });

document
  .getElementById("removeAllVoters")
  .addEventListener("click", async () => {
    const response = await fetchAPI("/admin/remove-voters", {
      method: "DELETE",
    });
    updateElementText("removeVotersStatus", response.message || response.error);
  });

// Initial data fetch
fetchDashboardData();
