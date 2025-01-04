from flask import render_template, request, session

from .fetch_pokemon_by_name import fetch_pokemon_by_name
from .handle_pokemon_search import handle_pokemon_search
from .utils.initialise_session_pokemon import initialise_session_pokemon


def search(name=None):
    data = None
    error = None

    initialise_session_pokemon()

    # Handle POST requests
    if request.method == "POST":
        data, error = handle_pokemon_search()
    else:
        # Handle GET requests: Get Pokémon name from query parameters
        name = name or request.args.get("name", "").strip()
        if name:
            data = fetch_pokemon_by_name(name)

    return render_template(
        "pokemon/pokemon.html",
        data=data,
        error=error,
        name=name,
        title="Pokémon Search",
        recent_searches=session["recent_searches"],
    )


