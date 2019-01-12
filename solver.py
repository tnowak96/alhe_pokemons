from __future__ import annotations
import random
from typing import List
from collections import namedtuple
import numpy as np
from pokemon import PokemonList
from simanneal import Annealer


RandomSearchResult = namedtuple("RandomSearchResult", ["best_score", "best_team", "results_history"])
SimulatedAnnealingResult = namedtuple("SimulatedAnnealingResult", ["best_score", "best_team", "results_history"])


def random_search(pokemons: PokemonList, iterations=100, save_history=False,
                  print_results=False) -> RandomSearchResult:
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
        _optional(print_results, print, f"{i}: team {team.indices}, scores: {team_score}")
        if team_score > best_score:
            _optional(print_results, print, f"updating best score ({team_score} > {best_score})")
            best_score = team_score
            best_team_indices = team.indices.copy()
        team = team.random_neighbor()
    return RandomSearchResult(
        best_score=best_score,
        best_team=PokemonTeam(pokemons, best_team_indices),
        results_history=results_history
    )


# works only for goal_function_mean_fight_result, giving the optimal solution
def greedy_search(pokemons: PokemonList) -> PokemonTeam:
    total_individual_results = np.sum(pokemons.all_fights_results, axis=1)
    best_indices = np.argsort(total_individual_results)
    return PokemonTeam(pokemons, best_indices[-6:])


def simulated_annealing(pokemons: PokemonList, iterations=100, save_history=False) -> SimulatedAnnealingResult:
    random.seed(0)  # for now hardcoded (deterministic runtime)
    team = PokemonTeam(pokemons)
    best_score = 0.0
    sa = SimAnneal(team, save_history)
    schedule = {'tmin': 0.05, 'tmax': 25_000.0, 'steps': iterations, 'updates': 100}
    sa.set_schedule(schedule)
    # auto_schedule = sa.auto(minutes=0.1)
    # sa.set_schedule(auto_schedule)
    # print(f"auto_shedule 1min{auto_schedule}")
    sa.copy_strategy = 'method'
    best_team, best_score = sa.anneal()
    results_history = sa.team_results_history
    return SimulatedAnnealingResult(
        best_score=best_score,
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
        results = self._score_fights()
        results[0, -1] = np.max(results[0, :-1])
        return results

    def goal_function_mean_fight_result(self) -> np.array:
        results = self._score_fights()
        results[0, -1] = np.sum(results[0, :-1]) / float(len(self.indices))
        return results

    def goal_function_max_fight_result_with_capture_rate(self) -> np.array:
        results = self._score_fights()
        results[0, :-1] = np.multiply(results[0, :-1], self.normalized_capture_rates())
        results[0, -1] = np.max(results[0, :-1])
        return results

    # helper function; returned array has one more element, so that it can easily be used in goal functions
    def _score_fights(self) -> np.array:
        results = np.zeros((1, len(self.indices) + 1))
        for list_index, pokemon_index in enumerate(self.indices):
            results[0, list_index] = np.sum(self.pokemons.all_fights_results[pokemon_index, :])
        return results

    def names(self) -> List[str]:
        return list(self.pokemons[index].name for index in self.indices)

    # pokemons.normalized_data - see pokemon.py: Pokemon.get_useful_numeric_parameters, PokemonList._to_numpy_array
    def normalized_capture_rates(self) -> np.array:
        return np.array(list(self.pokemons.normalized_data[index, -1] for index in self.indices))

    def copy(self):
        return PokemonTeam(self.pokemons, self.indices.copy())


def _optional(flag: bool, function, *args, **kwargs):
    if flag:
        return function(*args, **kwargs)
    return None
