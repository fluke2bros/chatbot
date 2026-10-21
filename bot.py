import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Konfigurierbarer Schwellenwert für die Kosinus-Ähnlichkeit
SCHWELLENWERT = 0.25

# Pfad zur Wissensdatenbank
WISSEN_PFAD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wissen.json")

# Fallback-Antwort mit Verweis auf die Allgemeine Studienberatung der HTW Berlin
FALLBACK_ANTWORT = (
    "Leider konnte ich zu deiner Frage keine passende Antwort zum Orientierungsjahr (O-ja) finden. "
    "Bitte wende dich direkt an die Allgemeine Studienberatung der HTW Berlin oder an das O-ja-Projektteam "
    "(E-Mail: o-ja@htw-berlin.de)."
)
FALLBACK_QUELLE = "https://www.htw-berlin.de/studium/studienorientierung/studienberatung/"


def lade_wissen(pfad: str = WISSEN_PFAD) -> list[dict]:
    """Lädt die Wissensbasis aus der JSON-Datei."""
    with open(pfad, "r", encoding="utf-8") as f:
        return json.load(f)


def antworte(frage: str, schwellenwert: float | None = None) -> dict[str, str]:
    """
    Vergleicht die Nutzerfrage mittels TF-IDF (char_wb, ngram_range 2-4) und
    Kosinus-Ähnlichkeit mit allen hinterlegten Beispielen in wissen.json.

    Gibt ein Dictionary zurück: {"antwort": "...", "quelle": "..."}
    """
    limit = SCHWELLENWERT if schwellenwert is None else schwellenwert

    if not frage or not frage.strip():
        return {
            "antwort": FALLBACK_ANTWORT,
            "quelle": FALLBACK_QUELLE,
        }

    wissen = lade_wissen()

    alle_beispiele: list[str] = []
    eintrag_zuordnung: list[dict] = []

    for eintrag in wissen:
        for beispiel in eintrag.get("beispiele", []):
            alle_beispiele.append(beispiel)
            eintrag_zuordnung.append(eintrag)

    if not alle_beispiele:
        return {
            "antwort": FALLBACK_ANTWORT,
            "quelle": FALLBACK_QUELLE,
        }

    vectorizer = TfidfVectorizer(
        analyzer="char_wb",
        ngram_range=(2, 4),
        lowercase=True,
    )

    tfidf_matrix = vectorizer.fit_transform(alle_beispiele)
    frage_vektor = vectorizer.transform([frage.strip()])

    aehnlichkeiten = cosine_similarity(frage_vektor, tfidf_matrix)[0]
    bester_index = int(aehnlichkeiten.argmax())
    beste_aehnlichkeit = float(aehnlichkeiten[bester_index])

    if beste_aehnlichkeit < limit:
        return {
            "antwort": FALLBACK_ANTWORT,
            "quelle": FALLBACK_QUELLE,
        }

    bester_eintrag = eintrag_zuordnung[bester_index]
    return {
        "antwort": bester_eintrag["antwort"],
        "quelle": bester_eintrag["quelle"],
    }
