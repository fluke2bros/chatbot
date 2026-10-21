import json
import os
from bot import antworte, lade_wissen

TESTFRAGEN_PFAD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testfragen.json")


def lade_testfragen(pfad: str = TESTFRAGEN_PFAD) -> list[dict]:
    """Lädt die Testfragen aus testfragen.json."""
    with open(pfad, "r", encoding="utf-8") as f:
        return json.load(f)


def evaluiere() -> tuple[int, int, float]:
    """
    Führt alle Testfragen gegen antworte() aus und misst die Trefferquote.
    Gibt (treffer, gesamt, quote_in_prozent) zurück.
    """
    wissen = lade_wissen()
    testfragen = lade_testfragen()

    intent_zu_antwort = {eintrag["intent"]: eintrag["antwort"] for eintrag in wissen}

    treffer = 0
    gesamt = len(testfragen)

    print("==================================================")
    print(f"  Starte Evaluierung mit {gesamt} Testfragen")
    print("==================================================\n")

    for idx, test in enumerate(testfragen, start=1):
        frage = test["frage"]
        erwarteter_intent = test["intent"]
        erwartete_antwort = intent_zu_antwort.get(erwarteter_intent)

        ergebnis = antworte(frage)
        erhaltene_antwort = ergebnis["antwort"]

        korrekt = erhaltene_antwort == erwartete_antwort
        if korrekt:
            treffer += 1
            status = "OK"
        else:
            status = "FEHLER"

        # Ermittle erkannten Intent zur Übersicht
        erkannter_intent = "fallback"
        for intent_name, antw_text in intent_zu_antwort.items():
            if antw_text == erhaltene_antwort:
                erkannter_intent = intent_name
                break

        print(f"[{idx:02d}/{gesamt:02d}] [{status}] Frage: \"{frage}\"")
        print(f"        Erwartet: {erwarteter_intent} | Erkannt: {erkannter_intent}")

    quote = (treffer / gesamt * 100.0) if gesamt > 0 else 0.0
    print("\n==================================================")
    print(f"  Ergebnis: {treffer} von {gesamt} Fragen richtig beantwortet")
    print(f"  Trefferquote: {quote:.2f}%")
    print("==================================================")
    return treffer, gesamt, quote


if __name__ == "__main__":
    evaluiere()
