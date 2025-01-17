import os
import re

def ersetze_umlaute_in_dateinamen(ordner):
    """
    Ersetzt Umlaute (ä, ö, ü) in Dateinamen durch Umschreibungen (ae, oe, ue)
    im angegebenen Ordner. Es werden nur Dateien umbenannt, die dem Muster
    Vorname_Nachname_Zahl.txt entsprechen.
    
    :param ordner: Der Pfad zum Ordner, in dem die Dateien umbenannt werden sollen.
    """
    if not os.path.exists(ordner):
        print(f"Der Ordner '{ordner}' wurde nicht gefunden.")
        return
    
    dateien = os.listdir(ordner)
    for datei in dateien:
        # Prüfen, ob der Dateiname dem Muster Vorname_Nachname_Zahl.txt entspricht
        if re.match(r"^[A-Za-zäöüÄÖÜ]+_[A-Za-zäöüÄÖÜ]+\.json$", datei):
            neuer_name = (
                datei.replace("ä", "ae")
                     .replace("ö", "oe")
                     .replace("ü", "ue")
                     .replace("Ä", "Ae")
                     .replace("Ö", "Oe")
                     .replace("Ü", "Ue")
            )
            alter_pfad = os.path.join(ordner, datei)
            neuer_pfad = os.path.join(ordner, neuer_name)
            # Umbenennen der Datei
            os.rename(alter_pfad, neuer_pfad)
            print(f"Umbenannt: {datei} -> {neuer_name}")

if __name__ == "__main__":
    ordner = os.path.join(os.getcwd(), "Autility-JSON")
    ersetze_umlaute_in_dateinamen(ordner)
