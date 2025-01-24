import json
import os

# Ordner mit JSON-Profilen und Zielordner für Chunks
PROFILE_PATH = "Merged"
OUTPUT_PATH = "Profile_Chunks"

# Sicherstellen, dass der Ausgabeordner existiert
if not os.path.exists(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH)

# Liste aller relevanten Abschnitte
sections = [
    "auticonProjects", "studyProjects", "projects", "education",
    "professionalExperience", "studies", "training", "engagements",
    "privateProjects", "furtherProjects", "auticonTraining",
    "certificates", "certifications"
]

# Liste der zusätzlichen Felder, die berücksichtigt werden sollen
additional_fields = [
    "firstName", "lastName", "fullName", "autilityId", "autilityUrl",
    "position", "availibility", "workHoursPerWeek", "location",
    "travelArrangement", "speciality", "preferredWorkingAreas",
    "qualification"
]

# Funktion zur Erstellung einzelner Chunk-Dateien mit Nummerierung
def chunk_consultant_profile(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        profile = json.load(file)

    chunks = []
    profile_id = profile.get("autilityId", "unknown")
    profile_name = profile.get("fullName", "unknown")
    chunk_counter = 1  # Initiale Nummerierung der Chunks

    # Zusätzliche Felder als eigene Chunks hinzufügen
    for field in additional_fields:
        if field in profile:
            value = profile[field]
            
            # Fehlerbehandlung für verschiedene Datentypen
            if isinstance(value, list):
                content = ", ".join(map(str, value))
            elif isinstance(value, (str, int, float)):
                content = str(value)
            else:
                content = "N/A"  # Fallback für unerwartete Typen
            
            chunks.append({
                f"ChunkID {chunk_counter}": {
                    "type": field,
                    "content": content,
                    "source": profile_name
                }
            })
            chunk_counter += 1

    # Iteriere durch alle Abschnitte im Profil und erstelle Chunks mit Nummerierung
    for section in sections:
        if section in profile and section not in ["certificates", "languageSkills"]:
            for entry in profile[section]:
                chunks.append({
                    f"ChunkID {chunk_counter}": {
                        "type": section,
                        "content": f"{entry.get('startDate', 'N/A')} - {entry.get('endDate', 'N/A')} - {entry.get('description', '')}",
                        "source": profile_name
                    }
                })
                chunk_counter += 1

    # Zertifikate separat verarbeiten
    if "certificates" in profile:
        for certificate in profile["certificates"]:
            skills_content = ", ".join(certificate.get("skills", []))
            chunks.append({
                f"ChunkID {chunk_counter}": {
                    "type": "certificates",
                    "name": certificate.get("name", "N/A"),
                    "date": certificate.get("date", "N/A"),
                    "content": f"Skills: {skills_content}",
                    "source": profile_name
                }
            })
            chunk_counter += 1

    # Sprachkenntnisse separat verarbeiten
    if "languageSkills" in profile:
        for language in profile["languageSkills"]:
            chunks.append({
                f"ChunkID {chunk_counter}": {
                    "type": "languageSkills",
                    "name": language.get("name", "N/A"),
                    "level": language.get("level", "N/A"),
                    "content": language.get("levelDescription", "N/A"),
                    "source": profile_name
                }
            })
            chunk_counter += 1

    # Skills separat verarbeiten
    if "technicalSkills" in profile:
        for skill_category in profile["technicalSkills"]:
            category_name = skill_category["category"]["name"]
            skills = [skill["name"] for skill in skill_category["category"]["skills"]]
            chunks.append({
                f"ChunkID {chunk_counter}": {
                    "type": "technicalSkills",
                    "category": category_name,
                    "content": f"{category_name}: {', '.join(skills)}",
                    "source": profile_name
                }
            })
            chunk_counter += 1

    # Berufliche Zusammenfassung als einzelner Chunk
    if "professionalSummary" in profile:
        chunks.append({
            f"ChunkID {chunk_counter}": {
                "type": "professionalSummary",
                "content": profile["professionalSummary"],
                "source": profile_name
            }
        })

    # Speichere Chunks in einer separaten JSON-Datei pro Profil im Ordner profile_chunks
    output_file = os.path.join(OUTPUT_PATH, f"profile_{profile_id}.json")
    with open(output_file, "w", encoding="utf-8") as outfile:
        json.dump(chunks, outfile, indent=4, ensure_ascii=False)

    print(f"Chunks für {profile_name} gespeichert unter: {output_file}")

# Verarbeitung aller Profile in JSON-Dateien
for filename in os.listdir(PROFILE_PATH):
    if filename.endswith(".json"):
        chunk_consultant_profile(os.path.join(PROFILE_PATH, filename))
