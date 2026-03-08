# Brainstorm Arena

Aplikacja webowa do burzy mózgów z 4 modelami przez OpenRouter:
- Grok
- Sonnet
- ChatGPT
- Qwen 3.5

## Jak to działa
1. Wpisujesz pomysł biznesowy/marketingowy.
2. 4 modele przygotowują niezależne propozycje.
3. Każdy model krytykuje i ulepsza plan po przeczytaniu odpowiedzi pozostałych.
4. Moderator tworzy jeden finalny plan.

## Uruchomienie

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export OPENROUTER_API_KEY="twoj_klucz"
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Następnie otwórz `http://localhost:8000`.

## Uwagi
- Domyślne identyfikatory modeli są w `app.py` (`AGENTS`).
- Jeśli któryś model w OpenRouter okaże się niedostępny, zmień `model` w odpowiednim agencie.
