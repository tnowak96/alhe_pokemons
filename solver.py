from __future__ import annotations
import random
from typing import List
from collections import namedtuple
import numpy as np
from simanneal import Annealer
from pokemon import PokemonList


SearchResult = namedtuple("SearchResult", ["best_score", "best_team", "results_history"])

AVAILABLE_GOAL_FUNCTIONS = [
    "goal_function_max_fight_result",
    "goal_function_mean_fight_result",
    "goal_function_max_fight_result_with_capture_rate"
]

AVAILABLE_SOLVERS = ["random_search", "greedy_search", "simulated_annealing"]

def random_search(pokemons: PokemonList, iterations=100, save_history=False) -> SearchResult:
    random.seed(0)  # for now hardcoded (deterministic runtime)
    team = PokemonTeam(pokemons)
    best_team_indices = team.indices.copy()
    best_score = 0.0
    results_history = np.empty((iterations, len(team.indices) + 1)) if save_history else None
    for i in range(iterations):
        all_scores = team.goal_function()
        team_score = all_scores[0][-1]
        if save_history:
            results_history[i, :] = all_scores
        if team_score > best_score:
            best_score = team_score
            best_team_indices = team.indices.copy()
        team = team.random_neighbor()
    return SearchResult(
        best_score=best_score,
        best_team=PokemonTeam(pokemons, best_team_indices),
        results_history=results_history
    )


# works only for goal_function_mean_fight_result, giving the optimal solution
def greedy_search(pokemons: PokemonList, **kwargs) -> SearchResult:
    total_individual_results = np.sum(pokemons.all_fights_results, axis=1)
    best_indices = np.argsort(total_individual_results)
    best_team = PokemonTeam(pokemons, best_indices[-6:])
    scores = best_team.goal_function()
    return SearchResult(
        best_score=scores[0][-1],
        best_team=best_team,
        results_history=scores
    )


def simulated_annealing(pokemons: PokemonList, iterations=100, save_history=False) -> SearchResult:
    random.seed(0)  # for now hardcoded (deterministic runtime)
    team = PokemonTeam(pokemons)
    sa = SimAnneal(team, save_history)
    schedule = {'tmin': 0.05, 'tmax': 25_000.0, 'steps': iterations, 'updates': 100}
    sa.set_schedule(schedule)
    # auto_schedule = sa.auto(minutes=0.1)
    # sa.set_schedule(auto_schedule)
    # print(f"auto_shedule 1min{auto_schedule}")
    sa.copy_strategy = 'method'
    best_team, best_score = sa.anneal()
    results_history = sa.team_results_history
    return SearchResult(
        best_score=-best_score,
        best_team=best_team,
        results_history=results_history
    )

class SimAnneal(Annealer):
    def __init__(self, pokemonTeam, save_history=False):
        self.save_history = save_history
        self.team_results_history = np.zeros((1, 7))
        super(SimAnneal, self).__init__(pokemonTeam)

    def move(self):
        #load new state as indices of Neighbour team
        self.state = self.state.random_neighbor()

    def energy(self):
        # calculate states energy, which will by minimized
        # minus sign is becouse our problem is maximizing goal function
        team_results = self.state.goal_function()
        if self.save_history:
            self.team_results_history = np.append(self.team_results_history, team_results, axis=0)
        return -(team_results[0][-1])


class PokemonTeam:
    current_goal_function_name = "goal_function_max_fight_result_with_capture_rate"

    def __init__(self, pokemons: PokemonList, indices_in_team: List[int] = None):
        self.pokemons = pokemons
        self.indices = indices_in_team if indices_in_team is not None else list(range(6))
        if len(self.indices) >= len(pokemons):
            raise ValueError(f"cannot initialize pokemon team - team size (got {len(self.indices)}) " +
                             f"cannot be greater than number of all pokemons (got {len(pokemons)})")

    def random_neighbor(self) -> PokemonTeam:
        index_to_be_replaced = random.randrange(len(self.indices))
        new_pokemon_index = self.random_index_outside_of_team()
        new_indices = self.indices.copy()
        new_indices[index_to_be_replaced] = new_pokemon_index
        return PokemonTeam(self.pokemons, new_indices)

    def random_index_outside_of_team(self) -> int:
        enemy_index = random.randrange(len(self.pokemons))
        while enemy_index in self.indices:
            enemy_index = random.randrange(len(self.pokemons))
        return enemy_index

    def goal_function(self) -> np.array:
        function = getattr(self, PokemonTeam.current_goal_function_name)
        return function()

    def goal_function_max_fight_result(self) -> np.array:
        results = np.zeros((1, len(self.indices) + 1))
        for enemy_index in range(len(self.pokemons)):
            individual_scores_in_one_fight = self.score_fights_against_given_enemy(enemy_index)
            results[0, :-1] += individual_scores_in_one_fight
            results[0, -1] += np.max(individual_scores_in_one_fight)
        return results

    def goal_function_mean_fight_result(self) -> np.array:
        results = np.zeros((1, len(self.indices) + 1))
        for enemy_index in range(len(self.pokemons)):
            individual_scores_in_one_fight = self.score_fights_against_given_enemy(enemy_index)
            results[0, :-1] += individual_scores_in_one_fight
            results[0, -1] += np.sum(individual_scores_in_one_fight) / float(len(self.indices))
        return results

    def goal_function_max_fight_result_with_capture_rate(self) -> np.array:
        results = np.zeros((1, len(self.indices) + 1))
        for enemy_index in range(len(self.pokemons)):
            individual_scores_in_one_fight = self.score_fights_against_given_enemy(enemy_index)
            individual_scores_in_one_fight = np.multiply(individual_scores_in_one_fight, self.normalized_capture_rates())
            results[0, :-1] += individual_scores_in_one_fight
            results[0, -1] += np.max(individual_scores_in_one_fight)
        return results

    def score_fights_against_given_enemy(self, enemy_index: int) -> np.array:
        points_against_given_enemy = np.empty(len(self.indices))
        for list_index, pokemon_index in enumerate(self.indices):
            points_against_given_enemy[list_index] = self.pokemons.all_fights_results[pokemon_index, enemy_index]
        return points_against_given_enemy

    def names(self) -> List[str]:
        return list(self.pokemons[index].name for index in self.indices)

    # pokemons.normalized_data - see pokemon.py: Pokemon.get_useful_numeric_parameters, PokemonList._to_numpy_array
    def normalized_capture_rates(self) -> np.array:
        return np.array(list(self.pokemons.normalized_data[index, -1] for index in self.indices))

    def copy(self):
        return PokemonTeam(self.pokemons, self.indices.copy())
