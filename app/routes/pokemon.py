import os
import json
import requests
from flask import render_template, request, session
from app.routes.pokemon_utils import pokemon_color


def load_cached_pokemon():
    """Load prepopulated Pokémon data from a cache file."""
    cache_file = os.path.join(os.path.dirname(__file__), "pokemon_data.json")
    if os.path.exists(cache_file):
        with open(cache_file, "r") as file:
            return json.load(file)
    return []


def register_pokemon_routes(app):
    @app.route("/pokemon", methods=["GET", "POST"])
    @app.route("/pokemon/<string:name>", methods=["GET", "POST"])
    def pokemon(name=None):
        data = None

        # Load prepopulated Pokémon if not already in the session
        if "recent_searches" not in session or not session["recent_searches"]:
            session["recent_searches"] = load_cached_pokemon()
            session.modified = True

        # Get the Pokémon name from query parameters or form
        name = name or request.args.get("name", "").strip()

        # Fetch Pokémon data if a name is provided
        if name or request.method == "POST":
            if request.method == "POST":
                name = request.form.get("name").strip()

            try:
                response = requests.get(
                    f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
                )
                response.raise_for_status()  # Raise an HTTPError for bad responses
                data = response.json()
                data["types"] = [t["type"]["name"] for t in data["types"]]
                data["color"] = pokemon_color(data["types"])

                # Update recent searches
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

            except requests.exceptions.RequestException as e:
                data = {"error": f"Error fetching Pokémon data: {str(e)}"}

        return render_template(
            "pokemon/pokemon.html",
            data=data,
            name=name,
            title="Pokémon Search",
            recent_searches=session["recent_searches"],
        )
