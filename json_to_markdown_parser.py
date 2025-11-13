import json
import os
from pathlib import Path

# Eingabe- und Ausgabeordner
INPUT_DIR = "Merged"
OUTPUT_DIR = "JSON_to_Markdown_Profiles"

# Ausgabeordner sicherstellen
os.makedirs(OUTPUT_DIR, exist_ok=True)


def list_to_str(value):
    """Liste oder einzelner Wert in eine schöne String-Darstellung konvertieren."""
    if isinstance(value, list):
        return ", ".join(str(v) for v in value)
    return "" if value is None else str(value)


def add_heading(lines, level, text):
    """Überschrift mit Leerzeilen davor/danach hinzufügen (MD022-konform)."""
    text = text.strip()
    if not text:
        return
    if lines and lines[-1].strip() != "":
        lines.append("")
    lines.append("#" * level + " " + text)
    lines.append("")  # Leerzeile nach der Überschrift


def add_text_block(lines, text):
    """Einen normalen Textblock anhängen (mit vorangehender Leerzeile)."""
    text = text.strip()
    if not text:
        return
    if lines and lines[-1].strip() != "":
        lines.append("")
    lines.append(text)


def add_bullet(lines, text):
    """Einen Bullet-Point hinzufügen."""
    text = text.strip()
    if not text:
        return
    lines.append(f"- {text}")


def add_section_list(lines, title, items):
    """
    Generische Hilfsfunktion für Abschnitte mit Einträgen,
    die startDate, endDate und description enthalten.
    """
    if not items:
        return
    add_heading(lines, 2, title)
    for item in items:
        start = (item.get("startDate") or "").strip()
        end = (item.get("endDate") or "").strip()
        desc = (item.get("description") or "").strip()

        # Überschrift pro Eintrag
        heading_parts = []
        if start:
            heading_parts.append(start)
        if end:
            heading_parts.append(end)
        heading_text = " – ".join(heading_parts) if heading_parts else ""

        if heading_text:
            add_heading(lines, 3, heading_text)
        if desc:
            add_text_block(lines, desc)


def convert_profile_to_markdown(data: dict) -> str:
    """Wandelt ein einzelnes JSON-Profil in eine Markdown-String-Repräsentation um."""
    lines = []

    full_name = data.get("fullName") or f"{data.get('firstName', '')} {data.get('lastName', '')}".strip()
    if not full_name:
        full_name = "Unbekannter Consultant"

    # Titel
    add_heading(lines, 1, full_name)

    # Basisinformationen
    add_heading(lines, 2, "Basisinformationen")
    position = data.get("position", "")
    avail = data.get("availibility", "")
    hours = data.get("workHoursPerWeek", "")
    location = data.get("location", "")
    travel = data.get("travelArrangement", "")
    speciality = data.get("speciality", "")
    preferred = list_to_str(data.get("preferredWorkingAreas", []))

    if position:
        add_bullet(lines, f"**Position:** {position}")
    if avail:
        add_bullet(lines, f"**Verfügbarkeit:** {avail}")
    if hours not in ("", None):
        add_bullet(lines, f"**Arbeitsstunden pro Woche:** {hours}")
    if location:
        add_bullet(lines, f"**Standort:** {location}")
    if travel:
        add_bullet(lines, f"**Reisebereitschaft:** {travel}")
    if speciality:
        add_bullet(lines, f"**Spezialisierung:** {speciality}")
    if preferred:
        add_bullet(lines, f"**Bevorzugte Tätigkeitsbereiche:** {preferred}")

    # Qualifikation
    qual = (data.get("qualification") or "").strip()
    if qual:
        add_heading(lines, 2, "Qualifikation")
        add_text_block(lines, qual)

    # Technische Skills
    tech_skills = data.get("technicalSkills", [])
    if tech_skills:
        add_heading(lines, 2, "Technische Skills")
        for category_item in tech_skills:
            category = category_item.get("category", {})
            cat_name = category.get("name", "").strip()
            skills = category.get("skills", [])

            if cat_name:
                add_heading(lines, 3, cat_name)
            for skill in skills:
                skill_name = skill.get("name", "").strip()
                level_desc = skill.get("levelDescription", "").strip()
                if skill_name:
                    if level_desc:
                        add_bullet(lines, f"**{skill_name}** ({level_desc})")
                    else:
                        add_bullet(lines, f"**{skill_name}**")

    # Berufliche Zusammenfassung
    prof_sum = (data.get("professionalSummary") or "").strip()
    if prof_sum:
        add_heading(lines, 2, "Berufliche Zusammenfassung")
        add_text_block(lines, prof_sum)

    # Auticon-Projekte
    add_section_list(lines, "Auticon Projekte", data.get("auticonProjects", []))

    # Studienprojekte
    add_section_list(lines, "Studienprojekte", data.get("studyProjects", []))

    # Berufserfahrung
    add_section_list(lines, "Berufserfahrung", data.get("professionalExperience", []))

    # Studium
    add_section_list(lines, "Studium", data.get("studies", []))

    # Weiterbildungen
    add_section_list(lines, "Weiterbildungen", data.get("training", []))

    # Engagements
    add_section_list(lines, "Engagements", data.get("engagements", []))

    # Zertifikate
    certificates = data.get("certificates", [])
    if certificates:
        add_heading(lines, 2, "Zertifikate")
        for cert in certificates:
            name = (cert.get("name") or "").strip()
            date = (cert.get("date") or "").strip()
            skills = list_to_str(cert.get("skills", []))

            heading = name
            if date:
                heading = f"{name} ({date})" if name else date

            if heading:
                add_heading(lines, 3, heading)
            if skills:
                add_text_block(lines, f"**Skills:** {skills}")

    # Sprachkenntnisse
    languages = data.get("languageSkills", [])
    if languages:
        add_heading(lines, 2, "Sprachkenntnisse")
        for lang in languages:
            lang_name = (lang.get("name") or "").strip()
            level_desc = (lang.get("levelDescription") or "").strip()
            if lang_name:
                if level_desc:
                    add_bullet(lines, f"**{lang_name}** ({level_desc})")
                else:
                    add_bullet(lines, f"**{lang_name}**")

    # Abschließenden String bauen
    # Überflüssige Leerzeilen am Ende entfernen
    while lines and lines[-1].strip() == "":
        lines.pop()

    return "\n".join(lines) + "\n"


def main():
    for filename in os.listdir(INPUT_DIR):
        if not filename.endswith(".json"):
            continue

        input_path = Path(INPUT_DIR) / filename
        with open(input_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                print(f"Fehler beim Lesen von {input_path}: {e}")
                continue

        markdown = convert_profile_to_markdown(data)

        output_name = filename.replace(".json", ".md")
        output_path = Path(OUTPUT_DIR) / output_name
        with open(output_path, "w", encoding="utf-8") as out:
            out.write(markdown)

        print(f"✅ {output_path} erstellt.")

if __name__ == "__main__":
    main()
