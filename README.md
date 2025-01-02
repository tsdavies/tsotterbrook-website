# Personal Digital Portfolio

## Overview

This dynamic web application serves as a personal portfolio showcasing various functionalities:

### Features

1. **Blog**:
    - Dynamic blog page allowing for content updates via a database.
    - User-friendly interface for displaying blog posts chronologically.

2. **Pokémon API Integration**:
    - Fetches and displays Pokémon details using the Pokémon API.
    - Interactive elements to search for specific Pokémon or view their stats and abilities.

3. **About and Contact Pages**:
    - Informative About page highlighting personal achievements and skills.
    - Functional Contact page with a secure, form for user messages sent via gmail.

## Technologies Used

- **Backend**: Python with Flask framework
- **Frontend**: HTML5, CSS3, Bootstrap for responsiveness and usability
- **Database**: SQLite (or [your database choice]) for dynamic content storage
- **API Integration**: Pokémon API for real-time Pokémon data
- **Deployment**: OpenShift using Gunicorn for robust hosting and scalability

## Installed Packages and Their Purpose

- **Flask**: Web framework to build and manage the application
- **Flask-WTF**: Simplifies form handling and validation
- **Gunicorn**: WSGI server for deploying the Flask application on OpenShift
- **Requests**: Facilitates API calls to the Pokémon API
- **SQLite3**: (Default Python library) used for database storage
- **Bootstrap**: Frontend library for responsive design
- **pip freeze**: Captures exact dependencies in `requirements.txt` for deployment

## Deployment Instructions

1. Install project dependencies:

```bash
    pip install -r requirements.txt
```

2. Activate the virtual environment and run the application locally for testing:

```bash
. venv/bin/activate # Mac/Linux
. venv\Scripts\activate # Windows
flask run
```

