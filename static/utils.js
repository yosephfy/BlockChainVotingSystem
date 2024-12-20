/**
 * Updates the text content of an HTML element.
 * @param {string} id - The ID of the HTML element.
 * @param {string} text - The text to set as the element's content.
 */
export function updateElementText(id, text) {
  const element = document.getElementById(id);
  if (element) {
    element.textContent = text;
  }
}

/**
 * Makes an API request and returns the parsed response.
 * Handles Flask-style success and error responses properly.
 * @param {string} url - The API endpoint URL.
 * @param {object} [options={}] - Optional fetch options.
 * @returns {Promise<object>} - The parsed JSON response with success or error status.
 */
export async function fetchAPI(url, options = {}) {
  try {
    const response = await fetch(url, options);
    const responseData = await response.json(); // Parse JSON response
    return responseData;
  } catch (error) {
    console.error(`Error fetching from ${url}:`, error);
    return { error: "Failed to fetch data. Please try again later." };
  }
}

/**
 * Displays a non-popup alert message dynamically on the page.
 * @param {object} options - Configuration options for the alert.
 * @param {string} [options.message=""] - The success message to display.
 * @param {string} [options.error=""] - The error message to display.
 * @param {string} [options.status="info"] - The type of alert (e.g., "success", "error", "info").
 * @param {number} [options.timeout=3000] - How long (in ms) the alert should appear before disappearing.
 */
export function showAlert({
  message = "",
  error = "",
  status = "info",
  timeout = 3000,
}) {
  const alertContainer = document.createElement("div");
  alertContainer.className = `alert alert-${status}`;
  alertContainer.textContent = message || error;

  // Append to body or another container
  document.body.appendChild(alertContainer);

  // Automatically remove after timeout
  setTimeout(() => {
    alertContainer.remove();
  }, timeout);
}

/**
 * Destroys an existing Chart.js chart instance if it exists.
 * @param {object|null} chart - The Chart.js chart instance.
 */
export function destroyChart(chart) {
  if (chart) {
    chart.destroy();
  }
}

/**
 * Initializes a new Chart.js pie chart.
 * @param {object} ctx - The canvas context for the chart.
 * @param {Array<string>} labels - The labels for the chart.
 * @param {Array<number>} data - The data points for the chart.
 * @returns {object} - The initialized Chart.js chart instance.
 */
export function initializePieChart(ctx, labels, data) {
  return new Chart(ctx, {
    type: "pie",
    data: {
      labels,
      datasets: [
        {
          label: "Votes by Candidate",
          data,
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
        legend: { position: "top" },
      },
    },
  });
}
