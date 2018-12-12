import numpy as np
import csv
import math

class Pokemon:
    def __init__(self, row):
        self.name = row[0]
        self.pokedex_number = int(row[1])
        self.generation = int(row[2])
        self.is_legendary = bool(int(row[3]))
        self.types = [row[4]]
        if row[5]:
            self.types.append(row[5])
        self.hp = int(row[6])
        self.attack = int(row[7])
        self.defense = int(row[8])
        self.sp_attack = int(row[9])
        self.sp_defense = int(row[10])
        self.speed = int(row[11])
        self.base_total = int(row[12])
        self.against = {
            "bug": float(row[13]),
            "dark": float(row[14]),
            "dragon": float(row[15]),
            "electric": float(row[16]),
            "fairy": float(row[17]),
            "fight": float(row[18]),
            "fire": float(row[19]),
            "flying": float(row[20]),
            "ghost": float(row[21]),
            "grass": float(row[22]),
            "ground": float(row[23]),
            "ice": float(row[24]),
            "normal": float(row[25]),
            "poison": float(row[26]),
            "psychic": float(row[27]),
            "rock": float(row[28]),
            "steel": float(row[29]),
            "water": float(row[30]),
        }
        self.capture_rate = int(row[31])
class Util:
    def duelFightSimulator(self, pok1, pok2):
        k = 10
        if len(pok1.types) == 1:
            against2 = pok2.against.get(pok1.types[0])
        elif len(pok1.types) == 2:
            against2 = max(pok2.against.get(pok1.types[0]), pok2.against.get(pok1.types[1]))
        Dmg_12 = (pok1.attack*against2)/(k*pok2.defense)

        if len(pok2.types) == 1:
            against1 = pok1.against.get(pok2.types[0])
        elif len(pok2.types) == 2:
            against1 = max(pok1.against.get(pok2.types[0]), pok1.against.get(pok2.types[1]))
        Dmg_21 = (pok2.attack*against1)/(k*pok1.defense)

        T_12 = math.ceil(pok2.hp/Dmg_12)
        T_21 = math.ceil(pok1.hp/Dmg_21)

        if T_12 < T_21:
            return 1
        elif T_12 > T_21:
            return 2
        else:
            return 0
def testFight(pList, idx_1, idx_2):
    if(idx_2 <= 0 or idx_1 <= 0):
        print("Index mniejszy od 0, nie ma takiego pokemona")
        return
    p1 = pList[idx_1-1]
    p2 = pList[idx_2-1]
    print(p1.name + " vs. " + p2.name)
    u = Util()
    result = u.duelFightSimulator(p1,p2)
    if(result == 1):
        print("\tWygrywa: " + p1.name)
    elif(result == 2):
        print("\tWygrywa: " + p2.name)
    if (result == 0):
        print("\tRemis: ")

if __name__ == '__main__':
    with open("data.csv", newline='') as file:
        reader = csv.reader(file, delimiter=';')
        pList = []
        iterReader = iter(reader)
        next(iterReader)
        for row in iterReader:
            pList.append(Pokemon(row))
        testFight(pList,25,7)
