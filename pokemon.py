import csv
from typing import Dict, Set
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

    def type_as_one_string(self):
        return ' '.join(sorted(self.types))

    def fill_numpy_array_with_normalized_parameters(self, array: np.array, max_values_for_normalization: np.array):
        array[0] = self.health / max_values_for_normalization[0]
        array[1] = self.attack / max_values_for_normalization[1]
        array[2] = self.defense / max_values_for_normalization[2]
        array[3] = self.vulnerability_against["bug"] / max_values_for_normalization[3]
        array[4] = self.vulnerability_against["dark"] / max_values_for_normalization[4]
        array[5] = self.vulnerability_against["dragon"] / max_values_for_normalization[5]
        array[6] = self.vulnerability_against["electric"] / max_values_for_normalization[6]
        array[7] = self.vulnerability_against["fairy"] / max_values_for_normalization[7]
        array[8] = self.vulnerability_against["fight"] / max_values_for_normalization[8]
        array[9] = self.vulnerability_against["fire"] / max_values_for_normalization[9]
        array[10] = self.vulnerability_against["flying"] / max_values_for_normalization[10]
        array[11] = self.vulnerability_against["ghost"] / max_values_for_normalization[11]
        array[12] = self.vulnerability_against["grass"] / max_values_for_normalization[12]
        array[13] = self.vulnerability_against["ground"] / max_values_for_normalization[13]
        array[14] = self.vulnerability_against["ice"] / max_values_for_normalization[14]
        array[15] = self.vulnerability_against["normal"] / max_values_for_normalization[15]
        array[16] = self.vulnerability_against["poison"] / max_values_for_normalization[16]
        array[17] = self.vulnerability_against["psychic"] / max_values_for_normalization[17]
        array[18] = self.vulnerability_against["rock"] / max_values_for_normalization[18]
        array[19] = self.vulnerability_against["steel"] / max_values_for_normalization[19]
        array[20] = self.vulnerability_against["water"] / max_values_for_normalization[20]
        array[21] = self.capture_rate / max_values_for_normalization[21]


class PokemonList(list):
    @classmethod
    def from_file(cls, filename="data.csv"):
        pokemon_list = cls()
        with open(filename, newline='') as file:
            reader = csv.reader(file, delimiter=';')
            iter_reader = iter(reader)
            next(iter_reader)
            for row in iter_reader:
                pokemon_list.append(Pokemon(row))
        return pokemon_list

    def to_numpy_array(self) -> np.array:
        all_types = set(pokemon.type_as_one_string() for pokemon in self)
        types_to_float_map = map_strings_to_numbers(all_types)
        max_numeric_values = self.max_values_of_useful_numeric_parameters()
        data = np.empty((len(self), max_numeric_values.size + 1))
        for index, pokemon in enumerate(self):
            data[index, 0] = types_to_float_map[pokemon.type_as_one_string()]
            pokemon.fill_numpy_array_with_normalized_parameters(data[index, 1:], max_numeric_values)
        return data

    def max_values_of_useful_numeric_parameters(self) -> np.array:
        array = np.empty(22)
        array[0] = np.max([pokemon.health for pokemon in self])
        array[1] = np.max([pokemon.attack for pokemon in self])
        array[2] = np.max([pokemon.defense for pokemon in self])
        array[3] = np.max([pokemon.vulnerability_against["bug"] for pokemon in self])
        array[4] = np.max([pokemon.vulnerability_against["dark"] for pokemon in self])
        array[5] = np.max([pokemon.vulnerability_against["dragon"] for pokemon in self])
        array[6] = np.max([pokemon.vulnerability_against["electric"] for pokemon in self])
        array[7] = np.max([pokemon.vulnerability_against["fairy"] for pokemon in self])
        array[8] = np.max([pokemon.vulnerability_against["fight"] for pokemon in self])
        array[9] = np.max([pokemon.vulnerability_against["fire"] for pokemon in self])
        array[10] = np.max([pokemon.vulnerability_against["flying"] for pokemon in self])
        array[11] = np.max([pokemon.vulnerability_against["ghost"] for pokemon in self])
        array[12] = np.max([pokemon.vulnerability_against["grass"] for pokemon in self])
        array[13] = np.max([pokemon.vulnerability_against["ground"] for pokemon in self])
        array[14] = np.max([pokemon.vulnerability_against["ice"] for pokemon in self])
        array[15] = np.max([pokemon.vulnerability_against["normal"] for pokemon in self])
        array[16] = np.max([pokemon.vulnerability_against["poison"] for pokemon in self])
        array[17] = np.max([pokemon.vulnerability_against["psychic"] for pokemon in self])
        array[18] = np.max([pokemon.vulnerability_against["rock"] for pokemon in self])
        array[19] = np.max([pokemon.vulnerability_against["steel"] for pokemon in self])
        array[20] = np.max([pokemon.vulnerability_against["water"] for pokemon in self])
        array[21] = np.max([pokemon.capture_rate for pokemon in self])
        return array


def map_strings_to_numbers(strings: Set[str]) -> Dict[str, float]:
    step = 1.0 / len(strings)
    number = 1.0
    retval = {}
    for string in sorted(list(strings)):
        retval[string] = number
        number -= step
    return retval
