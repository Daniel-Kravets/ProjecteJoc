from abc import ABC, abstractmethod
from creacion_objetos import Objecte
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from creacion_jugador import Inventari

class Zona:
    def __init__(self, nom: str, descripcio: str, objectes: list, sortides: list):
        self._nom = nom
        self._descripcio = descripcio
        self._objectes = objectes
        self._sortides = sortides

    def getDescripcio(self):
        return self._descripcio

    def afegirObjecte(self, objecte: Objecte, inventari: "Inventari"):
        if not inventari.conte(objecte.nom):
            print("No tens aquest objecte a la motxilla")
            return False
        if objecte in self._objectes:
            print("Aquest objecte ja és a la zona")
            return False
        inventari.treure(objecte)
        self._objectes.append(objecte)
        print(f"Has deixat {objecte.nom} a {self._nom}")
        return True

    def treureObjecte(self, objecte: Objecte, inventari: "Inventari"):
        if objecte not in self._objectes:
            print("Aquest objecte no està a aquesta zona")
            return False
        self._objectes.remove(objecte)
        inventari.afegir(objecte)
        print(f"Has recollit {objecte.nom}")
        return True

    def getSortida(self):
        return self._sortides

    def accionsDisponibles(self):
        accions = []
        for idSortida in self._sortides:
            accions.append("anar sala " + str(idSortida))
        for objecte in self._objectes:
            if objecte.es_pot_agafar:
                accions.append("agafar " + objecte.nom)
        return accions