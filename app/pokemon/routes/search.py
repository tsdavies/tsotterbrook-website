from flask import render_template, request, session, url_for, jsonify, redirect

from .fetch_pokemon_by_name import fetch_pokemon_by_name
from .handle_pokemon_search import handle_pokemon_search
from .utils.initialise_session_pokemon import initialise_session_pokemon


def search(name=None):
    data = None
    error = None

    initialise_session_pokemon()

    if request.method == "POST":
        data, error = handle_pokemon_search()
        if not error and data:
            name = data.get("name", "")
            # Redirect to the GET version with the name in the query parameter
            return redirect(url_for('pokemon.search', name=name))

    name = name or request.args.get("name", "").strip()
    if name:
        data = fetch_pokemon_by_name(name)

    return render_template(
        "pokemon.html",
        data=data,
        error=error,
        name=name,
        title="Pokémon Search",
        recent_searches=session["recent_searches"],
    )
