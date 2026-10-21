from bot import antworte


def main() -> None:
    print("==================================================")
    print("  HTW Berlin – O-ja! Orientierungsjahr Chatbot")
    print("  Tippe 'exit' oder 'beenden' zum Schließen.")
    print("==================================================\n")

    while True:
        try:
            frage = input("Du: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAuf Wiedersehen!")
            break

        if not frage:
            continue

        if frage.lower() in {"exit", "quit", "beenden", "q"}:
            print("Bot: Auf Wiedersehen! Viel Erfolg bei deiner Studien- und Berufswahl.")
            break

        ergebnis = antworte(frage)
        print(f"Bot: {ergebnis['antwort']}")
        print(f"Quelle: {ergebnis['quelle']}\n")


if __name__ == "__main__":
    main()
