from pokemon import PokemonList


def test_fight(pokemon1, pokemon2):
    print(pokemon1.name + " vs. " + pokemon2.name)
    result = pokemon1.score_fight(pokemon2)
    if result == 1.0:
        print(f"\tWinner: {pokemon1.name}")
    elif result == 0.0:
        print(f"\tWinner: {pokemon2.name}")
    elif result == 0.5:
        print("\tDraw")


def temporary_main():
    pokemons = PokemonList.from_file("data2.csv")
    for pokemon in pokemons:
        print(pokemon.name)
    test_fight(pokemons[0], pokemons[1])
    array = pokemons.to_numpy_array()
    print(array)


if __name__ == '__main__':
    temporary_main()
