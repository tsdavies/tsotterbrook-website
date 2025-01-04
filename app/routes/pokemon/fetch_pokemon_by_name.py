import requests
from app.routes.pokemon.utils.get_pokemon_color import get_pokemon_color


def fetch_pokemon_by_name(name):
    """Fetch and process Pokémon data from the API."""
    try:
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name.lower()}")
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()

        # Add additional attributes
        data["types"] = [t["type"]["name"] for t in data["types"]]
        data["color"] = get_pokemon_color(data["types"])
        return data

    except requests.exceptions.RequestException as e:
        return {"error": f"Error fetching Pokémon data: {str(e)}"}
