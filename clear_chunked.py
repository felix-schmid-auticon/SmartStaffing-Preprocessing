import os

def loesche_json_und_zusammengefuehrt_txt(ordner):
    """
    Löscht alle .json-Dateien und alle Textdateien mit der Endung _zusammengefuehrt.txt
    im angegebenen Ordner.

    :param ordner: Der Pfad zum Ordner, in dem die Dateien gelöscht werden sollen.
    """
    if not os.path.exists(ordner):
        print(f"Der Ordner '{ordner}' wurde nicht gefunden.")
        return

    dateien = os.listdir(ordner)
    for datei in dateien:
        # Überprüfen, ob die Datei eine .json-Datei oder eine _zusammengefuehrt.txt ist
        if datei.endswith(".json") or datei.endswith("_zusammengefasst.txt"):
            datei_pfad = os.path.join(ordner, datei)
            try:
                os.remove(datei_pfad)
                print(f"Gelöscht: {datei}")
            except Exception as e:
                print(f"Fehler beim Löschen von {datei}: {e}")

if __name__ == "__main__":
    ordner = os.path.join(os.getcwd(), "Chunked")
    loesche_json_und_zusammengefuehrt_txt(ordner)
