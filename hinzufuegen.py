import json
import os
from bot import WISSEN_PFAD, lade_wissen


def speichere_wissen(wissen: list[dict], pfad: str = WISSEN_PFAD) -> None:
    """Speichert die aktualisierte Wissensbasis formatiert in wissen.json."""
    with open(pfad, "w", encoding="utf-8") as f:
        json.dump(wissen, f, ensure_ascii=False, indent=2)


def main() -> None:
    print("==================================================")
    print("  Wissen ergänzen (wissen.json)")
    print("==================================================\n")

    if os.path.exists(WISSEN_PFAD):
        wissen = lade_wissen(WISSEN_PFAD)
    else:
        wissen = []

    vorhandene_intents = {eintrag["intent"]: eintrag for eintrag in wissen}

    try:
        intent = input("Intent-Name (z. B. 'kosten' oder 'studiendauer'): ").strip()
        if not intent:
            print("Abbruch: Der Intent-Name darf nicht leer sein.")
            return

        if intent in vorhandene_intents:
            print(f"\nHinweis: Der Intent '{intent}' existiert bereits.")
            aktion = input("Möchtest du (b)eispiele ergänzen oder den Eintrag (u)eberschreiben? [b/u]: ").strip().lower()
            if aktion == "b":
                eintrag = vorhandene_intents[intent]
                print("Gib neue Beispiel-Formulierungen ein (leere Zeile zum Beenden):")
                hinzugefuegt = 0
                while True:
                    bsp = input(f"  Beispiel {len(eintrag['beispiele']) + 1}: ").strip()
                    if not bsp:
                        break
                    eintrag["beispiele"].append(bsp)
                    hinzugefuegt += 1
                speichere_wissen(wissen)
                print(f"\nErfolgreich {hinzugefuegt} Beispiel(e) zum Intent '{intent}' hinzugefügt!")
                return
            elif aktion != "u":
                print("Abbruch.")
                return

        print("\nGib mindestens 5 Beispiel-Formulierungen für die Frage ein:")
        beispiele: list[str] = []
        while len(beispiele) < 5:
            bsp = input(f"  Beispiel {len(beispiele) + 1} (Pflicht): ").strip()
            if bsp:
                beispiele.append(bsp)
            else:
                print("  Bitte gib eine gültige Formulierung ein (mindestens 5 erforderlich).")

        while True:
            bsp = input(f"  Beispiel {len(beispiele) + 1} (optional, Enter zum Fortfahren): ").strip()
            if not bsp:
                break
            beispiele.append(bsp)

        antwort = ""
        while not antwort:
            antwort = input("\nAntworttext: ").strip()
            if not antwort:
                print("  Die Antwort darf nicht leer sein.")

        quelle = ""
        while not quelle:
            quelle = input("Quelle (URL oder Hinweis): ").strip()
            if not quelle:
                print("  Bitte gib eine Quelle an.")

        neuer_eintrag = {
            "intent": intent,
            "beispiele": beispiele,
            "antwort": antwort,
            "quelle": quelle,
        }

        if intent in vorhandene_intents:
            for i, e in enumerate(wissen):
                if e["intent"] == intent:
                    wissen[i] = neuer_eintrag
                    break
        else:
            wissen.append(neuer_eintrag)

        speichere_wissen(wissen)
        print(f"\nEintrag '{intent}' mit {len(beispiele)} Beispielen erfolgreich in wissen.json gespeichert!")

    except (EOFError, KeyboardInterrupt):
        print("\nVorgang abgebrochen.")


if __name__ == "__main__":
    main()
