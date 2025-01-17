import os
import re
import json


def abschnitte_analysieren(text, bekannte_abschnitte):
    """
    Erkennt Abschnitte und deren Inhalte basierend auf bekannten Abschnittsnamen.
    """
    abschnittsmuster = re.compile(
        r"^(" + "|".join(re.escape(abschnitt) for abschnitt in bekannte_abschnitte) + r")\b",
        re.IGNORECASE | re.MULTILINE
    )

    abschnitte = {}
    matches = list(abschnittsmuster.finditer(text))
    for i, match in enumerate(matches):
        abschnitt_name = match.group(1).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        abschnitt_inhalt = text[start:end].strip()
        abschnitte[abschnitt_name] = abschnitt_inhalt if abschnitt_inhalt else None

    return abschnitte


def extrahiere_daten_mit_regex(abschnitt_inhalt):
    """
    Extrahiert Unterabschnitte aus dem Abschnittsinhalt basierend auf Datumsformaten.
    """
    date_regex = re.compile(
        r"(?:(Seit|seit|Ab|ab)\s+)?(\d{2}/\d{4}|\d{4})(?:\s*[-–]\s*(\d{2}/\d{4}|\d{4}|aktuell))?\s*(.*)",
        re.IGNORECASE
    )
    eintraege = []
    zeilen = abschnitt_inhalt.split("\n")
    aktueller_eintrag = None

    for zeile in zeilen:
        zeile = zeile.strip()
        if not zeile:
            continue  # Überspringe leere Zeilen
        match = date_regex.match(zeile)
        if match:
            # Neuer Eintrag beginnt
            if aktueller_eintrag:
                eintraege.append(aktueller_eintrag)
            aktueller_eintrag = {
                "startDate": f"{match.group(1) or ''} {match.group(2)}".strip(),
                "endDate": match.group(3),
                "description": match.group(4).strip()
            }
        else:
            # Zeile gehört zum vorherigen Eintrag (Fließtext)
            if aktueller_eintrag:
                aktueller_eintrag["description"] += f" {zeile}"

    # Füge den letzten Eintrag hinzu
    if aktueller_eintrag:
        eintraege.append(aktueller_eintrag)

    return eintraege


def abschnitte_zu_json(abschnitte):
    """
    Transformiert Abschnitte in JSON-kompatibles Format und übersetzt die Abschnittsnamen ins Englische.
    """
    # Mapping der deutschen Abschnittsnamen zu englischen Bezeichnungen
    mapping = {
        "auticon Projekte": "auticonProjects",
        "Studium Projekte": "studyProjects",
        "Projekte": "projects",
        "Ausbildung": "education",
        "Beruflicher Werdegang": "professionalExperience",
        "Studium": "studies",
        "Weiterbildung": "training",
        "Engagement": "engagements",
        "Private Projekte": "privateProjects",
        "Weitere Projekte": "furtherProjects",
        "auticon Weiterbildungen": "auticonTraining",
        "Zertifikate": "certificates",
        "Zertifizierungen": "certifications",
    }

    json_daten = {}
    for abschnitt, inhalt in abschnitte.items():
        # Übersetze Abschnittsnamen ins Englische
        englischer_abschnitt = mapping.get(abschnitt, abschnitt)
        if inhalt:
            json_daten[englischer_abschnitt] = extrahiere_daten_mit_regex(inhalt)
    return json_daten


def zeige_abschnitte_im_terminal(abschnitte, dateiname):
    """
    Zeigt die gefundenen Abschnitte im Terminal an.
    """
    print(f"\nGefundene Abschnitte in {dateiname}:")
    for abschnitt, inhalt in abschnitte.items():
        print(f"- {abschnitt}")
    print("\n")


def textdateien_verarbeiten(dateipfade, ziel_datei_pfad, json_pfad, bekannte_abschnitte):
    """
    Liest Textdateien, analysiert Abschnitte und speichert das Ergebnis als JSON.
    """
    gesamter_text = ""
    for datei_pfad in dateipfade:
        with open(datei_pfad, 'r', encoding='utf-8') as datei:
            gesamter_text += datei.read() + "\n\n"

    abschnitte = abschnitte_analysieren(gesamter_text, bekannte_abschnitte)

    # Zeige die gefundenen Abschnitte im Terminal an
    zeige_abschnitte_im_terminal(abschnitte, os.path.basename(ziel_datei_pfad))

    json_daten = abschnitte_zu_json(abschnitte)

    with open(ziel_datei_pfad, 'w', encoding='utf-8') as ziel_datei:
        ziel_datei.write(gesamter_text.strip())

    with open(json_pfad, 'w', encoding='utf-8') as json_datei:
        json.dump(json_daten, json_datei, indent=4, ensure_ascii=False)


def verarbeite_alle_consultants(chunked_verzeichnis):
    """
    Verarbeitet alle Consultant-Profile im Verzeichnis 'Chunked'.
    """
    bekannte_abschnitte = [
        "auticon Projekte", "Studium Projekte", "Projekte", "Ausbildung", "Beruflicher Werdegang",
        "Studium", "Weiterbildung", "Engagement", "Private Projekte", "Weitere Projekte",
        "auticon Weiterbildungen"
    ]

    if not os.path.exists(chunked_verzeichnis):
        print(f"Der Ordner '{chunked_verzeichnis}' wurde nicht gefunden.")
        os.makedirs(chunked_verzeichnis, exist_ok=True)

    dateien = sorted([f for f in os.listdir(chunked_verzeichnis) if f.endswith('.txt')])
    consultants = {}

    # Suche nach Eingabedateien mit passendem Muster
    for datei in dateien:
        match = re.match(r"^([A-Za-z]+_[A-Za-z]+)_[0-9]+\.txt$", datei)  # Dateien wie John_Doe_1.txt
        if not match:
            continue
        name = match.group(1)  # Extrahiere 'John_Doe'
        if name not in consultants:
            consultants[name] = []
        consultants[name].append(os.path.join(chunked_verzeichnis, datei))

    # Verarbeitung der Consultants
    for name, files in consultants.items():
        ziel_datei_pfad = os.path.join(chunked_verzeichnis, f"{name}_zusammengefuehrt.txt")
        json_pfad = os.path.join(chunked_verzeichnis, f"{name}.json")
        textdateien_verarbeiten(files, ziel_datei_pfad, json_pfad, bekannte_abschnitte)

if __name__ == "__main__":
    chunked_verzeichnis = os.path.join(os.getcwd(), "Chunked")
    verarbeite_alle_consultants(chunked_verzeichnis)
