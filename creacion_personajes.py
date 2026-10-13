from abc import ABC, abstractmethod
from creacion_objetos import objectes,TarjaIdentificadora,Objecte,Donut,tarja,tarjaCompany
from creacion_mapa import salas,Zona
import random
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from creacion_jugador import Jugador

class Personatge:
    def __init__(self,nom:str,IDzona):
        self._nom=nom
        self._IDzona=IDzona
        
        
    def reaccionar(self,frase:str):
        frase = frase.lower()
        match frase:
            case "hola":
                if self._nom == "iHall":
                    print("Que tal, que necesitas?")
                elif self._nom == "Company":
                    print("ZzZzZzZ")
                else:
                    print("Grrrrr!!!")
            case "adeu":
                if self._nom == "iHall":
                    print("Chao")
                elif self._nom == "Company":
                    print("ZzZzZzZ")
                else:
                    print("Grrrrr!!!")
            case "ajuda":
                if self._nom == "iHall":
                    print("En què et puc ajudar, capità?")
                    print("tinc informacio sobre: la llanterna, el Malien, la porta, la tarja, la eina, el vestit espacial o els propulsors")
                elif self._nom == "Company":
                    print("ZzZzZzZ")
                else:
                    print("Grrrrr!!!")
            case "qui ets":
                if self._nom == "iHall":
                    print("Soc l'iHall")
                elif self._nom == "Company":
                    print("ZzZzZzZ")
                else:
                    print("Grrrrr!!!")
            case "llanterna":
                if self._nom == "iHall":
                    print("La llanterna? Crec que és en algun lloc de la nau... o potser no.")
                elif self._nom == "Company":
                    print("ZzZzZzZ")
                else:
                    print("Grrrrr!!!")
            case "malien" | "alien":
                if self._nom == "iHall":
                    print("En Malien ronda per la nau. Vés amb compte, capità.")
                elif self._nom == "Company":
                    print("ZzZzZzZ")
                else:
                    print("Grrrrr!!!")
            case "porta" | "obre":
                if self._nom == "iHall":
                    print("D'acord capità, t'obro la porta... si em ve de gust.")
                elif self._nom == "Company":
                    print("ZzZzZzZ")
                else:
                    print("Grrrrr!!!")
            case "tarja":
                if self._nom == "iHall":
                    print("La teva tarja? La vas deixar en algun calaix de les Oficines.")
                elif self._nom == "Company":
                    print("ZzZzZzZ")
                else:
                    print("Grrrrr!!!")
            case "eina":
                if self._nom == "iHall":
                    print("L'eina és al Taller, però està a les fosques. Necessitaràs llum.")
                elif self._nom == "Company":
                    print("ZzZzZzZ")
                else:
                    print("Grrrrr!!!")
            case "vestit":
                if self._nom == "iHall":
                    print("El vestit espacial és al Vestuari. Sense ell no sobreviuràs a fora.")
                elif self._nom == "Company":
                    print("ZzZzZzZ")
                else:
                    print("Grrrrr!!!")
            case "propulsors" | "motor":
                if self._nom == "iHall":
                    print("Hem xocat amb un aeròlit. Cal reparar els propulsors amb l'eina.")
                elif self._nom == "Company":
                    print("ZzZzZzZ")
                else:
                    print("Grrrrr!!!")
            case "desperta":
                if self._nom == "Company":
                    print("Eh? Què? Ja hem arribat a SUMMEM?")
                else:
                    print("Jo no dormo mai, capità.")
            case "donut" | "menjar":
                if self._nom == "Company":
                    print("Tinc gana... no hi havia dònuts a la cuina?")
                elif self._nom == "iHall":
                    print("Els dònuts són a la cuina. A en Malien li encanten.")
                else:
                    print("Mmmm... dònuts...")
            case _:
                print("No t'entenc.")
    
    
    def moure(self, idDesti: int, salas: list):
        zonaActual:Zona = salas[self._IDzona - 1]
        if idDesti in zonaActual._sortides:
            self._IDzona = idDesti
            return True
        print("Has fumao demasiado y ves cosas")
        return False

class Company(Personatge):
    def __init__(self,despert:bool,tarja):
        self._despert=despert
        self.tarja=tarja
        super().__init__(
            nom="Company",
            IDzona=5)
    def despertar(self):
        if self._despert:
            print("Ya estic despert tt, espabila.")
            return False
        self._despert = True
        print("El company es desperta. 'Que lo Que ma g'")
        print("Ara va voltant per la nau amb la seva tarja.")
        return True
            
    def moure_aleatori(self, salas: list):
            zonaActual:Zona = salas[self._IDzona - 1]
            if zonaActual._sortides != []:
                self._IDzona = random.choice(zonaActual._sortides)
        

class IHall(Personatge):
    def __init__(self, probabilitatEncert):
        self._probabilitat = probabilitatEncert
        super().__init__(
            nom="iHall",
            IDzona=None)
    def indicarUbicacio(self, objecte: Objecte, salas:list[Zona]):
        idReal = None
        for i in range(len(salas)):
            if objecte in salas[i]._objectes:
                idReal = i + 1
        if idReal is None:
            print("iHall: Buaa, yo que se tt.")
            return None
        if random.random() < self._probabilitat:
            print(f"iHall: {objecte.nom} és a {salas[idReal - 1]._nom}.")
            return idReal
        idFals = random.randint(1, len(salas))
        print(f"iHall: {objecte.nom} és a {salas[idFals - 1]._nom}.")
        return idFals
    def obrirPorta(self, jugador:"Jugador", idDesti: int, salas: list):
        zonaActual:Zona = jugador._zonaActual
        if idDesti not in zonaActual._sortides:
            print("iHall: Des d'aquí no pots anar a aquella sala, capità.")
            return False
        if random.random() < self._probabilitat:
            print("iHall: Porta oberta, capità.")
            return True
        print("iHall: Ho sento capità, ara mateix estic ocupat amb... coses importants.")
        return False
    

class Malien(Personatge):
    def __init__(self, movimentsRestants):
        super().__init__(
            nom="Malien",
            IDzona=7)
        self._movimentsRestants = movimentsRestants
        self._distret = False
        self._contador = 0
    def atacar(self):
        if self._distret:
            print("En Malien està fotense un donuts i pasa de la teva cara.")
            return False
        print("En Malien t'ha atrapat! GG EZ.")
        return True
    def distreure(self):
        if self._distret:
            print("En Malien ja esta entretingut.")
            return False
        self._distret = True
        print("Li llences el donut. En Malien el persegueix i et deixa tranquil per sempre.")
        return True
    def moure(self, salas: list):
        if self._distret:
            return
        self._contador = self._contador + 1
        if self._contador < 2:
            return
        self._contador = 0
        zonaActual:Zona = salas[self._IDzona - 1]
        if zonaActual._sortides == []:
            return
        self._IDzona = random.choice(zonaActual._sortides)

alien=Malien(7)
company=Company(False,tarjaCompany)
ihall=IHall(0.5)
personajes=[alien,company,ihall]