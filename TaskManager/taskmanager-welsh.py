import datetime
import json
import os
from typing import List, Dict, Optional, Any


class Tasg:
    def __init__(self, teitl: str, disgrifiad: str = "", blaenoriaeth: int = 1, 
                dyddiad_dyledus: Optional[datetime.datetime] = None, cwblhawyd: bool = False):
        self.id = None  # Bydd ID yn cael ei neilltuo pan gaiff ei gadw
        self.teitl = teitl
        self.disgrifiad = disgrifiad
        self.blaenoriaeth = blaenoriaeth  # 1-5, lle mae 5 yn uchaf
        self.dyddiad_dyledus = dyddiad_dyledus
        self.cwblhawyd = cwblhawyd
        self.crëwyd_ar = datetime.datetime.now()
        
    def i_geiriadur(self) -> Dict[str, Any]:
        """Trosi tasg i eiriadur ar gyfer cyfresoli"""
        return {
            'id': self.id,
            'teitl': self.teitl,
            'disgrifiad': self.disgrifiad,
            'blaenoriaeth': self.blaenoriaeth,
            'dyddiad_dyledus': self.dyddiad_dyledus.isoformat() if self.dyddiad_dyledus else None,
            'cwblhawyd': self.cwblhawyd,
            'crëwyd_ar': self.crëwyd_ar.isoformat()
        }
    
    @classmethod
    def o_geiriadur(cls, data: Dict[str, Any]) -> 'Tasg':
        """Creu tasg o eiriadur"""
        tasg = cls(
            teitl=data['teitl'],
            disgrifiad=data.get('disgrifiad', ''),
            blaenoriaeth=data.get('blaenoriaeth', 1),
            cwblhawyd=data.get('cwblhawyd', False)
        )
        
        if data.get('dyddiad_dyledus'):
            tasg.dyddiad_dyledus = datetime.datetime.fromisoformat(data['dyddiad_dyledus'])
        
        tasg.id = data.get('id')
        tasg.crëwyd_ar = datetime.datetime.fromisoformat(data['crëwyd_ar'])
        return tasg
    
    def cwblhau(self):
        """Marcio tasg fel un wedi'i chwblhau"""
        self.cwblhawyd = True


class RheolwrTasgau:
    def __init__(self, llwybr_storio: str = "tasgau.json"):
        self.llwybr_storio = llwybr_storio
        self.tasgau = []
        self.id_nesaf = 1
        self.llwytho_tasgau()
    
    def ychwanegu_tasg(self, tasg: Tasg) -> Tasg:
        """Ychwanegu tasg newydd a neilltuo ID"""
        tasg.id = self.id_nesaf
        self.id_nesaf += 1
        self.tasgau.append(tasg)
        self.cadw_tasgau()
        return tasg
    
    def cael_tasg(self, id_tasg: int) -> Optional[Tasg]:
        """Dod o hyd i dasg yn ôl ID"""
        for tasg in self.tasgau:
            if tasg.id == id_tasg:
                return tasg
        return None
    
    def diweddaru_tasg(self, id_tasg: int, **kwargs) -> Optional[Tasg]:
        """Diweddaru tasg yn ôl ID"""
        tasg = self.cael_tasg(id_tasg)
        if not tasg:
            return None
        
        # Diweddaru priodoleddau
        for allwedd, gwerth in kwargs.items():
            if hasattr(tasg, allwedd):
                setattr(tasg, allwedd, gwerth)
        
        self.cadw_tasgau()
        return tasg
    
    def dileu_tasg(self, id_tasg: int) -> bool:
        """Dileu tasg yn ôl ID"""
        tasg = self.cael_tasg(id_tasg)
        if not tasg:
            return False
        
        self.tasgau.remove(tasg)
        self.cadw_tasgau()
        return True
    
    def cael_pob_tasg(self) -> List[Tasg]:
        """Dychwelyd pob tasg"""
        return self.tasgau
    
    def cael_tasgau_anghyflawn(self) -> List[Tasg]:
        """Dychwelyd tasgau anghyflawn"""
        return [tasg for tasg in self.tasgau if not tasg.cwblhawyd]
    
    def cael_tasgau_hwyr(self) -> List[Tasg]:
        """Dychwelyd tasgau sydd wedi pasio'u dyddiadau"""
        nawr = datetime.datetime.now()
        return [
            tasg for tasg in self.tasgau 
            if tasg.dyddiad_dyledus and tasg.dyddiad_dyledus < nawr and not tasg.cwblhawyd
        ]
    
    def cadw_tasgau(self) -> None:
        """Cadw tasgau i ffeil"""
        data = {
            'id_nesaf': self.id_nesaf,
            'tasgau': [tasg.i_geiriadur() for tasg in self.tasgau]
        }
        
        with open(self.llwybr_storio, 'w') as f:
            json.dump(data, f, indent=2)
    
    def llwytho_tasgau(self) -> None:
        """Llwytho tasgau o ffeil"""
        if not os.path.exists(self.llwybr_storio):
            self.tasgau = []
            self.id_nesaf = 1
            return
        
        try:
            with open(self.llwybr_storio, 'r') as f:
                data = json.load(f)
                
            self.id_nesaf = data.get('id_nesaf', 1)
            self.tasgau = [Tasg.o_geiriadur(data_tasg) for data_tasg in data.get('tasgau', [])]
        except json.JSONDecodeError:
            # Os yw'r ffeil wedi'i llygrur, dechrau gyda rhestr wag
            self.tasgau = []
            self.id_nesaf = 1
    
    def chwilio_tasgau(self, ymholiad: str) -> List[Tasg]:
        """Chwilio tasgau yn ôl testun yn y teitl neu ddisgrifiad"""
        ymholiad = ymholiad.lower()
        canlyniadau = []
        for tasg in self.tasgau:
            if ymholiad in tasg.teitl.lower() or (tasg.disgrifiad and ymholiad in tasg.disgrifiad.lower()):
                canlyniadau.append(tasg)
        return canlyniadau


# Enghraifft o ddefnydd
if __name__ == "__main__":
    # Creu rheolwr tasgau
    rheolwr = RheolwrTasgau()
    
    # Ychwanegu rhai tasgau
    tasg1 = Tasg("Cwblhau papur seminar", "Penodau cyflwr y gelfyddyd a dylunio arbrawf", 5, 
                datetime.datetime(2025, 5, 30))
    tasg2 = Tasg("Prynu bwydydd", "Bara, llaeth, wyau", 3)
    
    rheolwr.ychwanegu_tasg(tasg1)
    rheolwr.ychwanegu_tasg(tasg2)
    
    # Argraffu pob tasg
    for tasg in rheolwr.cael_pob_tasg():
        print(f"{tasg.id}: {tasg.teitl} (Blaenoriaeth: {tasg.blaenoriaeth})")
        if tasg.dyddiad_dyledus:
            print(f"  Dyddiad dyledus: {tasg.dyddiad_dyledus.strftime('%d.%m.%Y')}")
