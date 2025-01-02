from app import create_app

app = create_app()


if __name__ == "__main__":
    print("Registered routes:")
    print(app.url_map)  # Prints all routes
    app.run(debug=True)
