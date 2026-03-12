const form = document.getElementById("brainstorm-form");
const submitBtn = document.getElementById("submit-btn");
const statusEl = document.getElementById("status");
const resultsEl = document.getElementById("results");
const initialEl = document.getElementById("initial");
const debateEl = document.getElementById("debate");
const finalEl = document.getElementById("final");

function setStatus(message, variant = "idle") {
  statusEl.textContent = message;
  statusEl.classList.remove("status--running", "status--error");
  if (variant === "running") {
    statusEl.classList.add("status--running");
  }
  if (variant === "error") {
    statusEl.classList.add("status--error");
  }
}

function renderCards(target, items) {
  target.innerHTML = "";
  items.forEach((item) => {
    const article = document.createElement("article");
    article.className = "card result-card";

    const heading = document.createElement("h3");
    heading.textContent = `${item.agent} (${item.model})`;

    const content = document.createElement("div");
    content.textContent = item.response;

    article.appendChild(heading);
    article.appendChild(content);
    target.appendChild(article);
  });
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const idea = document.getElementById("idea").value.trim();
  const context = document.getElementById("context").value.trim();

  submitBtn.disabled = true;
  setStatus("Trwa burza mózgów... To może potrwać 1–3 minuty.", "running");
  resultsEl.classList.add("hidden");

  try {
    const response = await fetch("/api/brainstorm", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ idea, context: context || null }),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || "Nieznany błąd serwera");
    }

    renderCards(initialEl, data.initial_round);
    renderCards(debateEl, data.debate_round);
    finalEl.textContent = data.final_plan;

    resultsEl.classList.remove("hidden");
    setStatus("Gotowe ✅ Plan został wygenerowany.");
  } catch (error) {
    setStatus(`Błąd: ${error.message}`, "error");
  } finally {
    submitBtn.disabled = false;
  }
});
