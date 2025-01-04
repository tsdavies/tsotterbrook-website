from flask import session


def update_session_pokemon(data):
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
