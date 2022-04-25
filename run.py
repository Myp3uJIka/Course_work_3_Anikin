from project.config import DevelopmentConfig
from project.dao.models import *
from project.server import create_app, db

app = create_app(DevelopmentConfig)


@app.shell_context_processor
def shell():
    return {
        "db": db,
        "Director": Director,
        "Genre": Genre,
        "Movie": Movie,
        "User": User
    }


app.run(host="localhost", port=5000, debug=True)
