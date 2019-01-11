from pokemon import PokemonList
import solver
from plotter import draw_3D_plot


def temporary_main():
    pokemons = PokemonList.from_file("data.csv")
    # greedy_team = solver.greedy_search(pokemons)
    # print(f"greedy_team: {greedy_team.names()}, goal function: {round(greedy_team.goal_function()[0][-1],2)}")
    # pokemon_data_array is unused now, can be used later to determine neighbors in terms of stats
    # print("pokemons as numpy array:", pokemons.normalized_data, sep='\n')
    search_result = solver.simulated_annealing(pokemons, iterations=80_000, save_history=False)
    # draw_3D_plot(search_result.results_history)
    print(f"best score: {round(search_result.best_score,2)}, best team: {search_result.best_team.names()}")
    print(f"best team normalized capture rates: {search_result.best_team.normalized_capture_rates()}")
    solver.PokemonTeam.current_goal_function_name = "goal_function_mean_fight_result"
    print(f"best team goal_function_mean_fight_result: {search_result.best_team.goal_function()[0, -1]}")


if __name__ == '__main__':
    temporary_main()
