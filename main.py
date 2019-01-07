from pokemon import PokemonList
import solver
from plotter import draw_3D_plot

def temporary_main():
    pokemons = PokemonList.from_file("data.csv")
    # pokemon_data_array is unused now, can be used later to determine neighbors in terms of stats
    print("pokemons as numpy array:", pokemons.normalized_data, sep='\n')
    search_result = solver.random_search(pokemons, iterations=100, save_history=True)
    draw_3D_plot(search_result.results_history)
    print(f"best score: {search_result.best_score}, best team: {search_result.best_team.names()}")


if __name__ == '__main__':
    temporary_main()
