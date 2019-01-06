from __future__ import annotations
import random
from typing import List
import numpy as np

class Solver:
    # some features that can be implemented:
    # - other search methods (simulated annealing, genetic algorithm...)
    # - optional search trace (solutions generated in each iterations with goal functions) - now everything is printed

    def __init__(self, all_fights_results: np.array):
        self.team_results_history = np.zeros((1, 7))
        random.seed(0)  # for now hardcoded (deterministic runtime)
        self.fights = all_fights_results

    def random_search(self, iterations: int = 100) -> (float, List[int]):
        team = PokemonTeam(self.fights)
        best_team_indices = team.indices.copy()
        best_score = 0.0
        for i in range(iterations):
            team_results = team.goal_function()
            score = team_results[0][-1]
            self.team_results_history = np.append(self.team_results_history, team_results, axis=0)
            print(f"{i}: team {team.indices}, scores: {score}, best pokemon index: {team.best_pokemon_index()}")
            if score > best_score:
                print(f"updating best score ({score} > {best_score})")
                best_score = score
                best_team_indices = team.indices.copy()
            team = team.random_neighbor()
        return best_score, best_team_indices

    def get_team_results_history(self):
        return self.team_results_history

class PokemonTeam:
    def __init__(self, all_fights_results: np.array, indices_in_team: List[int] = None):
        self.all_fights_results = all_fights_results
        self.number_of_all_pokemons = all_fights_results.shape[0]
        if all_fights_results.shape != (self.number_of_all_pokemons, self.number_of_all_pokemons):
            raise ValueError(f"all_fights_results array should be square matrix, got shape {all_fights_results.shape}")
        self.indices = indices_in_team if indices_in_team is not None else list(range(6))
        if len(self.indices) > self.number_of_all_pokemons:
            raise ValueError(f"cannot initialize pokemon team - team size (got {len(self.indices)}) " +
                             f"cannot be greater than number of all pokemons (got {self.number_of_all_pokemons})")
        self.individual_points = np.zeros(len(self.indices))

    def get_team_size(self):
        return len(self.indices)

    def random_neighbor(self) -> PokemonTeam:
        index_to_be_replaced = random.randrange(len(self.indices))
        new_pokemon_index = self.random_index_outside_of_team()
        new_indices = self.indices
        new_indices[index_to_be_replaced] = new_pokemon_index
        return PokemonTeam(self.all_fights_results, new_indices)

    def random_index_outside_of_team(self) -> int:
        index_in_enemies_list = random.randrange(self.number_of_all_pokemons - len(self.indices))
        for index_in_pokemons_list in range(self.number_of_all_pokemons):
            if index_in_enemies_list == 0:
                return index_in_pokemons_list
            if index_in_pokemons_list not in self.indices:
                index_in_enemies_list -= 1
        raise RuntimeError("this code should be unreachable")

    def goal_function(self) -> np.array:
        team_score = 0.0
        all_fights_results = np.zeros((1, len(self.indices)))
        for enemy_index in range(self.number_of_all_pokemons):
            fight_result = self.score_fights(enemy_index)
            team_score += np.sum(fight_result)/self.get_team_size()
            all_fights_results = np.add(all_fights_results, fight_result)
        all_fights_results = np.array([np.append(all_fights_results, team_score)])
        return all_fights_results

    def score_fights(self, enemy_index: int) -> np.array:
        self.individual_points.fill(0.0)
        points_against_given_enemy = np.empty(len(self.indices))
        for list_index, pokemon_index in enumerate(self.indices):
            points_against_given_enemy[list_index] = self.all_fights_results[pokemon_index, enemy_index]
        self.individual_points += points_against_given_enemy
        return points_against_given_enemy

    def best_pokemon_index(self) -> int:
        return np.argmax(self.individual_points)
