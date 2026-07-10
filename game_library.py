"""
game_library.py

Defines the GameLibrary class: the engine that manages a collection
of Game objects.

Responsibility: add, delete, search, update, save, and load games.
It does NOT ask the user for input and does NOT print menus -
some other "driver" (main.py) calls it and handles all I/O.
"""
from pathlib import Path

from game import Game


class GameLibrary:
    def __init__(self, filename="Game-Library-Manager-v1.0//games.txt"):
        self.games = []
        self.filename = filename

    # ------------------------------------------------------------------
    # CRUD operations
    # ------------------------------------------------------------------
    def add_game(self, title, genre, hours_played, rating):
        title = Game.validate_title(title)
        genre = Game.validate_genre(genre)
        hours_played = Game.validate_hours(hours_played)
        rating = Game.validate_rating(rating)

        if self.search_game(title) is not None:
            raise ValueError(f'"{title}" already exists in the library.')

        self.games.append(Game(title, genre, hours_played, rating))

    def delete_game(self, title):
        game = self.search_game(title)
        if game is None:
            return False
        self.games.remove(game)
        return True

    def search_game(self, title):
        needle = title.strip().lower()
        for game in self.games:
            if game.title.strip().lower() == needle:
                return game
        return None

    def update_hours(self, title, new_hours):
        game = self.search_game(title)
        if game is None:
            return False
        game.hours_played = Game.validate_hours(new_hours)
        return True

    def update_rating(self, title, new_rating):
        game = self.search_game(title)
        if game is None:
            return False
        game.rating = Game.validate_rating(new_rating)
        return True

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------
    def save(self):
        path = Path(self.filename)
        with path.open("w") as f:
            for game in self.games:
                f.write(game.to_line() + "\n")

    def load(self):
        self.games.clear()
        path = Path(self.filename)
        if not path.exists():
            return False

        with path.open("r") as f:
            lines = [line for line in f if line.strip()]

        self.games = [Game.from_line(line) for line in lines]
        return True
