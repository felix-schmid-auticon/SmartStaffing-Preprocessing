import tiktoken
import json
import os

# OpenAI Tokenizer für GPT-3.5/4
encoding = tiktoken.get_encoding("cl100k_base")

# Verzeichnis mit JSON-Chunks
PROFILE_CHUNKS_DIR = "Profile_Chunks"

def count_tokens(text):
    """Berechnet die Anzahl der Tokens im Text."""
    return len(encoding.encode(text))

# Überprüfe die Tokenanzahl pro Chunk
for filename in os.listdir(PROFILE_CHUNKS_DIR):
    if filename.endswith(".json"):
        with open(os.path.join(PROFILE_CHUNKS_DIR, filename), "r", encoding="utf-8") as file:
            profile_data = json.load(file)
            chunks = profile_data.get("chunks", [])
            
            for chunk in chunks:
                content = chunk.get("content", "")
                token_count = count_tokens(content)
                print(f"Chunk: {chunk.get('source', 'unknown')} → {chunk.get('type', 'unknown')} → {token_count} Tokens")
