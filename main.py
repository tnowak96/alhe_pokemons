import numpy as np
import csv
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


with open("data.csv", newline='') as file:
    reader = csv.reader(file, delimiter=';')
    pList = []
    for row in reader:
        pList.append(Pokemon(row))