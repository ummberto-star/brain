# Brainstorm Arena

Aplikacja webowa do burzy mózgów z 4 modelami przez OpenRouter:
- Grok
- Sonnet
- ChatGPT
- Qwen 3.5

## 0) Co musisz pobrać

### Wymagane
1. **Python 3.11+**
2. **Git**
3. Konto i klucz API z **OpenRouter**

### Szybkie sprawdzenie po instalacji
```bash
python --version
git --version
```

---

## 1) Pobranie projektu

```bash
git clone <TU_WKLEJ_URL_REPO>
cd brain
```

> Jeśli masz już folder z projektem, pomiń `git clone` i wejdź do katalogu `brain`.

---

## 2) Utworzenie środowiska Python

### Linux / macOS
```bash
python -m venv .venv
source .venv/bin/activate
```

### Windows (PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

---

## 3) Instalacja zależności

```bash
pip install -r requirements.txt
```

---

## 4) Gdzie wpisać API key OpenRouter

Najprościej przez plik `.env`:

```bash
cp .env.example .env
```

Potem edytuj `.env` i wklej swój klucz:

```env
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxx
```

Możesz też użyć zmiennej środowiskowej:
- Linux/macOS: `export OPENROUTER_API_KEY="twoj_klucz"`
- Windows PowerShell: `$env:OPENROUTER_API_KEY="twoj_klucz"`

---

## 5) Uruchomienie lokalne

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Otwórz w przeglądarce:
- `http://localhost:8000`

---

## 6) Jak sprawdzić czy działa

### Healthcheck
Otwórz:
- `http://localhost:8000/health`

Powinien być JSON:
```json
{"status":"ok"}
```

### Test UI
1. Wejdź na `http://localhost:8000`
2. Wpisz pomysł + kontekst
3. Kliknij **Uruchom debatę ekspertów**
4. Poczekaj 1–3 minuty na wynik

---

## 7) Co zobaczysz w aplikacji
- **Runda 1**: 4 niezależne propozycje modeli
- **Runda 2**: krytyka i ulepszenia między modelami
- **Finalna synteza**: jeden najlepszy plan

## Uwagi
- Konfiguracja modeli jest w `app.py` w sekcji `AGENTS`.
- Jeśli model jest niedostępny na OpenRouter, podmień `model` na inny dostępny identyfikator.
