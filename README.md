# O-ja! Chatbot-Kern (HTW Berlin)

Offline-fähiger Chatbot-Kern für Fragen rund um das **„O ja! Orientierungsjahr Ausbildung und Studium“** der HTW Berlin.  
Der Bot arbeitet ohne LLM und ohne API-Keys auf Basis von `scikit-learn` (TF-IDF mit `analyzer="char_wb"`, `ngram_range=(2, 4)` und Kosinus-Ähnlichkeit). Dadurch ist er auch gegenüber Rechtschreibfehlern robust.

---

## Projektstruktur

- `bot.py` – Chatbot-Kern mit `antworte(frage)` und konfigurierbarem `SCHWELLENWERT` (Standard: `0.25`)
- `wissen.json` – Wissensdatenbank mit Intents, Beispiel-Formulierungen (mind. 5 pro Eintrag), Antworten und Quellen
- `cli.py` – Interaktive Konsolenschleife zum Testen
- `hinzufuegen.py` – Konsolenwerkzeug zum Hinzufügen neuer Einträge oder Beispiele in `wissen.json`
- `testfragen.json` – Testdatensatz (mind. 30 ungesehene Testfragen)
- `test.py` – Skript zur Evaluierung der Trefferquote
- `requirements.txt` – Python-Abhängigkeiten (ohne Web-Frameworks)
- `README.md` – Projektdokumentation

---

## 1. Installation

Voraussetzung ist **Python 3**. Installiere die benötigte Abhängigkeit (`scikit-learn`):

```bash
pip install -r requirements.txt
```

---

## 2. Start der Konsole

Starte den interaktiven Konsolen-Chatbot mit:

```bash
python cli.py
```

Tippe eine Frage ein und bestätige mit `Enter`. Zum Beenden tippe `exit` oder `beenden`.

---

## 3. Wie man Wissen ergänzt

Um neue Frage-Antwort-Paare (Intents mit mindestens 5 Beispiel-Formulierungen, Antwort und Quelle) oder weitere Beispiele zu bestehenden Intents hinzuzufügen, starte:

```bash
python hinzufuegen.py
```

Folge den Anweisungen in der Konsole. Die Änderungen werden direkt in `wissen.json` gespeichert.

---

## 4. Wie man den Bot testet

Um die Trefferquote anhand der `testfragen.json` automatisch zu messen, führe aus:

```bash
python test.py
```

Das Skript prüft jede Frage aus `testfragen.json` über `antworte(frage)` und gibt am Ende die Trefferquote in Prozent aus.

---

## 5. Spätere Anbindung einer Weboberfläche (`POST /chat`)

Der Chatbot-Kern (`bot.py`) hat bewusst keine Web-Abhängigkeiten. Eine spätere Web-API (mit **Flask** oder **FastAPI**) importiert lediglich `antworte` aus `bot.py`.

### Erwartetes Schnittstellenformat
- **Request:** `POST /chat` mit JSON-Body `{"frage": "Wie lange dauert das O-ja?"}`
- **Response:** JSON-Body `{"antwort": "...", "quelle": "..."}`

### Beispiel mit FastAPI

```python
from fastapi import FastAPI
from pydantic import BaseModel
from bot import antworte

app = FastAPI()

class ChatRequest(BaseModel):
    frage: str

@app.post("/chat")
def chat_endpoint(req: ChatRequest):
    return antworte(req.frage)
```

### Beispiel mit Flask

```python
from flask import Flask, request, jsonify
from bot import antworte

app = Flask(__name__)

@app.post("/chat")
def chat_endpoint():
    daten = request.get_json(silent=True) or {}
    frage = daten.get("frage", "")
    return jsonify(antworte(frage))
```
