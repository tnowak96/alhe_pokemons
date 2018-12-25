from __future__ import annotations
import random
from typing import List
import numpy as np

class Solver:
    def __init__(self, all_fight_results: np.array):
        random.seed(0)  # for now hardcoded (deterministic runtime)
        self.fights = all_fight_results
        self.team = PokemonTeam(all_fight_results.shape[0])


class PokemonTeam:
    def __init__(self, number_of_all_pokemons: int, indices_in_team: List[int] = None):
        self.number_of_all_pokemons = number_of_all_pokemons
        self.indices = indices_in_team if indices_in_team is not None else list(range(6))

    def random_neighbor(self) -> PokemonTeam:
        index_to_be_replaced = random.randrange(len(self.indices))
        new_pokemon_index = self.random_enemy_index()
        new_indices = self.indices
        new_indices[index_to_be_replaced] = new_pokemon_index
        return PokemonTeam(self.number_of_all_pokemons, new_indices)

    def random_enemy_index(self) -> int:
        index_in_enemies_list = random.randrange(self.number_of_all_pokemons - len(self.indices))
        for index_in_pokemons_list in range(self.number_of_all_pokemons):
            if index_in_enemies_list == 0:
                return index_in_pokemons_list
            if index_in_pokemons_list not in self.indices:
                index_in_enemies_list -= 1
        raise RuntimeError("PokemonTeam.random_enemy_index failed (this code should be unreachable)")

    def score_fights(self, enemy_index: int, all_fight_results: np.array) -> np.array:
        retval = np.empty(len(self.indices))
        for list_index, pokemon_index in enumerate(self.indices):
            retval[list_index] = all_fight_results[pokemon_index, enemy_index]
        return retval


# temporary test, meant to be executed by hand
def test_main():
    solver = Solver(np.ones((10, 10))*0.5)
    for i in range(20):
        print(f"{i}: team {solver.team.indices}, scores: {solver.team.score_fights(0, solver.fights)}")
        solver.team = solver.team.random_neighbor()

if __name__ == "__main__":
    test_main()
