from abc import ABC, abstractmethod

class Objecte(ABC):
    def __init__(self, nom: str, descripcio: str, es_pot_agafar):
        self.nom = nom
        self.descripcio = descripcio
        self.es_pot_agafar = es_pot_agafar

    @abstractmethod
    def usar(self, context):
        pass

class VestitEspacial(Objecte):
    def __init__(self):
        super().__init__(
            nom="Vestit espacial",
            descripcio="Un vestit d'astronauta necessari per sortir a l'exterior de la nau",
            es_pot_agafar=True
        )
    def posar(self, jugador):
        jugador.porta_vestit = True
    def treure(self, jugador):
        jugador.porta_vestit = False
    def usar(self, context):
        if context.porta_vestit:
            self.treure(context)
            return "Ja no portes el vestit espacial."
        else:
            self.posar(context)
            return "Ara portes el vestit espacial. Pots sortir a l'exterior."

class Eina(Objecte):
    def __init__(self):
        super().__init__(
            nom = "Eina", 
            descripcio = "Una eina que es tope de bacana", 
            es_pot_agafar = True
        )
        
    def usar(self, context):
        context.usar = True
        return "Has utilitzat l'eina"


class Llanterna(Objecte):
    def __init__(self):
        super().__init__(
            nom="Llanterna",
            descripcio="Una llanterna per veure a les fosques",
            es_pot_agafar=True
        )
        self._encesa = False
    def encendre(self):
        self._encesa = True
    def apagar(self):
        self._encesa = False
    def usar(self, context):
        if self._encesa:
            self.apagar()
            return "Has apagat la llanterna."
        else:
            self.encendre()
            return "Has encès la llanterna. Ara hi veus a les fosques."
        
class Donut(Objecte):
    def __init__(self):
        super().__init__(
            nom = "Donut", 
            descripcio = "Un puto donut que t esperas", 
            es_pot_agafar = True
        )
        
    def usar(self, context):
        context.usar = True
        return "Has utilitzat el donut"

class TarjaIdentificadora(Objecte):
    def __init__(self, propietari):
        super().__init__(
            nom="Tarja identificadora",
            descripcio="Una tarja personal que obre les portes de la nau",
            es_pot_agafar=True
        )
        self.propietari = propietari
    def obrir_porta(self, sortida):
        if sortida.requereix_tarja: 
            sortida.bloquejada = False
            return True
        return False
    def usar(self, context):
        if self.obrir_porta(context):
            if self.propietari == "Bond":
                return "La porta s'ha obert amb la teva tarja."
            else:
                return ("iHall: 'Aquesta tarja no és teva, " 
                        "és d'en " + self.propietari + "!' Però t'obre la porta...")
        return "Aquesta porta no necessita tarja."

vestitEspacial =VestitEspacial()
eina=Eina()
llanterna=Llanterna()
donut=Donut()
tarja = TarjaIdentificadora(propietari="Bond")
tarjaCompany = TarjaIdentificadora(propietari="Company")
objectes=[vestitEspacial,eina,llanterna,donut,tarja,tarjaCompany]
