from pokemon import PokemonList


def temporary_main():
    pokemons = PokemonList.from_file("data.csv")
    pokemon_data_array = pokemons.to_numpy_array()
    print(pokemon_data_array)
    fight_results_array = pokemons.generate_all_fight_results()
    print(fight_results_array)


if __name__ == '__main__':
    temporary_main()
