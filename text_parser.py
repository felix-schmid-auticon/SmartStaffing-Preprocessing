import os
import json
import re


def abschnitte_analysieren(text):
    """
    Erkennt automatisch die Abschnitte in einem Text und teilt ihn auf,
    basierend auf bekannten Abschnittsnamen und ungleichmäßigen Abständen.

    :param text: Der gesamte Text.
    :return: Ein Dictionary mit Abschnittsnamen als Schlüssel und den zugehörigen Text als Wert.
    """
    # Liste der bekannten Abschnittsnamen
    bekannte_abschnitte = [
        "Name", "Profil", "IT-Skills", "Qualifikationen", "auticon Projekte",
        "Studium Projekte", "Projekte", "Ausbildung", "Beruflicher Werdegang",
        "Studium", "Weiterbildung", "Engagement", "Private Projekte", "Weitere Projekte"
    ]

    # Regex zur Erkennung der bekannten Abschnittsüberschriften
    # Enthält Abschnittsnamen
    abschnittsmuster = re.compile(
        r"^(" + "|".join(re.escape(abschnitt) for abschnitt in bekannte_abschnitte) + r")\b",
        re.IGNORECASE | re.MULTILINE
    )

    abschnitte = {}
    matches = list(abschnittsmuster.finditer(text))
    for i, match in enumerate(matches):
        abschnitt_name = match.group(1).strip()  # group(1) enthält den Abschnittsnamen
        start = match.end()

        # Bestimme das Ende des Abschnitts (nächster Abschnitt oder Ende des Textes)
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)

        # Extrahiere den Textblock für diesen Abschnitt
        abschnitt_inhalt = text[start:end].strip()
        if abschnitt_inhalt:
            abschnitte[abschnitt_name] = abschnitt_inhalt
        else:
            abschnitte[abschnitt_name] = None  # Leere Abschnitte explizit kennzeichnen

    return abschnitte





def textdateien_verarbeiten(dateipfade, ziel_datei_pfad, json_pfad):
    """
    Liest mehrere Textdateien ein, führt sie zusammen, analysiert die Abschnitte und speichert das Ergebnis als JSON.

    :param dateipfade: Liste mit den Pfaden der Dateien.
    :param ziel_datei_pfad: Pfad zur zusammengeführten Datei.
    :param json_pfad: Pfad zur JSON-Ausgabedatei.
    """
    try:
        # Inhalte aller Dateien einlesen und zusammenführen
        gesamter_text = ""
        for datei_pfad in dateipfade:
            with open(datei_pfad, 'r', encoding='utf-8') as datei:
                gesamter_text += datei.read() + "\n\n"

        # Zusammengeführte Datei speichern
        with open(ziel_datei_pfad, 'w', encoding='utf-8') as ziel_datei:
            ziel_datei.write(gesamter_text.strip())

        # Text analysieren und Abschnitte erkennen
        abschnitte = abschnitte_analysieren(gesamter_text)

        # JSON speichern
        with open(json_pfad, 'w', encoding='utf-8') as json_datei:
            json.dump(abschnitte, json_datei, indent=4, ensure_ascii=False)

        print(f"JSON-Datei für {json_pfad} erfolgreich erstellt.")

    except Exception as e:
        print(f"Es gab ein Problem beim Verarbeiten der Dateien {dateipfade}: {e}")


def verarbeite_alle_consultants(chunked_verzeichnis):
    """
    Verarbeitet alle Consultant-Profile im Verzeichnis Chunked.
    Dateien werden kombiniert und als JSON gespeichert.

    :param chunked_verzeichnis: Pfad zum Ordner, der die Dateien enthält.
    """
    try:
        if not os.path.exists(chunked_verzeichnis):
            print(f"Der Ordner '{chunked_verzeichnis}' wurde nicht gefunden.")
            return

        dateien = sorted([f for f in os.listdir(chunked_verzeichnis) if f.endswith('.txt')])
        consultants = {}

        # Gruppiere Dateien zu Consultants basierend auf Namensschema
        for datei in dateien:
            # Überprüfen, ob die Datei eine Zahl am Ende hat
            match = re.search(r"_\d+\.txt$", datei)
            if not match:
                print(f"Überspringe Datei ohne Zahl am Ende: {datei}")
                continue

            name = "_".join(datei.split("_")[:-1])  # Entferne die Nummer und Dateiendung
            if name not in consultants:
                consultants[name] = []
            consultants[name].append(os.path.join(chunked_verzeichnis, datei))
            
        for name, files in consultants.items():
            # Erlaube beliebige Anzahl an Dateien
            ziel_datei_pfad = os.path.join(chunked_verzeichnis, f"{name}_zusammengefuehrt.txt")
            json_pfad = os.path.join(chunked_verzeichnis, f"{name}.json")

            textdateien_verarbeiten(files, ziel_datei_pfad, json_pfad)

    except Exception as e:
        print(f"Es gab ein Problem beim Verarbeiten des Verzeichnisses '{chunked_verzeichnis}': {e}")


if __name__ == "__main__":
    chunked_verzeichnis = os.path.join(os.getcwd(), "Chunked")
    verarbeite_alle_consultants(chunked_verzeichnis)
