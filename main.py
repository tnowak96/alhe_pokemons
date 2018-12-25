from pokemon import PokemonList
from solver import Solver


def temporary_main():
    pokemons = PokemonList.from_file("data.csv")
    # pokemon_data_array is unused now, can be used later to determine neighbors in terms of stats
    pokemon_data_array = pokemons.to_numpy_array()
    print("pokemons as numpy array:", pokemon_data_array, sep='\n')
    fight_results_array = pokemons.generate_all_fight_results()
    solver = Solver(fight_results_array)
    best_score, best_team_indices = solver.random_search(iterations=20)
    winners_names = list(map(lambda index: pokemons[index].name, best_team_indices))
    print(f"best score: {best_score}, best team: {winners_names}")


if __name__ == '__main__':
    temporary_main()
