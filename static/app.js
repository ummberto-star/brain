const form = document.getElementById("brainstorm-form");
const statusEl = document.getElementById("status");
const resultsEl = document.getElementById("results");
const initialEl = document.getElementById("initial");
const debateEl = document.getElementById("debate");
const finalEl = document.getElementById("final");

function renderCards(target, items) {
  target.innerHTML = "";
  items.forEach((item) => {
    const article = document.createElement("article");
    article.className = "card";
    article.textContent = `${item.agent} (${item.model})\n\n${item.response}`;
    target.appendChild(article);
  });
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const idea = document.getElementById("idea").value.trim();
  const context = document.getElementById("context").value.trim();

  statusEl.textContent = "Trwa burza mózgów... To może potrwać 1-3 minuty.";
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
    statusEl.textContent = "Gotowe ✅";
  } catch (error) {
    statusEl.textContent = `Błąd: ${error.message}`;
  }
});
