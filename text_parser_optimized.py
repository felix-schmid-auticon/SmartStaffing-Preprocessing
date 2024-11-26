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
    bekannte_abschnitte = [
        "Name", "Profil", "IT-Skills", "Qualifikationen", "auticon Projekte",
        "Studium Projekte", "Projekte", "Ausbildung", "Beruflicher Werdegang",
        "Studium", "Weiterbildung", "Engagement", "Private Projekte", "Weitere Projekte"
    ]

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


def abschnitte_zu_json(abschnitte):
    """
    Transformiert die analysierten Abschnitte in die gewünschte JSON-Struktur.
    
    :param abschnitte: Dictionary mit analysierten Abschnitten.
    :return: JSON-kompatibles Dictionary.
    """
    json_daten = {
        "firstName": None,
        "lastName": None,
        "fullName": None,
        "autilityId": None,
        "autilityUrl": None,
        "position": None,
        "availibility": None,
        "workHoursPerWeek": None,
        "location": None,
        "travelArrangement": None,
        "speciality": None,
        "preferredWorkingAreas": [],
        "qualification": None,
        "technicalSkills": [],
        "professionalSummary": None,
    }

    if "Name" in abschnitte:
        name_parts = abschnitte["Name"].split()
        json_daten["firstName"] = name_parts[0] if len(name_parts) > 0 else None
        json_daten["lastName"] = name_parts[-1] if len(name_parts) > 1 else None
        json_daten["fullName"] = abschnitte["Name"]

    if "Profil" in abschnitte:
        json_daten["professionalSummary"] = abschnitte["Profil"]

    if "IT-Skills" in abschnitte:
        skills = abschnitte["IT-Skills"].split(",")
        for skill in skills:
            json_daten["technicalSkills"].append({
                "category": {
                    "name": "General Skills",
                    "skills": [
                        {
                            "name": skill.strip(),
                            "level": 1,
                            "levelDescription": "Grundkenntnisse"
                        }
                    ]
                }
            })

    if "Qualifikationen" in abschnitte:
        json_daten["qualification"] = abschnitte["Qualifikationen"]

    return json_daten


def textdateien_verarbeiten(dateipfade, ziel_datei_pfad, json_pfad):
    """
    Liest mehrere Textdateien ein, führt sie zusammen, analysiert die Abschnitte und speichert das Ergebnis als JSON.

    :param dateipfade: Liste mit den Pfaden der Dateien.
    :param ziel_datei_pfad: Pfad zur zusammengeführten Datei.
    :param json_pfad: Pfad zur JSON-Ausgabedatei.
    """
    try:
        gesamter_text = ""
        for datei_pfad in dateipfade:
            with open(datei_pfad, 'r', encoding='utf-8') as datei:
                gesamter_text += datei.read() + "\n\n"

        with open(ziel_datei_pfad, 'w', encoding='utf-8') as ziel_datei:
            ziel_datei.write(gesamter_text.strip())

        abschnitte = abschnitte_analysieren(gesamter_text)
        json_daten = abschnitte_zu_json(abschnitte)

        with open(json_pfad, 'w', encoding='utf-8') as json_datei:
            json.dump(json_daten, json_datei, indent=4, ensure_ascii=False)

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

        for datei in dateien:
            match = re.search(r"_\d+\.txt$", datei)
            if not match:
                print(f"Überspringe Datei ohne Zahl am Ende: {datei}")
                continue

            name = "_".join(datei.split("_")[:-1])
            if name not in consultants:
                consultants[name] = []
            consultants[name].append(os.path.join(chunked_verzeichnis, datei))
            
        for name, files in consultants.items():
            ziel_datei_pfad = os.path.join(chunked_verzeichnis, f"{name}_zusammengefuehrt.txt")
            json_pfad = os.path.join(chunked_verzeichnis, f"{name}.json")
            textdateien_verarbeiten(files, ziel_datei_pfad, json_pfad)

    except Exception as e:
        print(f"Es gab ein Problem beim Verarbeiten des Verzeichnisses '{chunked_verzeichnis}': {e}")


if __name__ == "__main__":
    chunked_verzeichnis = os.path.join(os.getcwd(), "Chunked")
    verarbeite_alle_consultants(chunked_verzeichnis)
