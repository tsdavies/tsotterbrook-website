import json
import os


def load_initial_pokemon():
    """Load prepopulated Pokémon data from a cache file."""
    cache_file = os.path.join(os.path.dirname(__file__), "initial_pokemon_data.json")
    if os.path.exists(cache_file):
        with open(cache_file, "r") as file:
            return json.load(file)
    return []
