from flask import request
from .fetch_pokemon_by_name import fetch_pokemon_by_name
from .utils.update_session_pokemon import update_session_pokemon


def handle_pokemon_search():
    """Handles Pokémon search logic for POST requests and updates session."""
    # Get the Pokémon name from the form
    name = request.form.get("name", "").strip()
    if not name:
        return None, "No Pokémon name provided."

    # Fetch Pokémon data
    data = fetch_pokemon_by_name(name)

    # Update recent searches if data is valid
    if "error" not in data:
        update_session_pokemon(data)

    return data, None if "error" not in data else data["error"]
