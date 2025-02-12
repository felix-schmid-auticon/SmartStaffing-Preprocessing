import json
import os
import tiktoken

# OpenAI Tokenizer für GPT-3.5/4
encoding = tiktoken.get_encoding("cl100k_base")

PROFILE_CHUNKS_DIR = "Profile_Chunks"
OUTPUT_DIR = "Optimized_Chunks"
MAX_TOKENS = 500  # Obergrenze für einen Chunk
MIN_TOKENS = 50   # Untergrenze, um Chunks zusammenzufassen

# Sicherstellen, dass der Ausgabeordner existiert
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Liste der Abschnitte, die zusammengefasst werden sollen
merge_sections = ["technicalSkills", "professionalExperience", "auticonProjects"]

# Felder, die als Metadaten gespeichert werden sollen
metadata_fields = ["firstName", "lastName", "fullName", "autilityId", "autilityUrl",
                   "position", "availibility", "workHoursPerWeek", "location",
                   "travelArrangement", "speciality", "preferredWorkingAreas", "qualification", "languageSkills"]

def count_tokens(text):
    """Berechnet die Anzahl der Tokens im Text."""
    return len(encoding.encode(text))

def extract_autility_id(profile_data):
    """Extrahiert die autilityId aus den Chunks."""
    for chunk in profile_data.get("chunks", []):
        if chunk.get("type") == "autilityId":
            return chunk.get("content", "unknown")
    return "unknown"

def process_chunks():
    """Optimiert die Chunking-Strategie durch Zusammenfassung und Metadatenverwaltung."""
    for filename in os.listdir(PROFILE_CHUNKS_DIR):
        if filename.endswith(".json"):
            with open(os.path.join(PROFILE_CHUNKS_DIR, filename), "r", encoding="utf-8") as file:
                profile_data = json.load(file)
                chunks = profile_data.get("chunks", [])

                optimized_chunks = []
                metadata = {}
                merged_sections = {}
                chunk_counters = {}  # Speichert Zähler für jede "type"-Kategorie

                # Profil-ID aus den Chunks extrahieren
                profile_id = extract_autility_id(profile_data)

                # Zunächst Metadaten sammeln
                for chunk in chunks:
                    chunk_type = chunk.get("type", "unknown")
                    content = chunk.get("content", "")
                    token_count = count_tokens(content)

                    if chunk_type in metadata_fields:
                        metadata[chunk_type] = content  # Speichere als Metadaten
                    elif chunk_type in merge_sections:
                        if chunk_type not in merged_sections:
                            merged_sections[chunk_type] = []
                        merged_sections[chunk_type].append(content)
                    else:
                        # Falls eine Kategorie noch keinen Zähler hat, initialisieren wir ihn
                        if chunk_type not in chunk_counters:
                            chunk_counters[chunk_type] = 1

                        # Normale Chunks behalten, falls sie groß genug sind
                        if token_count >= MIN_TOKENS:
                            chunk_id = f"{profile_id}_{chunk_type}_{chunk_counters[chunk_type]}"
                            optimized_chunks.append({
                                "id": chunk_id,
                                "type": chunk_type,
                                "content": content
                            })
                            chunk_counters[chunk_type] += 1  # Inkrementiere Zähler

                # Merged Sections zusammenfügen
                for section, contents in merged_sections.items():
                    merged_content = " | ".join(contents)  # Trenner für Zusammenfassung
                    token_count = count_tokens(merged_content)

                    # Falls Chunk zu groß ist, aufteilen
                    if token_count > MAX_TOKENS:
                        parts = [merged_content[i:i+MAX_TOKENS] for i in range(0, len(merged_content), MAX_TOKENS)]
                        for idx, part in enumerate(parts, start=1):
                            chunk_id = f"{profile_id}_{section}_{idx}"
                            optimized_chunks.append({
                                "id": chunk_id,
                                "type": section,
                                "content": part
                            })
                    else:
                        chunk_id = f"{profile_id}_{section}_1"
                        optimized_chunks.append({
                            "id": chunk_id,
                            "type": section,
                            "content": merged_content
                        })

                # Speichern der optimierten Daten
                output_file = os.path.join(OUTPUT_DIR, filename)
                with open(output_file, "w", encoding="utf-8") as outfile:
                    json.dump({"metadata": metadata, "chunks": optimized_chunks}, outfile, indent=4, ensure_ascii=False)

                print(f"Optimierte Chunks gespeichert unter: {output_file}")

# Starte den Prozess
process_chunks()
