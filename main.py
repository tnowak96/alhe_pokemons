import argparse
import numpy as np
from pokemon import PokemonList
import solver
from plotter import draw_3d_plot, draw_2d_plot


def run(params):
    pokemons = PokemonList.from_file(params.file)
    solver.PokemonTeam.current_goal_function_name = params.goal_function
    solver_function = getattr(solver, params.solver_function)
    save_history_flag = params.plot2d or params.plot3d or (params.outfile != "")
    search_result = solver_function(pokemons, iterations=params.iterations, save_history=save_history_flag)
    print(f"best score: {round(search_result.best_score,2)}, best team: {search_result.best_team.names()}")
    if params.team_details:
        print_team_details(search_result.best_team)
    if params.plot3d:
        draw_3d_plot(search_result.results_history)
    if params.plot2d:
        draw_2d_plot(search_result.results_history)
    if params.outfile != "":
        np.savetxt(params.outfile, search_result.results_history)


def print_team_details(team: solver.PokemonTeam):
    print(f"best team normalized capture rates: {team.normalized_capture_rates()}")
    print("best team in terms of all goal functions:")
    for function in solver.AVAILABLE_GOAL_FUNCTIONS:
        solver.PokemonTeam.current_goal_function_name = function
        print(f"{function}: {team.goal_function()[0, -1]}")


def main():
    parser = argparse.ArgumentParser(description="Find the best pokemon team in terms of a given goal function.")
    parser.add_argument("--file", dest="file", default="data.csv", help="file with pokemon data (default data.csv)")
    parser.add_argument("--goal", dest="goal_function", default="goal_function_max_fight_result_with_capture_rate",
                        help="goal function for pokemon team (default goal_function_max_fight_result_with_capture_rate)",
                        choices=solver.AVAILABLE_GOAL_FUNCTIONS)
    parser.add_argument("--solver", dest="solver_function", default="simulated_annealing",
                        help="solver function for pokemon team (default simulated_annealing)",
                        choices=solver.AVAILABLE_SOLVERS)
    parser.add_argument("--iterations", dest="iterations", type=int, default=1000, help="number of iterations (default 1000)")
    parser.add_argument("--plot2d", dest="plot2d", action="store_const", const=True, default=False, help="draw 2d plot")
    parser.add_argument("--plot3d", dest="plot3d", action="store_const", const=True, default=False, help="draw 3d plot")
    parser.add_argument("--details", dest="team_details", action="store_const", const=True, default=False,
                        help="show detailed data about winner team")
    parser.add_argument("--outfile", dest="outfile", default="",
                        help="output file for results history (default - will not be saved)")
    run(parser.parse_args())


if __name__ == '__main__':
    main()
