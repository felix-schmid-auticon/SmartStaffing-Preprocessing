import json
import os
from pathlib import Path

INPUT_DIR = "Merged"
OUTPUT_DIR = "Markdown_Profiles"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def list_to_md_list(lst):
    if not isinstance(lst, list):
        return str(lst)
    return ", ".join(lst)

def section_header(title):
    return f"\n## {title}\n"

def convert_json_to_markdown(data):
    md = []

    # Titel
    md.append(f"# {data.get('fullName', 'Unbekannt')}")

    # Basisinformationen
    md.append(section_header("Basisinformationen"))
    md.append(f"- **Position:** {data.get('position', '')}")
    md.append(f"- **Verfügbarkeit:** {data.get('availibility', '')}")
    md.append(f"- **Arbeitsstunden pro Woche:** {data.get('workHoursPerWeek', '')}")
    md.append(f"- **Standort:** {data.get('location', '')}")
    md.append(f"- **Reisebereitschaft:** {data.get('travelArrangement', '')}")
    md.append(f"- **Spezialisierung:** {data.get('speciality', '')}")
    md.append(f"- **Bevorzugte Tätigkeitsbereiche:** {list_to_md_list(data.get('preferredWorkingAreas', []))}")

    # Qualifikation
    md.append(section_header("Qualifikation"))
    md.append(data.get("qualification", ""))

    # Technische Skills
    md.append(section_header("Technische Skills"))
    for category in data.get("technicalSkills", []):
        cat = category.get("category", {})
        md.append(f"### {cat.get('name', '')}")
        for skill in cat.get("skills", []):
            md.append(f"- **{skill.get('name', '')}** ({skill.get('levelDescription', '')})")

    # Berufliche Zusammenfassung
    if "professionalSummary" in data:
        md.append(section_header("Berufliche Zusammenfassung"))
        md.append(data["professionalSummary"])

    # Generische Funktion für Listenabschnitte
    def add_section(title, key):
        items = data.get(key, [])
        if items:
            md.append(section_header(title))
            for item in items:
                start = item.get("startDate", "")
                end = item.get("endDate", "")
                desc = item.get("description", "")
                md.append(f"### {start} – {end}\n{desc}")

    add_section("Auticon Projekte", "auticonProjects")
    add_section("Studienprojekte", "studyProjects")
    add_section("Berufserfahrung", "professionalExperience")
    add_section("Studium", "studies")
    add_section("Weiterbildungen", "training")
    add_section("Engagements", "engagements")

    # Zertifikate
    certs = data.get("certificates", [])
    if certs:
        md.append(section_header("Zertifikate"))
        for cert in certs:
            name = cert.get("name", "")
            date = cert.get("date", "")
            skills = list_to_md_list(cert.get("skills", []))
            md.append(f"### {name} ({date})\n**Skills:** {skills}")

    # Sprachkenntnisse
    langs = data.get("languageSkills", [])
    if langs:
        md.append(section_header("Sprachkenntnisse"))
        for lang in langs:
            md.append(f"- **{lang.get('name', '')}** ({lang.get('levelDescription', '')})")

    return "\n".join(md)


# Verarbeitung aller Profile
for filename in os.listdir(INPUT_DIR):
    if filename.endswith(".json"):
        with open(os.path.join(INPUT_DIR, filename), "r", encoding="utf-8") as f:
            data = json.load(f)

        markdown = convert_json_to_markdown(data)

        output_path = Path(OUTPUT_DIR) / (filename.replace(".json", ".md"))
        with open(output_path, "w", encoding="utf-8") as out:
            out.write(markdown)

        print(f"{output_path} erstellt.")
