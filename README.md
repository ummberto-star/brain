# Brainstorm Arena

Aplikacja webowa do burzy mózgów z 4 modelami przez OpenRouter:
- Grok
- Sonnet
- ChatGPT
- Qwen 3.5

## Czy mogę to odpalić lokalnie?
Tak — normalnie lokalnie na swoim komputerze.

## Gdzie wpisać API key OpenRouter?
Masz 2 opcje:

1. **Plik `.env`** (najwygodniej):
   - skopiuj plik przykładowy: `cp .env.example .env`
   - otwórz `.env` i wklej swój klucz po `OPENROUTER_API_KEY=`

2. **Zmienna środowiskowa** (tymczasowo):
   - Linux/macOS: `export OPENROUTER_API_KEY="twoj_klucz"`
   - Windows PowerShell: `$env:OPENROUTER_API_KEY="twoj_klucz"`

> Aplikacja najpierw czyta `.env`, a jeśli go nie ma — bierze wartość ze środowiska.

## Uruchomienie krok po kroku

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edytuj .env i wpisz swój klucz
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Następnie otwórz `http://localhost:8000`.

## Jak sprawdzić, czy działa?

### 1) Healthcheck
Po uruchomieniu serwera wejdź na:
- `http://localhost:8000/health`

Powinieneś dostać:
```json
{"status":"ok"}
```

### 2) Test z UI
- Otwórz `http://localhost:8000`
- Wpisz pomysł i (opcjonalnie) kontekst
- Kliknij **Uruchom panel ekspertów**
- Po 1–3 minutach zobaczysz:
  - Rundę 1 (propozycje)
  - Rundę 2 (krytyka i ulepszenia)
  - Plan finalny

## Uwagi
- Domyślne identyfikatory modeli są w `app.py` (`AGENTS`).
- Jeśli któryś model w OpenRouter okaże się niedostępny, zmień `model` w odpowiednim agencie.
