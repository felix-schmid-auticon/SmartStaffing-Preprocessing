# SmartStaffing-Preprocessing

Workflow:
Convert text-profiles into structured json-files.
Merge with information from autility-JSON's.
Split Profiles into chunks.
Create Embeddings and save to Database.
Implement query.
Integrate to Azure AI Studio.

Funktionen, Abhängigkeiten und Zusammenhänge der Skripte:

1. profile_parser.py fasst die Text-Profile im Ordner Chunked zusammen und erstellt von dieser Zusammenfassung ein JSON-Datei.
2. merge_jsons.py fasst die JSON-Dateien aus den Ordnern Chunked und Autility-JSON zusammen und speichert eine JSON-Datei für jeden Consultant im Ordner Merged.
3. profile_chunks.py zerlegt jeden Abschnitt in den JSON-Profilen in einzelne Chunks und speichert eine JSON-Datei mit den Chunks für jedes Profil in Profile_Chunks.
4. profile_chunks_optimized.py berücksichtigt die Chunk-Size bzw. Anzahl Tokens. Die Informationen werden in Metadaten und Chunks aufgeteilt. Chunks mit wenig Token werden zusammengefasst, große Chunks werden aufgeteilt. Eine eindeutige ID für jeden Chunk soll die Abrufbarkeit erleichtern. profile_chunks_optimized.py ist abhängig von den Ergebnissen aus profile_chunks.py. Die Ergebnisse werden in Optimized_Chunks gespeichert.

Hilfsfunktionen:

1. chunk_size_calculator.py berechnet die Tokenanzahl pro Chunk mit OpenAI Tokenizer für GPT-3.5/4.
2. clear_chunked.py löscht die Textdateien mit der Endung "_zusammengefasst.txt" und die JSON-Dateien im Ordner Chunked
3. rename_umlauts_autility_json.py ändert [ä, ü, ö] in [ae, ue, oe] und [Ä, Ü, Ö] in [Ae, Ue, Oe] im Ordner Autility-JSON.
4. rename_umlauts_chunked.py ändert [ä, ü, ö] in [ae, ue, oe] und [Ä, Ü, Ö] in [Ae, Ue, Oe] im Ordner Chunked.

ToDo: Eventuell Skripte und/oder Funktionen vereinfachen und/oder zusammenfassen.
