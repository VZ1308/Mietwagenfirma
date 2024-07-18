import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import csv
from classes import Fahrzeug, PKW, Bus, Transporter, SUV, Kunde, Mietvertrag, Mietwagenfirma

# Globale Instanz der Mietwagenfirma
firma = Mietwagenfirma("Meine Mietwagenfirma")

# Dateinamen für CSV-Dateien
kunden_csv = "kunden.csv"
fahrzeuge_csv = "fahrzeuge.csv"
mietvertraege_csv = "mietvertraege.csv"

# Laden von Kunden, Fahrzeugen und Mietverträgen aus CSV-Dateien
def load_data_from_csv():
    try:
        if kunden_csv:
            with open(kunden_csv, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                next(reader)  # Ignoriere die Header-Zeile
                for row in reader:
                    try:
                        if len(row) != 4:
                            print(f"Ungültige Zeile in der Kunden-CSV-Datei: {row}")
                            continue
                        name, adresse, telefonnummer, email = row
                        kunde = Kunde(name, adresse, telefonnummer, email)
                        firma.kunde_hinzufuegen(kunde)
                    except Exception as e:
                        print(f"Fehler beim Verarbeiten einer Kundenzeile: {row}. Fehler: {e}")

        if fahrzeuge_csv:
            with open(fahrzeuge_csv, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                next(reader)  # Ignoriere die Header-Zeile
                for row in reader:
                    try:
                        # Prüfe, ob die Anzahl der Elemente in der Zeile korrekt ist
                        if len(row) < 9:
                            print(f"Ungültige Zeile in der Fahrzeug-CSV-Datei: {row}")
                            continue

                        # Entpacke die Werte
                        typ, marke, modell, baujahr, mietpreis_pro_tag, mietpreis_pro_stunde, sitzplaetze, ladeflaeche, allrad = row

                        # Verwende Standardwerte, falls notwendig
                        sitzplaetze = int(sitzplaetze) if sitzplaetze else 5  # Standardwert für Sitzplätze
                        ladeflaeche = float(ladeflaeche) if ladeflaeche else 0.0  # Standardwert für Ladefläche
                        allrad = allrad.lower() == 'ja'  # Konvertiere Allrad zu einem Boolean

                        # Erstelle das entsprechende Fahrzeugobjekt
                        if typ in Mietwagenfirma.class_names:
                            fahrzeug_class = Mietwagenfirma.class_names[typ]
                            if typ == "PKW":
                                fahrzeug = fahrzeug_class(marke, modell, baujahr, float(mietpreis_pro_tag),
                                                          float(mietpreis_pro_stunde), sitzplaetze)
                            elif typ == "Bus":
                                fahrzeug = fahrzeug_class(marke, modell, baujahr, float(mietpreis_pro_tag),
                                                          float(mietpreis_pro_stunde), sitzplaetze)
                            elif typ == "Transporter":
                                fahrzeug = fahrzeug_class(marke, modell, baujahr, float(mietpreis_pro_tag),
                                                          float(mietpreis_pro_stunde), ladeflaeche)
                            elif typ == "SUV":
                                fahrzeug = fahrzeug_class(marke, modell, baujahr, float(mietpreis_pro_tag),
                                                          float(mietpreis_pro_stunde), allrad)
                            else:
                                print(f"Unbekannter Fahrzeugtyp: {typ}")
                                continue

                            firma.fahrzeug_hinzufuegen(fahrzeug)
                        else:
                            print(f"Unbekannter Fahrzeugtyp: {typ}")
                    except Exception as e:
                        print(f"Fehler beim Verarbeiten einer Fahrzeugzeile: {row}. Fehler: {e}")

        if mietvertraege_csv:
            with open(mietvertraege_csv, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                next(reader)  # Ignoriere die Header-Zeile
                for row in reader:
                    try:
                        if len(row) != 6:
                            print(f"Ungültige Zeile in der Mietvertrags-CSV-Datei: {row}")
                            continue
                        kunden_name, fahrzeug_marke, fahrzeug_modell, mietbeginn_str, mietende_str, gesamtpreis = row
                        kunde = firma.find_kunde_by_name(kunden_name)
                        fahrzeug = firma.find_fahrzeug_by_marke_modell(fahrzeug_marke, fahrzeug_modell)
                        anfangsdatum = datetime.strptime(mietbeginn_str, "%d.%m.%Y %H:%M")
                        enddatum = datetime.strptime(mietende_str, "%d.%m.%Y %H:%M")
                        gesamtpreis = float(gesamtpreis)
                        mietvertrag = Mietvertrag(kunde, fahrzeug, anfangsdatum, enddatum, gesamtpreis)
                        firma.mietvertrag_hinzufuegen(mietvertrag)
                    except Exception as e:
                        print(f"Fehler beim Verarbeiten einer Mietvertragszeile: {row}. Fehler: {e}")

        messagebox.showinfo("Erfolg", "Daten wurden erfolgreich geladen.")
    except Exception as e:
        messagebox.showerror("Fehler", f"Es gab ein Problem beim Laden der Daten: {e}")

# Funktion zum Speichern der Mietverträge in eine CSV-Datei
def save_data_to_csv():
    try:
        if mietvertraege_csv:
            with open(mietvertraege_csv, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow(["Kunde", "Fahrzeug", "Anfangsdatum", "Enddatum", "Gesamtpreis"])  # Header-Zeile
                for mietvertrag in firma.mietvertraege:
                    writer.writerow([mietvertrag.kunde.name, mietvertrag.fahrzeug.marke, mietvertrag.fahrzeug.modell,
                                     mietvertrag.anfangsdatum.strftime("%d.%m.%Y %H:%M"),
                                     mietvertrag.enddatum.strftime("%d.%m.%Y %H:%M"), mietvertrag.gesamtpreis])

        if kunden_csv:
            with open(kunden_csv, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow(["Name", "Adresse", "Telefonnummer", "Email"])  # Header-Zeile
                for kunde in firma.kunden:
                    writer.writerow([kunde.name, kunde.adresse, kunde.telefonnummer, kunde.email])

        if fahrzeuge_csv:
            with open(fahrzeuge_csv, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow(["Typ", "Marke", "Modell", "Baujahr", "Mietpreis pro Tag", "Mietpreis pro Stunde", "Sitzplätze", "Ladefläche", "Allrad"])  # Header-Zeile
                for fahrzeug in firma.fahrzeuge:
                    if isinstance(fahrzeug, PKW):
                        writer.writerow(["PKW", fahrzeug.marke, fahrzeug.modell, fahrzeug.baujahr, fahrzeug.mietpreis_pro_tag,
                                         fahrzeug.mietpreis_pro_stunde, fahrzeug.sitzplaetze, "", ""])
                    elif isinstance(fahrzeug, Bus):
                        writer.writerow(["Bus", fahrzeug.marke, fahrzeug.modell, fahrzeug.baujahr, fahrzeug.mietpreis_pro_tag,
                                         fahrzeug.mietpreis_pro_stunde, fahrzeug.sitzplaetze, "", ""])
                    elif isinstance(fahrzeug, Transporter):
                        writer.writerow(["Transporter", fahrzeug.marke, fahrzeug.modell, fahrzeug.baujahr, fahrzeug.mietpreis_pro_tag,
                                         fahrzeug.mietpreis_pro_stunde, "", fahrzeug.ladeflaeche, ""])
                    elif isinstance(fahrzeug, SUV):
                        writer.writerow(["SUV", fahrzeug.marke, fahrzeug.modell, fahrzeug.baujahr, fahrzeug.mietpreis_pro_tag,
                                         fahrzeug.mietpreis_pro_stunde, "", "", fahrzeug.allrad])

        messagebox.showinfo("Erfolg", "Daten wurden erfolgreich gespeichert.")
    except Exception as e:
        messagebox.showerror("Fehler", f"Es gab ein Problem beim Speichern der Daten: {e}")


# Funktion zum Hinzufügen eines Kunden
def kunde_hinzufuegen():
    top = tk.Toplevel()
    top.title("Kunde hinzufügen")
    top.grab_set()

    def save_customer():
        name = entry_name.get().strip().capitalize()
        adresse = entry_adresse.get().strip().capitalize()
        telefonnummer = entry_telefonnummer.get().strip()
        email = entry_email.get().strip()

        try:
            telefonnummer = validate_telefonnummer(telefonnummer)
            validate_name(name)
            validate_email(email)
            kunde = Kunde(name, adresse, telefonnummer, email)
            firma.kunde_hinzufuegen(kunde)

            messagebox.showinfo("Erfolg", f"Kunde '{name}' wurde hinzugefügt.")
            top.destroy()
        except ValueError as ve:
            messagebox.showerror("Fehler", str(ve))

    label_name = tk.Label(top, text="Name:")
    label_name.grid(row=0, column=0, padx=10, pady=10)
    entry_name = tk.Entry(top)
    entry_name.grid(row=0, column=1, padx=10, pady=10)

    label_adresse = tk.Label(top, text="Adresse:")
    label_adresse.grid(row=1, column=0, padx=10, pady=10) # Platzierung
    entry_adresse = tk.Entry(top)
    entry_adresse.grid(row=1, column=1, padx=10, pady=10)

    label_telefonnummer = tk.Label(top, text="Telefonnummer:")
    label_telefonnummer.grid(row=2, column=0, padx=10, pady=10)
    entry_telefonnummer = tk.Entry(top)
    entry_telefonnummer.grid(row=2, column=1, padx=10, pady=10)

    label_email = tk.Label(top, text="Email:")
    label_email.grid(row=3, column=0, padx=10, pady=10)
    entry_email = tk.Entry(top)
    entry_email.grid(row=3, column=1, padx=10, pady=10)

    btn_save = tk.Button(top, text="Speichern", command=save_customer)
    btn_save.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")


# Funktion zum Entfernen eines Kunden
def kunde_entfernen():
    top = tk.Toplevel()
    top.title("Kunde entfernen")
    top.grab_set()

    def remove_customer():
        selected = listbox_kunden.curselection()
        if selected:
            index = selected[0]
            kunde = firma.kunden[index]
            firma.kunden.remove(kunde)
            save_data_to_csv()  # Kunden in CSV speichern
            messagebox.showinfo("Erfolg", f"Kunde '{kunde.name}' wurde entfernt.")
            top.destroy()
        else:
            messagebox.showerror("Fehler", "Bitte wählen Sie einen Kunden aus der Liste aus.")

    listbox_kunden = tk.Listbox(top, selectmode=tk.SINGLE)
    listbox_kunden.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    for kunde in firma.kunden:
        listbox_kunden.insert(tk.END, f"{kunde.name} ({kunde.adresse}, {kunde.telefonnummer}, {kunde.email})")

    btn_remove = tk.Button(top, text="Entfernen", command=remove_customer)
    btn_remove.pack(padx=10, pady=10)


# Funktion zum Anzeigen aller Kunden
def alle_kunden_anzeigen():
    top = tk.Toplevel()
    top.title("Alle Kunden anzeigen")
    top.grab_set()

    text = tk.Text(top, wrap=tk.WORD)
    text.pack(padx=10, pady=10)

    for kunde in firma.kunden:
        text.insert(tk.END, f"{kunde}\n")
    text.config(state=tk.DISABLED)


# Funktion zum Hinzufügen eines Fahrzeugs
def fahrzeug_hinzufuegen():
    # Erstellen eines neuen Fensters, das über dem Hauptfenster angezeigt wird
    top = tk.Toplevel()
    top.title("Fahrzeug hinzufügen")
    top.grab_set()

    # Funktion zum Speichern des neuen Fahrzeugs
    def save_vehicle():
        # Erfassung der Benutzereingaben aus den Eingabefeldern und der Dropdown-Liste
        typ = combobox_typ.get()
        marke = entry_marke.get().strip().capitalize()  # Entfernt führende und nachgestellte Leerzeichen, und formatiert die Eingabe
        modell = entry_modell.get().strip().capitalize()
        baujahr = entry_baujahr.get().strip()
        mietpreis_pro_tag = entry_mietpreis_tag.get().strip()
        mietpreis_pro_stunde = entry_mietpreis_stunde.get().strip()

        try:
            # Validierung der Eingaben für das Baujahr und die Mietpreise
            baujahr = validate_baujahr(baujahr)
            mietpreis_pro_tag = validate_mietpreis(mietpreis_pro_tag)
            mietpreis_pro_stunde = validate_mietpreis(mietpreis_pro_stunde)

            # Je nach Fahrzeugtyp unterschiedliche Attribute hinzufügen
            if typ == "PKW":
                # Erstellen eines PKW-Objekts mit den eingegebenen Werten und einer festen Sitzanzahl von 5
                fahrzeug = PKW(marke, modell, baujahr, mietpreis_pro_tag, mietpreis_pro_stunde, 5)
            elif typ == "Bus":
                # Erfassung und Validierung der Anzahl der Sitzplätze
                sitzplaetze = entry_sitzplaetze.get().strip()
                sitzplaetze = validate_sitzplaetze(sitzplaetze)
                # Erstellen eines Bus-Objekts
                fahrzeug = Bus(marke, modell, baujahr, mietpreis_pro_tag, mietpreis_pro_stunde, sitzplaetze)
            elif typ == "Transporter":
                # Erfassung und Validierung der Ladefläche
                ladeflaeche = entry_ladeflaeche.get().strip()
                ladeflaeche = validate_ladeflaeche(ladeflaeche)
                # Erstellen eines Transporter-Objekts
                fahrzeug = Transporter(marke, modell, baujahr, mietpreis_pro_tag, mietpreis_pro_stunde, ladeflaeche)
            elif typ == "SUV":
                # Erfassung des Allradantriebs als boolescher Wert
                allrad = var_allrad.get()
                # Erstellen eines SUV-Objekts
                fahrzeug = SUV(marke, modell, baujahr, mietpreis_pro_tag, mietpreis_pro_stunde, allrad)
            else:
                # Fehler, falls ein ungültiger Fahrzeugtyp ausgewählt wurde
                raise ValueError("Bitte wählen Sie einen Fahrzeugtyp aus.")

            # Hinzufügen des neuen Fahrzeugs
            firma.fahrzeug_hinzufuegen(fahrzeug)
            # Speichern der aktuellen Fahrzeugflotte in einer CSV-Datei
            save_data_to_csv()
            # Anzeige einer Erfolgsmeldung an den Benutzer
            messagebox.showinfo("Erfolg", f"Fahrzeug '{marke} {modell}' wurde hinzugefügt.")
            # Schließen des Fensters "Fahrzeug hinzufügen"
            top.destroy()
        except ValueError as ve:
            # Anzeige einer Fehlermeldung, falls eine ValueError auftritt (z.B. ungültige Eingaben)
            messagebox.showerror("Fehler", str(ve))

    def update_fields(event):
        # Diese Funktion wird aufgerufen, wenn der Fahrzeugtyp in der Combobox geändert wird.
        typ = combobox_typ.get()  # Holt den aktuell ausgewählten Fahrzeugtyp aus der Combobox
        if typ == "PKW":
            hide_all_fields()  # Versteckt alle spezifischen Eingabefelder, da PKW keine zusätzlichen Felder benötigt
        elif typ == "Bus":
            hide_all_fields()  # Versteckt alle spezifischen Eingabefelder
            # Zeigt die Eingabefelder für die Sitzplätze an, da Busse diese Information benötigen
            label_sitzplaetze.grid(row=5, column=0, padx=10, pady=10)
            entry_sitzplaetze.grid(row=5, column=1, padx=10, pady=10)
        elif typ == "Transporter":
            hide_all_fields()  # Versteckt alle spezifischen Eingabefelder
            # Zeigt die Eingabefelder für die Ladefläche an, da Transporter diese Information benötigen
            label_ladeflaeche.grid(row=5, column=0, padx=10, pady=10)
            entry_ladeflaeche.grid(row=5, column=1, padx=10, pady=10)
        elif typ == "SUV":
            hide_all_fields()  # Versteckt alle spezifischen Eingabefelder
            # Zeigt die Eingabefelder für den Allradantrieb an, da SUVs diese Information benötigen
            label_allrad.grid(row=5, column=0, padx=10, pady=10)
            checkbox_allrad.grid(row=5, column=1, padx=10, pady=10)

    def hide_all_fields():
        # Diese Funktion versteckt alle spezifischen Eingabefelder, um sicherzustellen, dass nur die relevanten Felder angezeigt werden.
        label_sitzplaetze.grid_remove()
        entry_sitzplaetze.grid_remove()
        label_ladeflaeche.grid_remove()
        entry_ladeflaeche.grid_remove()
        label_allrad.grid_remove()
        checkbox_allrad.grid_remove()



    # Label und Combobox für die Auswahl des Fahrzeugtyps
    label_typ = tk.Label(top, text="Fahrzeugtyp:")
    label_typ.grid(row=0, column=0, padx=10, pady=10)
    combobox_typ = ttk.Combobox(top, values=["PKW", "Bus", "Transporter", "SUV"])
    combobox_typ.grid(row=0, column=1, padx=10, pady=10)
    combobox_typ.bind("<<ComboboxSelected>>",
                      update_fields)  # Bindet die Funktion update_fields an die Auswahländerung der Combobox

    # Label und Eingabefeld für die Marke des Fahrzeugs
    label_marke = tk.Label(top, text="Marke:")
    label_marke.grid(row=1, column=0, padx=10, pady=10)
    entry_marke = tk.Entry(top)
    entry_marke.grid(row=1, column=1, padx=10, pady=10)

    # Label und Eingabefeld für das Modell des Fahrzeugs
    label_modell = tk.Label(top, text="Modell:")
    label_modell.grid(row=2, column=0, padx=10, pady=10)
    entry_modell = tk.Entry(top)
    entry_modell.grid(row=2, column=1, padx=10, pady=10)

    # Label und Eingabefeld für das Baujahr des Fahrzeugs
    label_baujahr = tk.Label(top, text="Baujahr:")
    label_baujahr.grid(row=3, column=0, padx=10, pady=10)
    entry_baujahr = tk.Entry(top)
    entry_baujahr.grid(row=3, column=1, padx=10, pady=10)

    # Label und Eingabefeld für den Mietpreis pro Tag
    label_mietpreis_tag = tk.Label(top, text="Mietpreis pro Tag:")
    label_mietpreis_tag.grid(row=4, column=0, padx=10, pady=10)
    entry_mietpreis_tag = tk.Entry(top)
    entry_mietpreis_tag.grid(row=4, column=1, padx=10, pady=10)

    # Label und Eingabefeld für den Mietpreis pro Stunde
    label_mietpreis_stunde = tk.Label(top, text="Mietpreis pro Stunde:")
    label_mietpreis_stunde.grid(row=4, column=2, padx=10, pady=10)
    entry_mietpreis_stunde = tk.Entry(top)
    entry_mietpreis_stunde.grid(row=4, column=3, padx=10, pady=10)

    # Spezifische Felder für Busse, Transporter und SUVs, die anfänglich versteckt werden
    label_sitzplaetze = tk.Label(top, text="Sitzplätze:")
    entry_sitzplaetze = tk.Entry(top)

    label_ladeflaeche = tk.Label(top, text="Ladefläche:")
    entry_ladeflaeche = tk.Entry(top)

    label_allrad = tk.Label(top, text="Allradantrieb:")
    var_allrad = tk.BooleanVar()
    checkbox_allrad = tk.Checkbutton(top, variable=var_allrad)

    # Zusätzliche Felder für spezifische Fahrzeugtypen
    label_sitzplaetze = tk.Label(top, text="Sitzplätze:")
    entry_sitzplaetze = tk.Entry(top)

    label_ladeflaeche = tk.Label(top, text="Ladefläche (m²):")
    entry_ladeflaeche = tk.Entry(top)

    label_allrad = tk.Label(top, text="Allradantrieb:")
    var_allrad = tk.BooleanVar()
    checkbox_allrad = tk.Checkbutton(top, variable=var_allrad)

    btn_save = tk.Button(top, text="Speichern", command=save_vehicle)
    btn_save.grid(row=6, column=0, columnspan=4, padx=10, pady=10, sticky="ew")


# Funktion zum Entfernen eines Fahrzeugs
def fahrzeug_entfernen():
    top = tk.Toplevel()
    top.title("Fahrzeug entfernen")
    top.grab_set()

    def remove_vehicle():
        selected = listbox_fahrzeuge.curselection()
        if selected:
            index = selected[0]
            fahrzeug = firma.fahrzeuge[index]
            firma.fahrzeuge.remove(fahrzeug)
            save_data_to_csv()  # Fahrzeuge in CSV speichern
            messagebox.showinfo("Erfolg", f"Fahrzeug '{fahrzeug.marke} {fahrzeug.modell}' wurde entfernt.")
            top.destroy()
        else:
            messagebox.showerror("Fehler", "Bitte wählen Sie ein Fahrzeug aus der Liste aus.")

    listbox_fahrzeuge = tk.Listbox(top, selectmode=tk.SINGLE)
    listbox_fahrzeuge.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    for fahrzeug in firma.fahrzeuge:
        listbox_fahrzeuge.insert(tk.END, f"{fahrzeug.marke} {fahrzeug.modell} ({fahrzeug.baujahr})")

    btn_remove = tk.Button(top, text="Entfernen", command=remove_vehicle)
    btn_remove.pack(padx=10, pady=10)


# Funktion zum Anzeigen aller Fahrzeuge
def alle_fahrzeuge_anzeigen():
    top = tk.Toplevel()
    top.title("Alle Fahrzeuge anzeigen")
    top.grab_set()

    text = tk.Text(top, wrap=tk.WORD)
    text.pack(padx=10, pady=10)

    for fahrzeug in firma.fahrzeuge:
        text.insert(tk.END, f"{fahrzeug}\n")
    text.config(state=tk.DISABLED) # deaktiviert Textwidget


# Funktion zur Berechnung des Mietpreises bei Rückgabe eines Fahrzeugs
def berechne_mietpreis(fahrzeug, mietzeit, stundenpreis=False):
    if stundenpreis:
        return fahrzeug.mietpreis_pro_stunde * mietzeit
    else:
        return fahrzeug.mietpreis_pro_tag * mietzeit.days


# Funktion zur Erstellung einer Rechnung bei Rückgabe eines Fahrzeugs
def erstelle_rechnung(fahrzeug, kunde, mietbeginn, mietende, gesamtpreis):
    rechnungstext = (
        f"=============== Rechnung ===============\n\n"
        f"Rechnungsdatum: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n"
        f"Rechnungsnummer: ABC123\n\n"
        f"===== Fahrzeuginformationen =====\n"
        f"Marke: {fahrzeug.marke}\n"
        f"Modell: {fahrzeug.modell}\n"
        f"Baujahr: {fahrzeug.baujahr}\n\n"
        f"===== Kundeninformationen =====\n"
        f"Name: {kunde.name}\n"
        f"Adresse: {kunde.adresse}\n"
        f"Telefonnummer: {kunde.telefonnummer}\n"
        f"E-Mail: {kunde.email}\n\n"
        f"===== Mietzeit =====\n"
        f"Mietbeginn: {mietbeginn.strftime('%d.%m.%Y %H:%M')}\n"
        f"Mietende: {mietende.strftime('%d.%m.%Y %H:%M')}\n\n"
        f"===== Abrechnung =====\n"
        f"Mietpreis pro Tag: {fahrzeug.mietpreis_pro_tag} Euro\n"
        f"Mietpreis pro Stunde: {fahrzeug.mietpreis_pro_stunde} Euro\n"
        f"Gesamtpreis: {gesamtpreis} Euro\n\n"
        f"=======================================\n"
        f"Vielen Dank für Ihre Buchung!"
    )

    messagebox.showinfo("Rechnung", rechnungstext)

def erstelle_mietvertrag(kunde, fahrzeug, mietbeginn, mietende, gesamtpreis):
    try:
        validate_mietzeit(mietbeginn, mietende)

        mietvertrag = Mietvertrag(kunde, fahrzeug, mietbeginn, mietende, gesamtpreis)
        firma.mietvertrag_hinzufuegen(mietvertrag)  # Mietvertrag zur Firma hinzufügen
        save_data_to_csv()  # Mietverträge in CSV speichern

        messagebox.showinfo("Erfolg", "Mietvertrag erfolgreich erstellt und gespeichert.")
    except ValueError as ve:
        messagebox.showerror("Fehler", str(ve))


def fahrzeug_vermieten():
    top = tk.Toplevel()
    top.title("Fahrzeug vermieten")
    top.grab_set()

    def miete_fahrzeug():
        selected_kunde_idx = combobox_kunden.current()
        selected_fahrzeug_idx = combobox_fahrzeuge.current()

        if selected_kunde_idx >= 0 and selected_fahrzeug_idx >= 0:
            kunde = firma.kunden[selected_kunde_idx]
            fahrzeug = firma.fahrzeuge[selected_fahrzeug_idx]

            mietbeginn_str = entry_mietbeginn.get().strip()
            mietende_str = entry_mietende.get().strip()

            try:
                mietbeginn = datetime.strptime(mietbeginn_str, "%d.%m.%Y %H:%M")
                mietende = datetime.strptime(mietende_str, "%d.%m.%Y %H:%M")
                validate_mietzeit(mietbeginn, mietende)
                # Fahrzeug als vermietet markieren
                if fahrzeug.mieten():
                    gesamtpreis = berechne_mietpreis(fahrzeug, mietende - mietbeginn)
                    erstelle_rechnung(fahrzeug, kunde, mietbeginn, mietende, gesamtpreis)
                    erstelle_mietvertrag(kunde, fahrzeug, mietbeginn, mietende, gesamtpreis)
                    # Mietvertrag zur Firma hinzufügen
                    mietvertrag = Mietvertrag(kunde, fahrzeug, mietbeginn, mietende, gesamtpreis)
                    firma.mietvertrag_hinzufuegen(mietvertrag)


                    messagebox.showinfo("Erfolg", f"Fahrzeug '{fahrzeug.marke} {fahrzeug.modell}' wurde vermietet.")
                    top.destroy()
                else:
                    messagebox.showwarning("Warnung", "Das Fahrzeug ist bereits vermietet.")
            except ValueError as ve:
                messagebox.showerror("Fehler", str(ve))
        else:
            messagebox.showerror("Fehler", "Bitte wählen Sie einen Kunden und ein Fahrzeug aus der Liste aus.")

    # Combobox für Kunden
    combobox_kunden = ttk.Combobox(top)
    combobox_kunden.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    kunden_namen = [f"{kunde.name} ({kunde.adresse}, {kunde.telefonnummer}, {kunde.email})" for kunde in firma.kunden]
    combobox_kunden['values'] = kunden_namen

    # Combobox für Fahrzeuge
    combobox_fahrzeuge = ttk.Combobox(top)
    combobox_fahrzeuge.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    fahrzeuge_namen = [f"{fahrzeug.marke} {fahrzeug.modell}" for fahrzeug in firma.fahrzeuge]
    combobox_fahrzeuge['values'] = fahrzeuge_namen

    # Labels und Einträge für Mietbeginn und Mietende
    label_mietbeginn = tk.Label(top, text="Mietbeginn (dd.mm.yyyy hh:mm):")
    label_mietbeginn.pack(padx=10, pady=10)
    entry_mietbeginn = tk.Entry(top)
    entry_mietbeginn.pack(padx=10, pady=10)

    label_mietende = tk.Label(top, text="Mietende (dd.mm.yyyy hh:mm):")
    label_mietende.pack(padx=10, pady=10)
    entry_mietende = tk.Entry(top)
    entry_mietende.pack(padx=10, pady=10)

    # Button zum Fahrzeugvermieten
    btn_mieten = tk.Button(top, text="Fahrzeug vermieten", command=miete_fahrzeug)
    btn_mieten.pack(padx=10, pady=10)
# Funktion zum Beenden des Programms
def beenden():
    messagebox.showinfo("Hinweis", "Programm wird beendet.")
    root.destroy()


# Hilfsfunktionen für die Validierung
def validate_name(name):
    if not name:
        raise ValueError("Name darf nicht leer sein.")
    if not name.replace(" ", "").isalpha():
        raise ValueError("Ungültiger Name: Nur Buchstaben sind erlaubt.")


def validate_email(email):
    if not email:
        return
    if "@" not in email or "." not in email:
        raise ValueError("Ungültige Email-Adresse.")


def validate_telefonnummer(telefonnummer):
    if not telefonnummer.isdigit() or len(telefonnummer) < 10 or len(telefonnummer) > 12:
        raise ValueError("Ungültige Telefonnummer: Muss aus 10 bis 12 Ziffern bestehen.")
    return telefonnummer


def validate_baujahr(baujahr):
    if not baujahr.isdigit() or len(baujahr) != 4:
        raise ValueError("Ungültiges Baujahr: Muss aus vier Ziffern bestehen.")
    return baujahr


def validate_mietpreis(mietpreis):
    try:
        mietpreis = float(mietpreis)
    except ValueError:
        raise ValueError("Ungültiger Mietpreis: Muss eine Zahl sein.")
    return mietpreis


def validate_sitzplaetze(sitzplaetze):
    if not sitzplaetze.isdigit() or int(sitzplaetze) <= 0:
        raise ValueError("Ungültige Anzahl der Sitzplätze: Muss eine positive Zahl sein.")
    return int(sitzplaetze)


def validate_ladeflaeche(ladeflaeche):
    try:
        ladeflaeche = float(ladeflaeche)
        if ladeflaeche <= 0:
            raise ValueError()
    except ValueError:
        raise ValueError("Ungültige Ladefläche: Muss eine positive Zahl sein.")
    return ladeflaeche


def validate_mietzeit(mietbeginn, mietende):
    # Überprüfen, ob das Mietende nach dem Mietbeginn liegt
    if mietende <= mietbeginn:
        raise ValueError("Das Mietende muss nach dem Mietbeginn liegen.")



def load_fahrzeuge_from_csv():
    try:
        with open("fahrzeuge.csv", "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                typ, marke, modell, baujahr, mietpreis_pro_tag, mietpreis_pro_stunde, details = row
                if typ == "PKW":
                    fahrzeug = PKW(marke, modell, baujahr, float(mietpreis_pro_tag), float(mietpreis_pro_stunde), 5)
                elif typ == "Bus":
                    fahrzeug = Bus(marke, modell, baujahr, float(mietpreis_pro_tag), float(mietpreis_pro_stunde),
                                   int(details))
                elif typ == "Transporter":
                    fahrzeug = Transporter(marke, modell, baujahr, float(mietpreis_pro_tag),
                                           float(mietpreis_pro_stunde), float(details))
                elif typ == "SUV":
                    fahrzeug = SUV(marke, modell, baujahr, float(mietpreis_pro_tag), float(mietpreis_pro_stunde),
                                   bool(details))
                else:
                    raise ValueError("Ungültiger Fahrzeugtyp beim Laden.")
                firma.fahrzeuge.append(fahrzeug)
    except FileNotFoundError:
        pass  # Wenn die Datei nicht gefunden wird, wird sie beim Laden erstellt



# GUI erstellen
root = tk.Tk()
root.title("Mietwagenverwaltungsprogramm")

# Willkommensnachricht
current_date = datetime.now().strftime("%d.%m.%Y")
welcome_label = tk.Label(root, text=f"Willkommen zum Mietwagenverwaltungsprogramm!\nHeute ist der {current_date}",
                         padx=20, pady=20, font=("Helvetica", 14, "bold"), bg="#4CAF50", fg="white")
welcome_label.pack(fill=tk.X)

# Hauptmenü
menu_frame = tk.Frame(root, bg="#f0f0f0")
menu_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

# Buttons für die Menüoptionen
buttons = [
    ("Kunden hinzufügen", kunde_hinzufuegen),
    ("Kunden entfernen", kunde_entfernen),
    ("Alle Kunden anzeigen", alle_kunden_anzeigen),
    ("Fahrzeug vermieten", fahrzeug_vermieten),
    ("Fahrzeug hinzufügen", fahrzeug_hinzufuegen),
    ("Fahrzeug entfernen", fahrzeug_entfernen),
    ("Alle Fahrzeuge anzeigen", alle_fahrzeuge_anzeigen),
    ("Daten speichern", save_data_to_csv),
    ("Daten laden", load_data_from_csv),
    ("Programm beenden", beenden)
]
# Startwert für Zeilen und Spaltennummer
row_num = 0
col_num = 0
for btn_text, btn_command in buttons:
    button = tk.Button(menu_frame, text=btn_text, command=btn_command, width=20, height=2,
                       font=("Helvetica", 12), bg="#2196F3", fg="white", relief="raised", bd=3) #relief = Darstellung des Rahmens um den Button
    button.grid(row=row_num, column=col_num, padx=10, pady=10)
    # sorgt dafür, dass zwei Buttons pro Zeile platziert werden
    col_num += 1
    if col_num > 1:
        col_num = 0
        row_num += 1



# Loop für die GUI
root.mainloop()