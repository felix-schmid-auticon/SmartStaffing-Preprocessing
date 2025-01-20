import os
import json


def append_json_data(file1_path, file2_path):
    """
    Liest zwei JSON-Dateien ein und fügt die Inhalte der zweiten Datei
    direkt an die erste Datei hinzu, ohne additionalInfo zu verwenden.

    :param file1_path: Pfad zur ersten JSON-Datei (Basis).
    :param file2_path: Pfad zur zweiten JSON-Datei (hinzuzufügende Daten).
    :return: Ein Dictionary mit der kombinierten Struktur.
    """
    try:
        with open(file1_path, 'r', encoding='utf-8') as file1:
            data1 = json.load(file1)
        with open(file2_path, 'r', encoding='utf-8') as file2:
            data2 = json.load(file2)

        # Inhalte von file2 an data1 "anhängen", ohne additionalInfo
        if isinstance(data1, dict) and isinstance(data2, dict):
            for key, value in data2.items():
                if key in data1 and isinstance(data1[key], list) and isinstance(value, list):
                    # Falls der Schlüssel bereits existiert und beide Werte Listen sind, zusammenführen
                    data1[key].extend(value)
                elif key in data1 and isinstance(data1[key], dict) and isinstance(value, dict):
                    # Falls beide Werte Dictionaries sind, zusammenführen
                    data1[key].update(value)
                else:
                    # Schlüssel existiert nicht in data1, füge neuen Schlüssel hinzu
                    data1[key] = value
        else:
            print("Fehler: Beide Dateien müssen JSON-Objekte sein (keine Arrays).")
            return None

        return data1

    except Exception as e:
        print(f"Fehler beim Anhängen von {file2_path} an {file1_path}: {e}")
        return None


def merge_all_json_files(folder1, folder2, output_folder):
    """
    Kombiniert alle JSON-Dateien aus zwei Ordnern paarweise und speichert die Ergebnisse.
    Daten aus Ordner1 werden an Daten aus Ordner2 angehängt.

    :param folder1: Pfad zum ersten Ordner (zusätzliche Daten).
    :param folder2: Pfad zum zweiten Ordner (Basisdaten).
    :param output_folder: Pfad zum Ordner, in dem die kombinierten Dateien gespeichert werden sollen.
    """
    try:
        # Ordner erstellen, falls nicht vorhanden
        os.makedirs(output_folder, exist_ok=True)

        # Alle JSON-Dateien in den beiden Ordnern
        files1 = {f for f in os.listdir(folder1) if f.endswith('.json')}
        files2 = {f for f in os.listdir(folder2) if f.endswith('.json')}

        # Gemeinsame Dateien identifizieren
        common_files = files1 & files2

        if not common_files:
            print("Keine gemeinsamen JSON-Dateien gefunden.")
            return

        for file_name in common_files:
            file1_path = os.path.join(folder2, file_name)  # Basisdaten
            file2_path = os.path.join(folder1, file_name)  # Zusätzliche Daten
            output_path = os.path.join(output_folder, file_name)

            merged_data = append_json_data(file1_path, file2_path)
            if merged_data is not None:
                with open(output_path, 'w', encoding='utf-8') as output_file:
                    json.dump(merged_data, output_file, indent=4, ensure_ascii=False)
                print(f"Kombinierte Datei gespeichert: {output_path}")

    except Exception as e:
        print(f"Fehler beim Verarbeiten der Ordner: {e}")


if __name__ == "__main__":
    # Ordnerpfade
    chunked_folder = os.path.join(os.getcwd(), "Chunked")
    autility_json_folder = os.path.join(os.getcwd(), "Autility-JSON")
    merged_folder = os.path.join(os.getcwd(), "Merged")

    # Dateien zusammenführen
    merge_all_json_files(chunked_folder, autility_json_folder, merged_folder)
