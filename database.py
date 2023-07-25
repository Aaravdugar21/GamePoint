import sqlite3
from flask import g

db_file = "app.db"
game_db_file = "game.db"

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(db_file)
    return g.db

def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def get_game_db():
    if "game_db" not in g:
        g.game_db = sqlite3.connect(game_db_file)
    return g.game_db

def close_game_db(e=None):
    game_db = g.pop("game_db", None)
    if game_db is not None:
        game_db.close()
