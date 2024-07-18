class Fahrzeug:    def __init__(self, marke, modell, baujahr, mietpreis_pro_tag, mietpreis_pro_stunde):        self.marke = marke        self.modell = modell        self.baujahr = baujahr        self.mietpreis_pro_tag = mietpreis_pro_tag        self.mietpreis_pro_stunde = mietpreis_pro_stunde        self.verfuegbar = True  # Fahrzeug ist anfangs verfügbar    def __str__(self):        return f"Marke: {self.marke}\nModell: {self.modell}\nBaujahr: {self.baujahr}\nMietpreis pro Tag: {self.mietpreis_pro_tag}€\nMietpreis pro Stunde: {self.mietpreis_pro_stunde}€\n"    def mieten(self):        if self.verfuegbar:            self.verfuegbar = False  # Fahrzeug wird als vermietet markiert            return True        return False    def zurueckgeben(self):        self.verfuegbar = True  # Fahrzeug wird als verfügbar markiert# PKW Klasse, die von Fahrzeug erbtclass PKW(Fahrzeug):    def __init__(self, marke, modell, baujahr, mietpreis_pro_tag, mietpreis_pro_stunde, sitzplaetze):        super().__init__(marke, modell, baujahr, mietpreis_pro_tag, mietpreis_pro_stunde)        self.sitzplaetze = sitzplaetze    def __str__(self):        return super().__str__() + f"Sitzplätze: {self.sitzplaetze}\n"# SUV Klasse, die von Fahrzeug erbtclass SUV(Fahrzeug):    def __init__(self, marke, modell, baujahr, mietpreis_pro_tag, mietpreis_pro_stunde, allrad):        super().__init__(marke, modell, baujahr, mietpreis_pro_tag, mietpreis_pro_stunde)        self.allrad = allrad    def __str__(self):        return super().__str__() + f"Allrad: {'Ja' if self.allrad else 'Nein'}\n"# Transporter Klasse, die von Fahrzeug erbtclass Transporter(Fahrzeug):    def __init__(self, marke, modell, baujahr, mietpreis_pro_tag, mietpreis_pro_stunde, ladeflaeche):        super().__init__(marke, modell, baujahr, mietpreis_pro_tag, mietpreis_pro_stunde)        self.ladeflaeche = ladeflaeche    def __str__(self):        return super().__str__() + f"Ladefläche: {self.ladeflaeche} m³\n"# Bus Klasse, die von Fahrzeug erbtclass Bus(Fahrzeug):    def __init__(self, marke, modell, baujahr, mietpreis_pro_tag, mietpreis_pro_stunde, sitzplaetze):        super().__init__(marke, modell, baujahr, mietpreis_pro_tag, mietpreis_pro_stunde)        self.sitzplaetze = sitzplaetze    def __str__(self):        return super().__str__() + f"Sitzplätze: {self.sitzplaetze}\n"# Kunde Klasseclass Kunde:    def __init__(self, name, adresse, telefonnummer, email):        self.name = name        self.adresse = adresse        self.telefonnummer = telefonnummer        self.email = email    def __str__(self):        return f"Name: {self.name}\nAdresse: {self.adresse}\nTelefonnummer: {self.telefonnummer}\nEmail: {self.email}\n"# Mietvertrag Klasseclass Mietvertrag:    def __init__(self, kunde, fahrzeug, anfangsdatum, enddatum, gesamtpreis=0):        self.kunde = kunde        self.fahrzeug = fahrzeug        self.anfangsdatum = anfangsdatum        self.enddatum = enddatum        self.gesamtpreis = gesamtpreis        self.gesamtpreis_ausrechnen()  # Berechne den Gesamtpreis beim Initialisieren    def __str__(self):        return f"Kunde: {self.kunde.name}\nFahrzeug: {self.fahrzeug.marke} {self.fahrzeug.modell}\nMietbeginn: {self.anfangsdatum}\nMietende: {self.enddatum}\n{self.gesamtpreis:.2f}€\n"    def gesamtpreis_ausrechnen(self):        # Annahme: Mietpreis pro Tag und pro Stunde werden verwendet        mietpreis_pro_tag = self.fahrzeug.mietpreis_pro_tag        mietpreis_pro_stunde = self.fahrzeug.mietpreis_pro_stunde        # Berechnung der Mietdauer in Stunden        delta = self.enddatum - self.anfangsdatum        mietdauer_in_stunden = delta.total_seconds() / 3600        # Berechnung des Gesamtpreises        gesamtpreis_tag = mietdauer_in_stunden / 24 * mietpreis_pro_tag        gesamtpreis_stunde = mietdauer_in_stunden * mietpreis_pro_stunde        self.gesamtpreis = gesamtpreis_tag + gesamtpreis_stunde        return self.gesamtpreis# Mietwagenfirma Klasseclass Mietwagenfirma:    def __init__(self, name):        self.name = name        self.kunden = []        self.mietvertraege = []        self.fahrzeuge = []    def kunde_hinzufuegen(self, kunde):        self.kunden.append(kunde)  # Kunde wird der Liste hinzugefügt    def alle_kunden_anzeigen(self):        for kunde in self.kunden:            print(kunde)    def mietvertrag_anzeigen(self):        for mietvertrag in self.mietvertraege:            print(mietvertrag)    def fahrzeug_hinzufuegen(self, fahrzeug):        self.fahrzeuge.append(fahrzeug)  # Fahrzeug wird der Liste hinzugefügt    def verfuegbare_fahrzeuge(self):        for fahrzeug in self.fahrzeuge:            if fahrzeug.verfuegbar:                print(fahrzeug)    def alle_fahrzeuge_anzeigen(self):        for fahrzeug in self.fahrzeuge:            print(fahrzeug)    def alle_mietvertraege_anzeigen(self):        for mietvertrag in self.mietvertraege:            print(mietvertrag)    def fahrzeug_mieten(self, marke, modell, kundenname, anfangsdatum, enddatum):        kunde = self.find_kunde_by_name(kundenname)        if kunde is None:            print(f"Kunde '{kundenname}' nicht gefunden.")            return None        fahrzeug = self.find_fahrzeug_by_marke_modell(marke, modell)        if fahrzeug is None:            print(f"Fahrzeug '{marke} {modell}' nicht gefunden.")            return None        mietvertrag = Mietvertrag(kunde, fahrzeug, anfangsdatum, enddatum, 0)  # Gesamtpreis wird später berechnet oder gesetzt        self.mietvertrag_hinzufuegen(mietvertrag)        fahrzeug.mieten()  # Markiere das Fahrzeug als vermietet        return mietvertrag    def find_fahrzeug_by_marke_modell(self, fahrzeug_marke, fahrzeug_modell):        for fahrzeug in self.fahrzeuge:            if fahrzeug.marke == fahrzeug_marke and fahrzeug.modell == fahrzeug_modell:                return fahrzeug        return None  # Rückgabe von None, wenn das Fahrzeug nicht gefunden wurde    def mietvertrag_hinzufuegen(self, mietvertrag):        self.mietvertraege.append(mietvertrag)    def find_kunde_by_name(self, kunden_name):        for kunde in self.kunden:            if kunde.name == kunden_name:                return kunde        return None  # Rückgabe von None, wenn der Kunde nicht gefunden wurde    # Zuordnung der Fahrzeugtypen zu den entsprechenden Klassen    class_names = {        'PKW': PKW,        'Bus': Bus,        'Transporter': Transporter,        'SUV': SUV    }