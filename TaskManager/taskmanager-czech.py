import datetime
import json
import os
from typing import List, Dict, Optional, Any


class Ukol:
    def __init__(self, nazev: str, popis: str = "", priorita: int = 1, 
                termin: Optional[datetime.datetime] = None, dokonceno: bool = False):
        self.id = None  # ID bude přiřazeno při uložení
        self.nazev = nazev
        self.popis = popis
        self.priorita = priorita  # 1-5, kde 5 je nejvyšší
        self.termin = termin
        self.dokonceno = dokonceno
        self.vytvoreno = datetime.datetime.now()
        
    def do_slovniku(self) -> Dict[str, Any]:
        """Převede úkol na slovník pro serializaci"""
        return {
            'id': self.id,
            'nazev': self.nazev,
            'popis': self.popis,
            'priorita': self.priorita,
            'termin': self.termin.isoformat() if self.termin else None,
            'dokonceno': self.dokonceno,
            'vytvoreno': self.vytvoreno.isoformat()
        }
    
    @classmethod
    def ze_slovniku(cls, data: Dict[str, Any]) -> 'Ukol':
        """Vytvoří úkol ze slovníku"""
        ukol = cls(
            nazev=data['nazev'],
            popis=data.get('popis', ''),
            priorita=data.get('priorita', 1),
            dokonceno=data.get('dokonceno', False)
        )
        
        if data.get('termin'):
            ukol.termin = datetime.datetime.fromisoformat(data['termin'])
        
        ukol.id = data.get('id')
        ukol.vytvoreno = datetime.datetime.fromisoformat(data['vytvoreno'])
        return ukol
    
    def dokoncit(self):
        """Označí úkol jako dokončený"""
        self.dokonceno = True


class SpravceUkolu:
    def __init__(self, cesta_uloziste: str = "ukoly.json"):
        self.cesta_uloziste = cesta_uloziste
        self.ukoly = []
        self.dalsi_id = 1
        self.nacist_ukoly()
    
    def pridat_ukol(self, ukol: Ukol) -> Ukol:
        """Přidá nový úkol a přiřadí mu ID"""
        ukol.id = self.dalsi_id
        self.dalsi_id += 1
        self.ukoly.append(ukol)
        self.ulozit_ukoly()
        return ukol
    
    def ziskat_ukol(self, id_ukolu: int) -> Optional[Ukol]:
        """Najde úkol podle ID"""
        for ukol in self.ukoly:
            if ukol.id == id_ukolu:
                return ukol
        return None
    
    def aktualizovat_ukol(self, id_ukolu: int, **kwargs) -> Optional[Ukol]:
        """Aktualizuje úkol podle ID"""
        ukol = self.ziskat_ukol(id_ukolu)
        if not ukol:
            return None
        
        # Aktualizace atributů
        for klic, hodnota in kwargs.items():
            if hasattr(ukol, klic):
                setattr(ukol, klic, hodnota)
        
        self.ulozit_ukoly()
        return ukol
    
    def smazat_ukol(self, id_ukolu: int) -> bool:
        """Smaže úkol podle ID"""
        ukol = self.ziskat_ukol(id_ukolu)
        if not ukol:
            return False
        
        self.ukoly.remove(ukol)
        self.ulozit_ukoly()
        return True
    
    def ziskat_vsechny_ukoly(self) -> List[Ukol]:
        """Vrátí všechny úkoly"""
        return self.ukoly
    
    def ziskat_nedokoncene_ukoly(self) -> List[Ukol]:
        """Vrátí nedokončené úkoly"""
        return [ukol for ukol in self.ukoly if not ukol.dokonceno]
    
    def ziskat_proslé_ukoly(self) -> List[Ukol]:
        """Vrátí úkoly po termínu"""
        nyni = datetime.datetime.now()
        return [
            ukol for ukol in self.ukoly 
            if ukol.termin and ukol.termin < nyni and not ukol.dokonceno
        ]
    
    def ulozit_ukoly(self) -> None:
        """Uloží úkoly do souboru"""
        data = {
            'dalsi_id': self.dalsi_id,
            'ukoly': [ukol.do_slovniku() for ukol in self.ukoly]
        }
        
        with open(self.cesta_uloziste, 'w') as f:
            json.dump(data, f, indent=2)
    
    def nacist_ukoly(self) -> None:
        """Načte úkoly ze souboru"""
        if not os.path.exists(self.cesta_uloziste):
            self.ukoly = []
            self.dalsi_id = 1
            return
        
        try:
            with open(self.cesta_uloziste, 'r') as f:
                data = json.load(f)
                
            self.dalsi_id = data.get('dalsi_id', 1)
            self.ukoly = [Ukol.ze_slovniku(data_ukolu) for data_ukolu in data.get('ukoly', [])]
        except json.JSONDecodeError:
            # Pokud je soubor poškozen, začneme s prázdným seznamem
            self.ukoly = []
            self.dalsi_id = 1
    
    def vyhledat_ukoly(self, dotaz: str) -> List[Ukol]:
        """Vyhledá úkoly podle textu v názvu nebo popisu"""
        dotaz = dotaz.lower()
        vysledky = []
        for ukol in self.ukoly:
            if dotaz in ukol.nazev.lower() or (ukol.popis and dotaz in ukol.popis.lower()):
                vysledky.append(ukol)
        return vysledky


# Ukázka použití
if __name__ == "__main__":
    # Vytvoříme správce úkolů
    spravce = SpravceUkolu()
    
    # Přidáme nějaké úkoly
    ukol1 = Ukol("Dokončit seminární práci", "Kapitoly State-of-the-art, Návrh experimentu", 5, 
                datetime.datetime(2025, 5, 30))
    ukol2 = Ukol("Nakoupit potraviny", "Chleba, mléko, vejce", 3)
    
    spravce.pridat_ukol(ukol1)
    spravce.pridat_ukol(ukol2)
    
    # Vypíšeme všechny úkoly
    for ukol in spravce.ziskat_vsechny_ukoly():
        print(f"{ukol.id}: {ukol.nazev} (Priorita: {ukol.priorita})")
        if ukol.termin:
            print(f"  Termín: {ukol.termin.strftime('%d.%m.%Y')}")
