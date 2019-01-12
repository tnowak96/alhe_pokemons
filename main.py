from pokemon import PokemonList
import solver
from plotter import draw_3d_plot, draw_2d_plot


def temporary_main():
    pokemons = PokemonList.from_file("data.csv")
    greedy_team = solver.greedy_search(pokemons)
    print(f"greedy_team: {greedy_team.names()}, goal function: {round(greedy_team.goal_function()[0][-1],2)}")
    # pokemon_data_array is unused now, can be used later to determine neighbors in terms of stats
    # print("pokemons as numpy array:", pokemons.normalized_data, sep='\n')
<<<<<<< HEAD
    # search_result = solver.simulated_annealing(pokemons, iterations=8_000, save_history=True)
    search_result = solver.random_search(pokemons, iterations=10_000_000, save_history=True, print_results=False)
=======
    search_result = solver.simulated_annealing(pokemons, iterations=80_000, save_history=True)
    draw_3D_plot(search_result.results_history)
>>>>>>> ac1c68319bfcd2bd7e9a9077514aa0d52882c616
    print(f"best score: {round(search_result.best_score,2)}, best team: {search_result.best_team.names()}")
    draw_3d_plot(search_result.results_history)
    draw_2d_plot(search_result.results_history)


if __name__ == '__main__':
    temporary_main()
