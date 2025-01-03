from flask import session, request
from .fetch_pokemon_by_name import fetch_pokemon_by_name


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
        recent_search = {
            "name": data["name"],
            "sprite": data["sprites"]["front_default"],
        }
        session["recent_searches"] = [
            search
            for search in session["recent_searches"]
            if search["name"].lower() != recent_search["name"].lower()
        ]
        session["recent_searches"].append(recent_search)
        session["recent_searches"] = session["recent_searches"][-5:]
        session.modified = True

    return data, None if "error" not in data else data["error"]
