import json
from datetime import datetime

class Kulu:
    def __init__(self, maara, kategoria, paivamaara):
        # alustetaan kulu maaralla, kategorialla ja paivamaaralla
        self.maara = maara
        self.kategoria = kategoria
        self.paivamaara = datetime.strptime(paivamaara, "%d-%m-%Y").date()

class MenojenSeuranta:
    def __init__(self):
        self.kulut = []
        self.lataa_kulut() # Ladataan aiemmin tallennetut kulut tiedostosta

    def lisaa_kulu(self, maara, kategoria, paivamaara):
        # Lisaa uuden kulun listaan ja tallentaa sen tiedostoon
        kulu = Kulu(maara, kategoria, paivamaara) 
        self.kulut.append(kulu)
        self.tallenna_kulut()

    def nayta_kulut(self, alkupaivamaara, loppupaivamaara):
        # Nayttaa kaikki kulut valitulla aikavalil
        alku = datetime.strptime(alkupaivamaara, "%d-%m-%Y").date()
        loppu = datetime.strptime(loppupaivamaara, "%d-%m-%Y").date()
        for kulu in self.kulut:
            if alku <= kulu.paivamaara <= loppu:
                print(f"{kulu.paivamaara.strftime('%d-%m-%Y')} - {kulu.kategoria}: €{kulu.maara}")

    def yhteenveto(self, alkupaivamaara, loppupaivamaara):
        # Laskee ja nayttaa kulujen yhteenvedon valitulla aikavalilla
        alku = datetime.strptime(alkupaivamaara, "%d-%m-%Y").date()
        loppu = datetime.strptime(loppupaivamaara, "%d-%m-%Y").date()
        yhteenveto = {}
        for kulu in self.kulut:
            if alku <= kulu.paivamaara <= loppu:
                yhteenveto[kulu.kategoria] = yhteenveto.get(kulu.kategoria, 0) + kulu.maara
        for kategoria, yhteensa in yhteenveto.items():
            print(f"{kategoria}: €{yhteensa}")

    def tallenna_kulut(self):
        # tallentaa kulut JSON-tiedostoon
        with open("kulut.json", "w") as tiedosto:
            json.dump([{"maara": kulu.maara, "kategoria": kulu.kategoria, "paivamaara": kulu.paivamaara.strftime("%d-%m-%Y")} for kulu in self.kulut], tiedosto)

    def lataa_kulut(self):
        # Lataa kulut tiedostosta jos tiedosto on olemassa
        try:
            with open("kulut.json", "r") as tiedosto:
                data = json.load(tiedosto)
                self.kulut = [Kulu(kulu['maara'], kulu['kategoria'], kulu['paivamaara']) for kulu in data]
        except FileNotFoundError:
            pass

def main():
    seuranta = MenojenSeuranta()

    while True:
        print("\nMenot Seuranta")
        print("1. Lisaa Kulu")
        print("2. Nayta Kulut")
        print("3. Yhteenveto")
        print("4. Poistu")

        valinta = input("Anna valinta: ")

        if valinta == '1':
            # Lisataan uusi kulu
            maara = float(input("Anna summa (€): "))
            kategoria = input("Anna kategoria: ")
            paivamaara = input("Anna paivamaara (PP-KK-VVVV): ")
            seuranta.lisaa_kulu(maara, kategoria, paivamaara)
        elif valinta == '2':
            # Naytetaan kulut valitulla aikavalilla
            alkupaivamaara = input("Anna alkupaivamaara (PP-KK-VVVV): ")
            loppupaivamaara = input("Anna loppupaivamaara (PP-KK-VVVV): ")
            seuranta.nayta_kulut(alkupaivamaara, loppupaivamaara)
        elif valinta == '3':
            # Naytetaan kulujen yhteenveto valitulla ajalla
            alkupaivamaara = input("Anna alkupaivamaara (PP-KK-VVVV): ")
            loppupaivamaara = input("Anna loppupaivamaara (PP-KK-VVVV): ")
            seuranta.yhteenveto(alkupaivamaara, loppupaivamaara)
        elif valinta == '4':
            # Poistutaan ohjelmasta
            break
        else:
            print("Virheellinen valinta.")

if __name__ == "__main__":
    main()
