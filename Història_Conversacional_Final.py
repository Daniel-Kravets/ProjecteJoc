from imprimir_historia import impresion_historia
from creacion_mapa import salas,Zona,crearSalas
from creacion_objetos import objectes,Objecte,llanterna,donut,eina,vestitEspacial,tarja,tarjaCompany
from creacion_jugador import bond,Jugador,Inventari
from creacion_personajes import personajes,Malien,IHall,Company

class Joc:
    def __init__(self , jugador:Jugador, zones:list[Zona], iHall:IHall, malien:Malien, enCurs:bool) -> None:
        self._jugador = jugador
        self._zones = zones
        self._ihall = iHall
        self._malien = malien
        self._enCurs = enCurs
        self._company:Company = personajes[1]
        self._mostrarZona = True
        self._calaixObert = False
        self._tarjaAlCalaix = True
        self._propulsorsReparats = False
        self._motorsEngegats = False
        self._infectat = False
        self._malienAvisat = False
        self._portesObertes = []      # portes que l'iHall ja ha obert (es queden obertes)
        self._comportaOberta = False  # comporta de la Sala sortida exterior cap als Propulsors
        self._neveraOberta = False    # Menjador
        self._aixetaOberta = False    # Banys

    def iniciar(self):
        while self._enCurs == True:
            zona:Zona = self._jugador._zonaActual

            if self._mostrarZona == True:
                print("\n\n----- " + zona._nom + " -----")
                print(zona.getDescripcio())

                print("\nDes d'aquí pots anar a:")
                for idSortida in zona._sortides:
                    salaDesti:Zona = self._zones[idSortida - 1]
                    estat = ""
                    if self.clauPorta(self.zonaID(), idSortida) in self._portesObertes:
                        estat = "  [porta oberta]"
                    print("  - " + salaDesti._nom + "  (escriu: anar " + str(idSortida) + ")" + estat)

                print("\nMires al voltant...")
                hiHaAlgunaCosa = False
                for objecte in zona._objectes:
                    objecte:Objecte
                    if objecte == eina and self.hiHaLlum() == False:
                        print("  Està massa fosc per veure què hi ha per aquí.")
                    else:
                        print("  - Hi ha " + objecte.nom + "  (escriu: agafar " + objecte.nom.lower() + ")")
                    hiHaAlgunaCosa = True
                if self.mostrarElementsZona() == True:
                    hiHaAlgunaCosa = True
                if hiHaAlgunaCosa == False:
                    print("  Aquí no hi ha res d'interessant.")

                if self._company._IDzona == self.zonaID():
                    if self._company._despert == True:
                        print("\nEl teu company és aquí, encara mig adormit.")
                    else:
                        print("\nEl teu company dorm com un tronc, amb la tarja penjada al coll.  (escriu: parlar company desperta)")

                print("\nOrdres: anar, agafar, deixar, usar, encendre, apagar, obrir, tancar, parlar, inventari, mirar")
                print("Si no saps què fer, escriu: parlar ihall ajuda")
                print("Si vols plegar, escriu: sortir")
                self._mostrarZona = False

            try:
                accio = input("\nQuè vols fer? ").lower().strip()
            except (EOFError, KeyboardInterrupt):
                print("\nPartida interrompuda. Fins aviat, capità!")
                self._enCurs = False
                break

            self.processarOrdre(accio)

            if self._enCurs == True:
                if self.comprovarFinalJoc() == True:
                    self.reiniciar()

    def mostrarElementsZona(self):
        # Coses de la zona que no es poden agafar però amb les que es pot interactuar
        idZona = self.zonaID()
        if idZona == 2:
            if self._comportaOberta == True:
                print("  - La comporta cap als propulsors està oberta  (escriu: tancar comporta)")
            else:
                print("  - La comporta cap als propulsors està tancada  (escriu: obrir comporta)")
            return True
        if idZona == 3:
            print("  - Hi ha una nevera al racó  (escriu: obrir nevera)")
            return True
        if idZona == 6:
            print("  - Hi ha una aixeta que degota  (escriu: obrir aixeta / tancar aixeta)")
            return True
        if idZona == 8:
            if self._calaixObert == True:
                print("  - Hi ha un calaix obert en un escriptori  (escriu: tancar calaix)")
            else:
                print("  - Hi ha uns escriptoris amb calaixos  (escriu: obrir calaix)")
            return True
        if idZona == 9:
            if self._propulsorsReparats == True:
                print("  - El panell dels motors està llest  (escriu: encendre motors)")
            else:
                print("  - El panell dels motors marca: AVARIA ALS PROPULSORS")
            return True
        return False

    def processarOrdre(self,ordre:str):
        paraules = ordre.split(" ")
        verb = paraules[0]
        resta = ordre[len(verb) + 1:].strip()

        if verb == "anar":
            self.anar(resta)
        elif verb == "agafar":
            self.agafar(resta)
        elif verb == "deixar":
            self.deixar(resta)
        elif verb == "usar":
            self.usar(resta)
        elif verb == "encendre" or verb == "apagar":
            self.encendreApagar(verb, resta)
        elif verb == "obrir" or verb == "tancar":
            self.obrirTancar(verb, resta)
        elif verb == "parlar":
            self.parlar(resta)
        elif verb == "inventari":
            self.mostrarInventari()
        elif verb == "mirar":
            self._mostrarZona = True
        elif verb == "sortir":
            print("Bond decideix que ja n'hi ha prou per avui. Fins aviat!")
            self._enCurs = False
        else:
            print("Això no té gaire sentit ara mateix...")

    def zonaID(self):
        return self._zones.index(self._jugador._zonaActual) + 1

    def clauPorta(self, idA:int, idB:int):
        # La porta entre la sala 3 i la 5 és la mateixa que entre la 5 i la 3
        if idA < idB:
            return str(idA) + "-" + str(idB)
        return str(idB) + "-" + str(idA)

    def hiHaLlum(self):
        inventari:Inventari = self._jugador._inventari
        if llanterna in inventari.objectes and llanterna._encesa == True:
            return True
        return False

    def buscarObjecte(self, nom:str, llista:list):
        for objecte in llista:
            objecte:Objecte
            if nom != "" and nom in objecte.nom.lower():
                return objecte
        return None

    def llegirNumeroSala(self, text:str):
        # Agafa l'últim número del text. Ex: "porta 3" -> 3, "obre la 5" -> 5
        paraules = text.split(" ")
        try:
            return int(paraules[len(paraules) - 1])
        except ValueError:
            return None

    def anar(self, resta:str):
        zona:Zona = self._jugador._zonaActual
        inventari:Inventari = self._jugador._inventari

        try:
            numero = int(resta)
        except ValueError:
            print("Has d'escriure el número de la sala. Per exemple: anar 3")
            return

        if numero not in zona._sortides:
            print("Per aquí no es pot passar.")
            return
        idDesti = numero

        portaOberta = False
        if idDesti == 1 or self.zonaID() == 1:
            # Entre la Sala sortida exterior i els Propulsors hi ha la comporta, no una porta normal
            if idDesti == 1 and self._jugador._portaVestit == False:
                print("Sense el vestit espacial posat no aguantaries ni cinc segons a fora.")
                return
            if self._comportaOberta == False:
                print("La comporta exterior està tancada.  (escriu: obrir comporta)")
                return
            portaOberta = True
        elif tarja in inventari.objectes:
            print("Passes la teva tarja pel lector i la porta s'obre.")
            portaOberta = True
        elif tarjaCompany in inventari.objectes:
            print("iHall: Aquesta tarja no és teva, capità... T'obro, però que consti que ho sé.")
            portaOberta = True
        elif self.clauPorta(self.zonaID(), idDesti) in self._portesObertes:
            portaOberta = True
        else:
            print("La porta està tancada i no tens tarja. Li demanes a l'iHall que te l'obri...")
            portaOberta = self._ihall.obrirPorta(self._jugador, idDesti, self._zones)
            if portaOberta == True:
                self._portesObertes.append(self.clauPorta(self.zonaID(), idDesti))
            else:
                print("(Pots tornar-li a demanar: escriu 'anar " + str(idDesti) + "' o 'parlar ihall obre " + str(idDesti) + "'. No perds cap torn.)")

        if portaOberta == False:
            return

        self._jugador.moure(idDesti, self._zones)
        self._mostrarZona = True
        self._malienAvisat = False
        self.mourePersonatges()

    def mourePersonatges(self):
        self._malien.moure(self._zones)
        if self._company._despert == True:
            self._company.moure_aleatori(self._zones)
            zonaCompany:Zona = self._zones[self._company._IDzona - 1]
            if donut in zonaCompany._objectes:
                zonaCompany._objectes.remove(donut)
                print("Se sent algú mastegant lluny... El company ha trobat els dònuts i se'ls ha cruspit.")

    def agafar(self, resta:str):
        zona:Zona = self._jugador._zonaActual
        inventari:Inventari = self._jugador._inventari
        objecte = self.buscarObjecte(resta, zona._objectes)

        if objecte == None:
            if "tarja" in resta and self._company._IDzona == self.zonaID() and self._company.tarja != None:
                if self._company._despert == False:
                    print("El company porta la tarja posada i dorm. Primer l'hauràs de despertar.")
                    return
                if inventari.afegir(self._company.tarja) == True:
                    self._company.tarja = None
                    print("Li agafes la tarja al company, que ni se n'adona.")
                return
            print("Aquí no hi ha res d'això.")
            return

        if objecte == eina and self.hiHaLlum() == False:
            print("Està tot fosc i no trobes res. Et cal una llanterna encesa.")
            return

        if len(inventari.objectes) >= inventari.capacitat:
            print("Ja no et cap res més a sobre. Deixa alguna cosa abans.")
            return

        self._jugador.agafar(objecte, self._zones)

    def deixar(self, resta:str):
        inventari:Inventari = self._jugador._inventari
        objecte = self.buscarObjecte(resta, inventari.objectes)
        if objecte == None:
            print("No portes això a sobre.")
            return
        if objecte == vestitEspacial and self._jugador._portaVestit == True:
            if self.zonaID() == 1:
                print("Treure't el vestit aquí fora no és gaire bona idea.")
                return
            self._jugador._portaVestit = False
        self._jugador.deixar(objecte, self._zones)

    def usar(self, resta:str):
        inventari:Inventari = self._jugador._inventari
        objecte = self.buscarObjecte(resta, inventari.objectes)
        if objecte == None:
            print("No portes això a sobre.")
            return

        malienAqui = False
        if self._malien._IDzona == self.zonaID() and self._malien._distret == False:
            malienAqui = True

        if objecte == vestitEspacial:
            if self._jugador._portaVestit == True:
                if self.zonaID() == 1:
                    print("Treure't el vestit aquí fora no és gaire bona idea.")
                else:
                    self._jugador._portaVestit = False
                    print("Et treus el vestit espacial.")
            else:
                self._jugador._portaVestit = True
                print("Et poses el vestit espacial. Ja pots sortir a l'exterior.")
        elif objecte == llanterna:
            self._jugador.usar(llanterna, None)
        elif objecte == eina:
            if malienAqui == True:
                self._infectat = True
                self._malien._distret = True
                self._malien._IDzona = 0
                print("Intentes clavar-li l'eina a en Malien, però se t'escola gola avall. No fa gaire bona pinta...")
            elif self.zonaID() == 1:
                if self._propulsorsReparats == True:
                    print("Els propulsors ja estan reparats. Cap a Comandament!")
                else:
                    self._propulsorsReparats = True
                    print("Després de suar una bona estona, els propulsors queden reparats. Ara corre cap a Comandament!")
            else:
                print("Aquí l'eina no et serveix de res.")
        elif objecte == donut:
            if malienAqui == True:
                self._malien.distreure()
                inventari.treure(donut)
            else:
                print("Millor guarda els dònuts per quan facin falta.")
        else:
            print("La tarja ja fa la seva feina sola quan passes per una porta.")

    def encendreApagar(self, verb:str, resta:str):
        if "motor" in resta:
            self.encendreApagarMotors(verb)
            return

        inventari:Inventari = self._jugador._inventari
        if "llanterna" not in resta:
            print("Això no es pot " + verb + ".")
            return
        if llanterna not in inventari.objectes:
            print("No portes cap llanterna a sobre.")
            return

        if verb == "encendre":
            if llanterna._encesa == True:
                print("La llanterna ja està encesa.")
            else:
                llanterna.encendre()
                print("Encens la llanterna. Ara s'hi veu molt millor.")
                if self.zonaID() == 10:
                    self._mostrarZona = True
        else:
            if llanterna._encesa == False:
                print("La llanterna ja està apagada.")
            else:
                llanterna.apagar()
                print("Apagues la llanterna.")

    def encendreApagarMotors(self, verb:str):
        if self.zonaID() != 9:
            print("Els motors només es poden controlar des de Comandament.")
            return
        if verb == "apagar":
            print("Els motors ja estan aturats, capità. Per això estem aquí.")
            return
        if self._propulsorsReparats == False:
            print("Prems el botó, però el panell marca AVARIA ALS PROPULSORS. Primer els hauràs de reparar.")
            return
        self._motorsEngegats = True

    def obrirTancar(self, verb:str, resta:str):
        # Important: mirar "comporta" abans que "porta", perquè "comporta" conté "porta"
        if "calaix" in resta:
            self.obrirTancarCalaix(verb)
        elif "comporta" in resta:
            self.obrirTancarComporta(verb)
        elif "porta" in resta:
            self.obrirTancarPorta(verb, resta)
        elif "nevera" in resta:
            self.obrirTancarNevera(verb)
        elif "aixeta" in resta:
            self.obrirTancarAixeta(verb)
        else:
            print("Això no es pot " + verb + ".")

    def obrirTancarCalaix(self, verb:str):
        zona:Zona = self._jugador._zonaActual
        if self.zonaID() != 8:
            print("Aquí no hi ha cap calaix.")
            return

        if verb == "obrir":
            if self._calaixObert == True:
                print("El calaix ja està obert.")
                return
            self._calaixObert = True
            if self._tarjaAlCalaix == True:
                self._tarjaAlCalaix = False
                zona._objectes.append(tarja)
                print("Obres el calaix i... mira què hi ha! La teva tarja identificadora.  (escriu: agafar tarja)")
            else:
                print("Obres el calaix. No hi ha res més que papers.")
        else:
            if self._calaixObert == False:
                print("El calaix ja està tancat.")
                return
            self._calaixObert = False
            if tarja in zona._objectes:
                zona._objectes.remove(tarja)
                self._tarjaAlCalaix = True
            print("Tanques el calaix.")

    def obrirTancarComporta(self, verb:str):
        if self.zonaID() != 2:
            print("Aquí no hi ha cap comporta.")
            return
        if verb == "obrir":
            if self._comportaOberta == True:
                print("La comporta ja està oberta.")
                return
            if self._jugador._portaVestit == False:
                print("iHall: Capità, obrir la comporta sense vestit seria l'última cosa que faria. No l'obro.")
                return
            self._comportaOberta = True
            print("La comporta s'obre amb un xiulet. A fora hi ha els propulsors.")
        else:
            if self._comportaOberta == False:
                print("La comporta ja està tancada.")
                return
            self._comportaOberta = False
            print("Tanques la comporta.")

    def obrirTancarPorta(self, verb:str, resta:str):
        zona:Zona = self._jugador._zonaActual
        inventari:Inventari = self._jugador._inventari
        idDesti = self.llegirNumeroSala(resta)
        if idDesti == None:
            print("Quina porta? Escriu el número de la sala. Per exemple: " + verb + " porta 3")
            return
        if idDesti not in zona._sortides:
            print("Des d'aquí no hi ha cap porta cap a aquesta sala.")
            return
        if idDesti == 1 or self.zonaID() == 1:
            print("Cap als propulsors no hi ha porta, hi ha la comporta.  (escriu: " + verb + " comporta)")
            return

        porta = self.clauPorta(self.zonaID(), idDesti)
        if verb == "obrir":
            if porta in self._portesObertes:
                print("Aquesta porta ja està oberta.")
                return
            if tarja in inventari.objectes or tarjaCompany in inventari.objectes:
                print("Passes la tarja pel lector i la porta queda oberta.")
                self._portesObertes.append(porta)
                return
            if self._ihall.obrirPorta(self._jugador, idDesti, self._zones) == True:
                self._portesObertes.append(porta)
        else:
            if porta not in self._portesObertes:
                print("Aquesta porta ja està tancada.")
                return
            self._portesObertes.remove(porta)
            print("La porta es tanca amb un xiuxiueig.")

    def obrirTancarNevera(self, verb:str):
        if self.zonaID() != 3:
            print("Aquí no hi ha cap nevera.")
            return
        if verb == "obrir":
            if self._neveraOberta == True:
                print("La nevera ja està oberta.")
                return
            self._neveraOberta = True
            print("Obres la nevera. Està buida... algú s'ho ha cruspit tot. Potser a la Cuina queda alguna cosa.")
        else:
            if self._neveraOberta == False:
                print("La nevera ja està tancada.")
                return
            self._neveraOberta = False
            print("Tanques la nevera.")

    def obrirTancarAixeta(self, verb:str):
        if self.zonaID() != 6:
            print("Aquí no hi ha cap aixeta.")
            return
        if verb == "obrir":
            if self._aixetaOberta == True:
                print("L'aixeta ja està oberta.")
                return
            self._aixetaOberta = True
            print("Obres l'aixeta i et refresques la cara. Ara estàs més despert.")
        else:
            if self._aixetaOberta == False:
                print("L'aixeta ja està tancada.")
                return
            self._aixetaOberta = False
            print("Tanques l'aixeta. A l'espai l'aigua no es malgasta.")

    def parlar(self, resta:str):
        paraules = resta.split(" ")
        amb = paraules[0]
        frase = resta[len(amb) + 1:].strip()
        for article in ["el ", "la ", "els ", "les ", "l'"]:
            if frase.startswith(article):
                frase = frase[len(article):]
        if frase == "vestit espacial":
            frase = "vestit"

        if amb == "ihall":
            if frase == "llanterna":
                self._ihall.indicarUbicacio(llanterna, self._zones)
            elif frase == "malien" or frase == "alien":
                if self._infectat == True:
                    print("iHall: En Malien? El porta vostè a dins, capità. Jo no m'hi acostaria.")
                else:
                    zonaMalien:Zona = self._zones[self._malien._IDzona - 1]
                    print("iHall: Ara mateix en Malien és a " + zonaMalien._nom + ".")
            elif (frase.startswith("obre") or frase.startswith("porta")) and self.llegirNumeroSala(frase) != None:
                self.obrirTancarPorta("obrir", frase)
            else:
                self._jugador.parlar(self._ihall, frase)
        elif amb == "company":
            if self._company._IDzona != self.zonaID():
                print("El teu company no és aquí.")
            elif frase == "desperta":
                self._company.despertar()
            else:
                self._jugador.parlar(self._company, frase)
        elif amb == "malien":
            if self._malien._IDzona != self.zonaID():
                print("En Malien no és aquí, per sort.")
            else:
                self._jugador.parlar(self._malien, frase)
        else:
            print("Amb qui vols parlar? Prova 'parlar ihall ajuda' o 'parlar company desperta'.")

    def mostrarInventari(self):
        inventari:Inventari = self._jugador._inventari
        print("Portes a sobre:")
        if inventari.objectes == []:
            print("  Res de res.")
        for objecte in inventari.llistar():
            objecte:Objecte
            print("  - " + objecte.nom)
        if self._jugador._portaVestit == True:
            print("  (portes el vestit espacial posat)")

    def comprovarFinalJoc(self):
        idActual = self.zonaID()

        if self._motorsEngegats == True:
            print("\nEngegues els motors i la Pia XXII torna a posar rumb a SUMMEM. Missió complerta, capità Bond!")
            return True

        if self._infectat == True:
            self._malien._movimentsRestants = self._malien._movimentsRestants - 1
            if self._malien._movimentsRestants <= 0:
                print("\nNotes una punxada a la panxa... Un Malien petit et surt de l'estómac. Fi de la partida.")
                return True

        if self._company._despert == True and self._malien._distret == False:
            if self._company._IDzona == self._malien._IDzona:
                print("\nSe sent un crit a l'altra punta de la nau. En Malien ha trobat el teu company... Fi de la partida.")
                return True

        if self._malien._IDzona == idActual and self._malien._distret == False:
            if self._malienAvisat == True:
                self._malien.atacar()
                return True
            self._malienAvisat = True
            print("\nEn Malien és aquí i et mira amb molta gana! Fes alguna cosa ja o no ho expliques.")
        else:
            self._malienAvisat = False

        return False

    def reiniciar(self):
        try:
            resposta = input("\nVols jugar una altra partida? (s/n) ").lower().strip()
        except (EOFError, KeyboardInterrupt):
            resposta = "n"
        if resposta != "s":
            print("Fins aviat, capità!")
            self._enCurs = False
            return

        inventari:Inventari = self._jugador._inventari
        self._zones = crearSalas()
        self._jugador._zonaActual = self._zones[4]
        self._jugador._portaVestit = False
        inventari.objectes = []
        llanterna._encesa = False

        self._malien._IDzona = 7
        self._malien._distret = False
        self._malien._contador = 0
        self._malien._movimentsRestants = 7

        self._company._IDzona = 5
        self._company._despert = False
        self._company.tarja = tarjaCompany

        self._mostrarZona = True
        self._calaixObert = False
        self._tarjaAlCalaix = True
        self._propulsorsReparats = False
        self._motorsEngegats = False
        self._infectat = False
        self._malienAvisat = False
        self._portesObertes = []
        self._comportaOberta = False
        self._neveraOberta = False
        self._aixetaOberta = False



if __name__=="__main__":
    impresion_historia()
    joc_final = Joc(bond, salas, personajes[2], personajes[0], True)
    joc_final.iniciar()