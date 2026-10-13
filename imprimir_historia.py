historia= "En el año 2120, la nave Pia XXII viaja hacia el planeta SUMMEM buscando un nuevo hogar para la humanidad. Tras un largo período de hibernación, el capitán Bond despierta porque la IA de la nave, iHall, ha detectado una avería en el sistema de propulsión provocada por el choque con un aerolito. Bond debe moverse por las distintas zonas de la nave para conseguir el traje espacial, encontrar una linterna (solo iHall sabe dónde está, y no siempre dice la verdad), localizar la herramienta del taller y llegar hasta los propulsores para repararlos. Todo se complica porque un alienígena llamado 'Malien' ronda libremente por la nave y solo se le puede distraer con unos donuts. Bond también necesitará una tarjeta identificadora para abrir las puertas automáticas de la nave. El objetivo final es reparar los propulsores y volver a la sala de comandos para reactivar los motores y continuar la misión hacia SUMMEM."
import time
def impresion_historia():
    for letra in historia:
        print(letra,end="", flush=True)
        time.sleep(0.01)

