"""
game.py

Defines the Game class: a single game entry in the library.

Responsibility: know everything about ONE game (its data, validation
rules for that data, and how to display/serialize itself).
It does NOT know about menus, user input, searching, or files.
"""


class Game:
    """Represents a single game in the library."""

    MIN_RATING = 1
    MAX_RATING = 5

    def __init__(self, title, genre, hours_played, rating):
        self.title = title
        self.genre = genre
        self.hours_played = hours_played
        self.rating = rating

    # ------------------------------------------------------------------
    # Validation helpers (static: they validate raw input, they don't
    # need an existing Game instance to run).
    # ------------------------------------------------------------------
    @staticmethod
    def _validate_non_empty(value, field_name):
        if value is None or not str(value).strip():
            raise ValueError(f"{field_name} cannot be empty.")
        return str(value).strip()

    @staticmethod
    def validate_title(title):
        return Game._validate_non_empty(title, "Title")

    @staticmethod
    def validate_genre(genre):
        return Game._validate_non_empty(genre, "Genre")

    @staticmethod
    def validate_hours(hours):
        try:
            hours = int(hours)
        except (TypeError, ValueError):
            raise ValueError("Hours played must be a whole number.")
        if hours < 0:
            raise ValueError("Hours played cannot be negative.")
        return hours

    @staticmethod
    def validate_rating(rating):
        try:
            rating = int(rating)
        except (TypeError, ValueError):
            raise ValueError(
                f"Rating must be a whole number between "
                f"{Game.MIN_RATING} and {Game.MAX_RATING}."
            )
        if rating < Game.MIN_RATING or rating > Game.MAX_RATING:
            raise ValueError(
                f"Rating must be between {Game.MIN_RATING} and {Game.MAX_RATING}."
            )
        return rating

    # ------------------------------------------------------------------
    # Display 
    # ------------------------------------------------------------------
    def display(self, index=None):
        stars = "★" * self.rating + "☆" * (self.MAX_RATING - self.rating)
        header = f"{index}.\n" if index is not None else ""
        return (
            f"{header}"
            f"   Title  : {self.title}\n"
            f"   Genre  : {self.genre}\n"
            f"   Hours  : {self.hours_played}\n"
            f"   Rating : {stars}"
        )

    def to_line(self):
        return f"{self.title}|{self.genre}|{self.hours_played}|{self.rating}"

    @staticmethod
    def from_line(line):
        parts = line.strip().split("|")
        if len(parts) != 4:
            raise ValueError(f"Malformed save line: {line!r}")
        title, genre, hours, rating = parts
        return Game(
            Game.validate_title(title),
            Game.validate_genre(genre),
            Game.validate_hours(hours),
            Game.validate_rating(rating),
        )
