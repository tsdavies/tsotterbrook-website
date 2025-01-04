from flask import session

from app.routes.pokemon.data.load_initial_pokemon_data import load_initial_pokemon


def initialise_session_pokemon():
    # Load prepopulated Pokémon if not already in the session
    if "recent_searches" not in session or not session["recent_searches"]:
        session["recent_searches"] = load_initial_pokemon()
        session.modified = True
