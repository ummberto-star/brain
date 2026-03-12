import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from starlette.requests import Request


OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def load_local_env(path: str = ".env") -> None:
    env_path = Path(path)
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


load_local_env()


@dataclass
class Agent:
    name: str
    model: str
    role_prompt: str


AGENTS = [
    Agent(
        name="Grok",
        model="x-ai/grok-3-mini-beta",
        role_prompt=(
            "Jesteś odważnym strategiem wzrostu. Szukasz asymetrycznych okazji, "
            "proponujesz eksperymenty o dużym potencjale i jasno wskazujesz ryzyka."
        ),
    ),
    Agent(
        name="Sonnet",
        model="anthropic/claude-3.7-sonnet",
        role_prompt=(
            "Jesteś analitycznym architektem planów. Tworzysz logiczne, etapowe strategie "
            "z KPI, budżetem, harmonogramem i zależnościami."
        ),
    ),
    Agent(
        name="ChatGPT",
        model="openai/gpt-4.1",
        role_prompt=(
            "Jesteś praktycznym konsultantem produktu i marketingu. Stawiasz na wykonalność, "
            "priorytetyzację i szybkie iteracje."
        ),
    ),
    Agent(
        name="Qwen 3.5",
        model="qwen/qwen3-235b-a22b",
        role_prompt=(
            "Jesteś specjalistą od optymalizacji i egzekucji. Szukasz usprawnień, "
            "eliminujesz słabe punkty i wzmacniasz ROI."
        ),
    ),
]


class BrainstormInput(BaseModel):
    idea: str = Field(min_length=10, description="Pomysł biznesowy lub marketingowy")
    context: str | None = Field(default=None, description="Dodatkowy kontekst")


class OpenRouterClient:
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def complete(self, *, model: str, system_prompt: str, user_prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload: dict[str, Any] = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.7,
        }
        async with httpx.AsyncClient(timeout=90) as client:
            response = await client.post(OPENROUTER_URL, headers=headers, json=payload)
        if response.status_code >= 400:
            details = response.text
            raise HTTPException(status_code=502, detail=f"OpenRouter error ({model}): {details}")
        data = response.json()
        choices = data.get("choices", [])
        if not choices:
            raise HTTPException(status_code=502, detail=f"Brak odpowiedzi od modelu: {model}")
        return choices[0]["message"]["content"].strip()


app = FastAPI(title="Brainstorm Arena")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request, "agents": AGENTS})


@app.post("/api/brainstorm")
async def brainstorm(payload: BrainstormInput) -> dict[str, Any]:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail=(
                "Brak OPENROUTER_API_KEY. Ustaw zmienną środowiskową albo dodaj ją do pliku .env."
            ),
        )

    client = OpenRouterClient(api_key)
    context_block = f"\nKontekst: {payload.context.strip()}" if payload.context else ""
    shared_task = (
        f"Pomysł użytkownika: {payload.idea.strip()}{context_block}\n\n"
        "Zadanie: Przygotuj konkretny plan działania. Odpowiedz po polsku, w sekcjach: "
        "1) Teza, 2) Plan 30/60/90 dni, 3) Kanały i taktyki, 4) KPI, 5) Ryzyka i mitigacje."
    )

    initial_outputs: list[dict[str, str]] = []
    for agent in AGENTS:
        initial = await client.complete(
            model=agent.model,
            system_prompt=agent.role_prompt,
            user_prompt=shared_task,
        )
        initial_outputs.append({"agent": agent.name, "model": agent.model, "response": initial})

    peer_context = "\n\n".join(
        [f"[{item['agent']} - {item['model']}]\n{item['response']}" for item in initial_outputs]
    )

    revised_outputs: list[dict[str, str]] = []
    for agent in AGENTS:
        debate_prompt = (
            f"Masz swój styl: {agent.role_prompt}\n\n"
            f"Oto propozycje całego panelu ekspertów:\n{peer_context}\n\n"
            "Zadanie: Skrytykuj słabe elementy pozostałych planów (krótko i konkretnie), "
            "następnie przedstaw ulepszoną wersję planu końcowego. "
            "Wyróżnij co przejmujesz od innych i co odrzucasz."
        )
        revised = await client.complete(
            model=agent.model,
            system_prompt="Jesteś członkiem panelu strategicznego, który debatuje i ulepsza plan.",
            user_prompt=debate_prompt,
        )
        revised_outputs.append({"agent": agent.name, "model": agent.model, "response": revised})

    revised_context = "\n\n".join(
        [f"[{item['agent']} - {item['model']}]\n{item['response']}" for item in revised_outputs]
    )

    synthesis_prompt = (
        "Jesteś moderatorem panelu 4 ekspertów. Twoim zadaniem jest stworzyć JEDEN najlepszy plan, "
        "łącząc najlepsze elementy i usuwając sprzeczności.\n\n"
        f"Pomysł użytkownika: {payload.idea.strip()}{context_block}\n\n"
        f"Runda po dyskusji:\n{revised_context}\n\n"
        "Odpowiedz po polsku i użyj formatu:\n"
        "- Streszczenie strategiczne (max 8 zdań)\n"
        "- Finalny plan 30/60/90 dni\n"
        "- Budżet i alokacja\n"
        "- KPI i kamienie milowe\n"
        "- Lista eksperymentów (min 8)\n"
        "- Główne ryzyka + plan awaryjny\n"
    )

    final_plan = await client.complete(
        model="openai/gpt-4.1",
        system_prompt="Jesteś bezstronnym moderatorem łączącym wyniki debaty ekspertów.",
        user_prompt=synthesis_prompt,
    )

    return {
        "initial_round": initial_outputs,
        "debate_round": revised_outputs,
        "final_plan": final_plan,
    }


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
