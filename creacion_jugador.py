from creacion_mapa import salas,Zona
from creacion_objetos import Objecte
from creacion_personajes import Personatge

class Inventari():
    def __init__(self):
        self.objectes = []
        self.capacitat = 5
    def afegir(self, objecte:Objecte):
        if objecte in self.objectes:
            print("Ja tens aquest objecte")
            return False
        if len(self.objectes) >= self.capacitat:
            print("L'inventari està ple")
            return False
        self.objectes.append(objecte)
        print(f"S'ha afegit {objecte.nom} a l'inventari")
        return True
    def treure(self, objecte:Objecte):
        if objecte in self.objectes:
            self.objectes.remove(objecte)
            print(f"S'ha tret {objecte.nom} de l'inventari")
            return True
        print("Primer ets tonto, segon no tens aquest objecte")
        return False
    def conte(self, nom_objecte:str):
        for objecte in self.objectes:
            objecte:Objecte
            if objecte.nom.lower() == nom_objecte.lower():
                return True
        return False
    def llistar(self):
        return self.objectes



class Jugador:
    def __init__(self, nom:str, zonaActual:Zona, inventari:Inventari, portaVestit:bool):
        self._nom=nom
        self._zonaActual=zonaActual
        self._inventari=inventari
        self._portaVestit=portaVestit
    def moure(self, idDesti: int, salas: list):
        zonaActual:Zona = self._zonaActual
        if idDesti in zonaActual._sortides:
            self._zonaActual = salas[idDesti - 1]
            return True
        print("Has fumao demasiado y ves cosas")
        return False
    def agafar(self, objecte:Objecte, salas: list):
        zonaActual:Zona = self._zonaActual
        if not objecte.es_pot_agafar:
            print("Aquest objecte no es pot agafar")
            return False
        return zonaActual.treureObjecte(objecte, self._inventari)
    def deixar(self, objecte, salas: list):
        zonaActual:Zona = self._zonaActual
        return zonaActual.afegirObjecte(objecte, self._inventari)
    def usar(self, objecte:Objecte, destinacio) -> None:
        if not self._inventari.conte(objecte.nom):
            print("No tens aquest objecte a la motxilla")
            return
        print(objecte.usar(destinacio))
    def parlar(self, personatge:Personatge, frase: str):
        personatge.reaccionar(frase)

inventari=Inventari()
bond=Jugador("Bond",salas[4],inventari,False)