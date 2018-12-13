import pokemon


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
    pokemons = pokemon.read_pokemons()
    test_fight(pokemons[24], pokemons[6])


if __name__ == '__main__':
    temporary_main()
