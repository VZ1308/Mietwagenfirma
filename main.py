import re
from datetime import datetime
from classes import Fahrzeug, PKW, Bus, Transporter, SUV, Kunde, Mietvertrag, Mietwagenfirma
import csv
import os

# Globale Instanz der Mietwagenfirma
firma = Mietwagenfirma("Meine Mietwagenfirma")

def welcome_message():
    current_date = datetime.now().strftime("%d.%m.%Y")
    message = f"Willkommen zum Mietwagenverwaltungsprogramm! \n----------Heute ist der {current_date}----------"
    print(message)


def speichern_in_datei():
    try:
        with open('kunden.csv', 'w', newline='') as kunden_datei:
            writer = csv.writer(kunden_datei)
            writer.writerow(['Name', 'Adresse', 'Telefonnummer', 'Email'])
            for kunde in firma.kunden:
                writer.writerow([kunde.name, kunde.adresse, kunde.telefonnummer, kunde.email])

        with open('mietvertraege.csv', 'w', newline='') as mietvertraege_datei:
            writer = csv.writer(mietvertraege_datei)
            writer.writerow(['Kunde', 'Fahrzeug', 'Anfangsdatum', 'Enddatum', 'Gesamtpreis'])
            for mietvertrag in firma.mietvertraege:
                writer.writerow(
                    [mietvertrag.kunde, mietvertrag.fahrzeug, mietvertrag.anfangsdatum, mietvertrag.enddatum, mietvertrag.gesamtpreis])

        with open('fahrzeuge.csv', 'w', newline='') as fahrzeuge_datei:
            writer = csv.writer(fahrzeuge_datei)
            writer.writerow(['Marke', 'Modell', 'Kennzeichen'])
            for fahrzeug in firma.fahrzeuge:
                writer.writerow([fahrzeug.marke, fahrzeug.modell, fahrzeug.baujahr, fahrzeug.mietpreis_pro_tag, fahrzeug.mietpreis_pro_stunde])

        print("Daten wurden erfolgreich gespeichert.")
    except Exception as e:
        print(f"Fehler beim Speichern der Daten: {e}")

def laden_aus_datei():
    try:
        if os.path.exists('kunden.csv'):
            with open('kunden.csv', 'r') as kunden_datei:
                reader = csv.DictReader(kunden_datei)
                firma.kunden = [Kunde(row['Name'], row['Adresse'], row['Telefonnummer'], row['Email']) for row in
                                reader]

        if os.path.exists('mietvertraege.csv'):
            with open('mietvertraege.csv', 'r') as mietvertraege_datei:
                reader = csv.DictReader(mietvertraege_datei)
                firma.mietvertraege = [Mietvertrag(row['Kunde'], row['Fahrzeug'], row['Anfangsdatum'], row['Enddatum'])
                                       for row in reader]

        if os.path.exists('fahrzeuge.csv'):
            with open('fahrzeuge.csv', 'r') as fahrzeuge_datei:
                reader = csv.DictReader(fahrzeuge_datei)
                firma.fahrzeuge = [Fahrzeug(row['Marke'], row['Modell'],row['Baujahr'], row['Mietpreis pro Tag'], row['Mietpreis pro Stunde']) for row in reader]

        print("Daten wurden erfolgreich geladen.")
    except FileNotFoundError:
        print("Die Dateien wurden nicht gefunden.")
    except Exception as e:
        print(f"Fehler beim Laden der Daten: {e}")
def validate_name(name):
    # Name sollte nur Buchstaben enthalten
    if not name.replace(" ", "").isalpha():
        raise ValueError("Ungültiger Name. Bitte geben Sie nur Buchstaben ein.")
    return name.strip().capitalize()


def validate_telefonnummer(telefonnummer):
    # Telefonnummer sollte nur aus Zahlen bestehen und 10-stellig sein
    telefonnummer = telefonnummer.strip()
    if not telefonnummer.isdigit() or len(telefonnummer) < 10:
        raise ValueError("Ungültige Telefonnummer. Bitte geben Sie eine Nummer mit mehr als 10 Zahlen ein.")
    return telefonnummer
def validate_baujahr(baujahr_str):
    # Überprüfung, ob das Baujahr eine Zahl ist
    while not baujahr_str.isdigit():
        print("Ungültiges Baujahr. Bitte geben Sie eine Zahl ein.")
        baujahr_str = input("Baujahr: ")
    return int(baujahr_str)

def validate_mietpreis(preis_str):
    # Überprüfung, ob der Mietpreis eine Zahl ist
    while not (re.match(r'^\d*\.?\d*$', preis_str) and float(preis_str) >= 0):
        print("Ungültiger Mietpreis. Bitte geben Sie eine positive Zahl ein.")
        preis_str = input("Mietpreis: ")
    return float(preis_str)
def menuefenster_kunden():
    while True:
        print("\n--------------------------")
        print("Kunden-Verwaltung")
        print("--------------------------")
        print("1. Kunde hinzufügen")
        print("2. Kunde entfernen")
        print("3. Alle Kunden anzeigen")
        print("4. Kunden filtern")
        print("5. Alle Mietverträge anzeigen")
        print("6. Speichern in Datei")
        print("7. Laden aus Datei")
        print("8. Zurück zum Hauptmenü")

        choice = input("Wählen Sie eine Option (1-8): ")

        if choice == '1':
            print("\n--- Kunde hinzufügen ---")
            try:
                name = validate_name(input("Name des Kunden: "))
                adresse = input("Adresse des Kunden: ").strip().capitalize()
                telefonnummer = int(validate_telefonnummer(input("Telefonnummer des Kunden: ")))
                email = input("Email-Adresse des Kunden: ")

                while not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                    print("Ungültige E-Mail-Adresse. Bitte geben Sie eine gültige E-Mail-Adresse ein.")
                    email = input("Email-Adresse des Kunden: ")

                kunde = Kunde(name, adresse, telefonnummer, email)
                firma.kunde_hinzufuegen(kunde)
                print(f"Kunde '{name}' wurde hinzugefügt.")
            except ValueError as ve:
                print(f"Fehler: {ve}")

        elif choice == '2':
            print("\n--- Kunde entfernen ---")
            name = input("Name des Kunden, den Sie entfernen möchten: ")
            found = False
            for kunde in firma.kunden:
                if kunde.name == name:
                    firma.kunden.remove(kunde)
                    found = True
                    print(f"Kunde '{name}' wurde entfernt.")
                    break
            if not found:
                print(f"Kunde '{name}' wurde nicht gefunden.")

        elif choice == '3':
            print("\n--- Alle Kunden anzeigen ---")
            firma.alle_kunden_anzeigen()

        elif choice == '4':
            filterwert = input("Welchen Kunden möchten Sie filtern? (Name oder Adresse): ")
            gefilterte_kunden = [k for k in firma.kunden if filterwert.lower() in k.name.lower() or filterwert.lower() in k.adresse.lower()]
            if gefilterte_kunden:
                print("\nGefilterte Kunden:")
                for kunde in gefilterte_kunden:
                    print(f"{kunde}")
            else:
                print(f"Keine Kunden gefunden, die '{filterwert}' enthalten.")

        elif choice == '5':
            print("\n--- Alle Mietverträge anzeigen ---")
            firma.alle_mietvertraege_anzeigen()


        elif choice == '6':
            print("\n--- Speichern in Datei ---")
            speichern_in_datei()

        elif choice == '7':
            print("\n--- Laden aus Datei ---")
            laden_aus_datei()

        elif choice == '8':
            print("Zurück zum Hauptmenü.")
            break

        else:
            print("Ungültige Eingabe. Bitte wählen Sie eine der angegebenen Optionen.")



def menuefenster_fahrzeug():
    while True:
        print("\n--------------------------")
        print("Fahrzeug-Verwaltung")
        print("--------------------------")
        print("1. Fahrzeug hinzufügen")
        print("2. Fahrzeug entfernen")
        print("3. Verfügbare Fahrzeuge anzeigen")
        print("4. Fahrzeug mieten")
        print("5. Alle Fahrzeuge anzeigen")
        print("6. Fahrzeuge in Datei speichern")
        print("7. Fahrzeuge aus Datei laden")
        print("8. Zurück zum Hauptmenü")

        choice = input("Wählen Sie eine Option (1-9): ")

        if choice == '1':
            print("\n--- Fahrzeug hinzufügen ---")
            print("Welches Fahrzeug möchten Sie hinzufügen?")
            print("1. PKW")
            print("2. SUV")
            print("3. Transporter")
            print("4. Bus")

            fahrzeugwahl = input("Wählen Sie eine Fahrzeugart (1-4): ")

            if fahrzeugwahl == '1':
                marke = input("Marke des PKW: ").strip().capitalize()
                modell = input("Modell des PKW: ").strip().capitalize()
                baujahr = validate_baujahr(input("Baujahr des PKW: "))
                mietpreis_pro_tag = validate_mietpreis(input("Mietpreis pro Tag des PKW (in €): "))
                mietpreis_pro_stunde = validate_mietpreis(input("Mietpreis pro Stunde des PKW (in €): "))
                sitzplaetze = int(input("Anzahl der Sitzplätze des PKW: "))

                pkw = PKW(marke, modell, baujahr, mietpreis_pro_tag, mietpreis_pro_stunde, sitzplaetze)
                firma.fahrzeug_hinzufuegen(pkw)
                print(f"Fahrzeug '{marke} {modell}' wurde hinzugefügt.")

            elif fahrzeugwahl == '2':
                marke = input("Marke des SUV: ").strip().capitalize()
                modell = input("Modell des SUV: ").strip().capitalize()
                baujahr = validate_baujahr(input("Baujahr des SUV: "))
                mietpreis_pro_tag = validate_mietpreis(input("Mietpreis pro Tag des SUV (in €): "))
                mietpreis_pro_stunde = validate_mietpreis(input("Mietpreis pro Stunde des SUV (in €): "))
                allrad = input("Hat der SUV Allradantrieb? (Ja/Nein): ").lower() == 'ja'

                suv = SUV(marke, modell, baujahr, mietpreis_pro_tag, mietpreis_pro_stunde, allrad)
                firma.fahrzeug_hinzufuegen(suv)
                print(f"Fahrzeug '{marke} {modell}' wurde hinzugefügt.")

            elif fahrzeugwahl == '3':
                marke = input("Marke des Transporters: ").strip().capitalize()
                modell = input("Modell des Transporters: ").strip().capitalize()
                baujahr = validate_baujahr(input("Baujahr des Transporters: "))
                mietpreis_pro_tag = validate_mietpreis(input("Mietpreis pro Tag des Transporters (in €): "))
                mietpreis_pro_stunde = validate_mietpreis(input("Mietpreis pro Stunde des Transporters (in €): "))
                ladevolumen = float(input("Ladevolumen des Transporters (in m³): "))

                transporter = Transporter(marke, modell, baujahr, mietpreis_pro_tag, mietpreis_pro_stunde, ladevolumen)
                firma.fahrzeug_hinzufuegen(transporter)
                print(f"Fahrzeug '{marke} {modell}' wurde hinzugefügt.")

            elif fahrzeugwahl == '4':
                marke = input("Marke des Busses: ").strip().capitalize()
                modell = input("Modell des Busses: ").strip().capitalize()
                baujahr = validate_baujahr(input("Baujahr des Busses: "))
                mietpreis_pro_tag = validate_mietpreis(input("Mietpreis pro Tag des Busses (in €): "))
                mietpreis_pro_stunde = validate_mietpreis(input("Mietpreis pro Stunde des Busses (in €): "))
                sitzplaetze = int(input("Anzahl der Sitzplätze des Busses: "))

                bus = Bus(marke, modell, baujahr, mietpreis_pro_tag, mietpreis_pro_stunde, sitzplaetze)
                firma.fahrzeug_hinzufuegen(bus)
                print(f"Fahrzeug '{marke} {modell}' wurde hinzugefügt.")

            else:
                print("Ungültige Eingabe. Bitte wählen Sie eine der angegebenen Optionen.")

        elif choice == '2':
            print("\n--- Fahrzeug entfernen ---")
            marke = input("Marke des Fahrzeugs, das Sie entfernen möchten: ").strip().capitalize()
            modell = input("Modell des Fahrzeugs, das Sie entfernen möchten: ").strip().capitalize()
            found = False
            for fahrzeug in firma.fahrzeuge:
                if fahrzeug.marke == marke and fahrzeug.modell == modell:
                    firma.fahrzeuge.remove(fahrzeug)
                    found = True
                    print(f"Fahrzeug '{marke} {modell}' wurde entfernt.")
                    break
            if not found:
                print(f"Fahrzeug '{marke} {modell}' wurde nicht gefunden.")

        elif choice == '3':
            print("\n--- Verfügbare Fahrzeuge anzeigen ---")
            firma.verfuegbare_fahrzeuge()


        elif choice == '4':

            print("\n--- Fahrzeug mieten ---")
            marke = input("Marke des Fahrzeugs, das Sie mieten möchten: ").strip().capitalize()
            modell = input("Modell des Fahrzeugs, das Sie mieten möchten: ").strip().capitalize()
            kundenname = input("Name des Kunden, der das Fahrzeug mieten möchte: ").strip().capitalize()
            anfangsdatum = input("Anfangsdatum (DD.MM.YYYY hh:mm): ")
            enddatum = input("Enddatum (DD.MM.YYYY hh:mm): ")

            try:
                anfangsdatum = datetime.strptime(anfangsdatum, "%d.%m.%Y %H:%M")
                enddatum = datetime.strptime(enddatum, "%d.%m.%Y %H:%M")
                mietvertrag = firma.fahrzeug_mieten(marke, modell, kundenname, anfangsdatum, enddatum)
                if mietvertrag:
                    print(f"Das Fahrzeug '{marke} {modell}' wurde erfolgreich an {kundenname} vermietet.")

            except ValueError:

                print(
                    "Fehler bei der Eingabe des Datums. Bitte geben Sie das Datum im richtigen Format ein (DD.MM.YYYY HH:MM).")

        elif choice == '5':
            print("\n--- Alle Fahrzeuge anzeigen ---")
            firma.alle_fahrzeuge_anzeigen()

        elif choice == '6':
            print("\n--- Fahrzeuge in Datei speichern ---")
            speichern_in_datei()

        elif choice == '7':
            print("\n--- Fahrzeuge aus Datei laden ---")
            laden_aus_datei()

        elif choice == '8':
            print("Zurück zum Hauptmenü.")
            break

        else:
            print("Ungültige Eingabe. Bitte wählen Sie eine der angegebenen Optionen.")

def hauptmenue():
    while True:
        print("\n--------------------------")
        print("        Hauptmenü")
        print("--------------------------")
        print("1. Kunden verwalten")
        print("2. Fahrzeuge verwalten")
        print("3. Programm beenden")

        choice = input("Wählen Sie eine Option (1-3): ")

        if choice == '1':
            menuefenster_kunden()

        elif choice == '2':
            menuefenster_fahrzeug()

        elif choice == '3':
            print("Programm wird beendet.")
            break

        else:
            print("Ungültige Eingabe. Bitte wählen Sie eine der angegebenen Optionen.")

if __name__ == "__main__":
    welcome_message()
    hauptmenue()
