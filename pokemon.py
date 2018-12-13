import csv
from typing import List
import numpy as np


class Pokemon:
    def __init__(self, row):
        self.name = row[0]
        self.pokedex_number = int(row[1])
        self.generation = int(row[2])
        self.is_legendary = bool(int(row[3]))
        self.types = [row[4]]
        if row[5]:
            self.types.append(row[5])
        self.health = int(row[6])
        self.attack = int(row[7])
        self.defense = int(row[8])
        self.special_attack = int(row[9])
        self.special_defense = int(row[10])
        self.speed = int(row[11])
        self.base_total = int(row[12])
        self.vulnerability_against = {
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

    def get_damage_taken_multiplier(self, enemy) -> float:
        return max(self.vulnerability_against[enemy_type] for enemy_type in enemy.types)

    def get_number_of_turns_to_get_killed(self, enemy) -> float:
        defense_coefficient = 10
        damage_taken = (enemy.attack * self.get_damage_taken_multiplier(enemy)) / (defense_coefficient * self.defense)
        return self.health/damage_taken

    def score_fight(self, enemy) -> float:
        turns_to_kill_enemy = np.ceil(enemy.get_number_of_turns_to_get_killed(self))
        turns_to_get_killed = np.ceil(self.get_number_of_turns_to_get_killed(enemy))
        if turns_to_kill_enemy < turns_to_get_killed:
            return 1.0  # 'self' wins
        if turns_to_kill_enemy > turns_to_get_killed:
            return 0.0  # 'self' loses
        return 0.5  # draw


def read_pokemons(filename="data.csv") -> List[Pokemon]:
    pokemons = []
    with open(filename, newline='') as file:
        reader = csv.reader(file, delimiter=';')
        iter_reader = iter(reader)
        next(iter_reader)
        for row in iter_reader:
            pokemons.append(Pokemon(row))
    return pokemons
