from modelos import Zona
from creacion_objetos import vestitEspacial,eina,llanterna,donut
import random
zonas=[1,2,3,4,5,6,7,8,9,10]
id=0

def salaLinterna():
    return random.randint(1,9)

def SalasSegunID(id,num):
    match id:
        case 1:
            Sala:Zona=Zona("Propulsors","Zona de motors",[],[2]) #Las sortides son los ids de las salas
            if num==1:  
                Sala._objectes.append(llanterna)
        case 2:
            Sala=Zona("Sala sortida exterior","Sortida exterior", [],[3,1])
            if num==2:  
                Sala._objectes.append(llanterna)
        case 3:
            Sala=Zona("Menjador","On els tripulants passen l'estona",[],[4,5,2])
            if num==3:  
                Sala._objectes.append(llanterna)
        case 4:
            Sala=Zona("Cuina","On els tripulants preparen el menjar",[donut],[7,3])
            if num==4:  
                Sala._objectes.append(llanterna)
        case 5:
            Sala=Zona("Dormitori","On els tripulants descanen d'un llarg dia, pot haver algú dormint",[],[6,3])
            if num==5:  
                Sala._objectes.append(llanterna)
        case 6:
            Sala=Zona("Banys","Els lavabos de la nau, semblen bruts",[],[8,5])
            if num==6:  
                Sala._objectes.append(llanterna)
        case 7:
            Sala=Zona("Vestuaris","Aqui és on la gent es prepara per un gran dia",[vestitEspacial],[8,4])
            if num==7:  
                Sala._objectes.append(llanterna)
        case 8:
            Sala=Zona("Oficines","La gent aqui sol treballar, no és habitual. Hi ha uns quants escriptoris amb calaixos",[],[6,7,10,9])
            if num==8:  
                Sala._objectes.append(llanterna)
        case 9:
            Sala=Zona("Comandament","Aqui és on estàn els 'peces gordos'",[],[8])
            if num==9:  
                Sala._objectes.append(llanterna)
        case 10:
            Sala=Zona("Tallers","On els tripulants inventen i arreglen diversos aparells. Està tot a les fosques",[eina],[8])
            if num==10:
                Sala._objectes.append(llanterna)
    return Sala

def crearSalas():
    num=salaLinterna()
    return [SalasSegunID(1,num),SalasSegunID(2,num),SalasSegunID(3,num),SalasSegunID(4,num),
        SalasSegunID(5,num),SalasSegunID(6,num),SalasSegunID(7,num),SalasSegunID(8,num)
        ,SalasSegunID(9,num),SalasSegunID(10,num)]

salas=crearSalas()