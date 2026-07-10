"""
main.py

The menu / driver for the Game Library Manager.

Responsibility: show the menu, read user input, and call the
appropriate GameLibrary methods. All user-facing text and I/O
lives here - GameLibrary itself never talks to the user directly.
"""

from game_library import GameLibrary

MENU_TEXT = """
========================================
       GAME LIBRARY MANAGER v1.0
========================================
1. Add Game
2. View Games
3. Search Game
4. Update Game
5. Delete Game
6. Save Library
7. Load Library
8. Exit
"""


def show_menu():
    print(MENU_TEXT)


def add_game(library):
    while True:
        title = input("Enter Title (or 6 to save and return to menu): ")
        if title.strip() == "6":
            library.save()
            print("Saved successfully.")
            return

        genre = input("Enter Genre: ")
        hours = input("Hours Played: ")
        rating = input("Rating (1-5): ")
        try:
            library.add_game(title, genre, hours, rating)
            print("Game added successfully.")
        except ValueError as error:
            print(f"Error: {error}")


def view_games(library):
    if not library.games:
        print("No games in library.")
        return

    separator = "=" * 32
    print(separator)
    for index, game in enumerate(library.games, start=1):
        print(game.display(index))
        print(separator)


def search_game(library):
    title = input("Enter title: ")
    game = library.search_game(title)
    if game is None:
        print("Game not found.")
    else:
        print(game.display())


def update_game(library):
    title = input("Enter title: ")
    game = library.search_game(title)
    if game is None:
        print("Game not found.")
        return

    print("1. Update Hours")
    print("2. Update Rating")
    print("3. Cancel")
    choice = input("Choose an option: ").strip()

    try:
        if choice == "1":
            new_hours = input("New Hours: ")
            library.update_hours(title, new_hours)
            print("Game updated successfully.")
        elif choice == "2":
            new_rating = input("New Rating: ")
            library.update_rating(title, new_rating)
            print("Game updated successfully.")
        elif choice == "3":
            return
        else:
            print("Invalid option.")
    except ValueError as error:
        print(f"Error: {error}")


def delete_game(library):
    title = input("Enter title: ")
    game = library.search_game(title)
    if game is None:
        print("Game not found.")
        return

    confirm = input("Are you sure? (Y/N): ").strip().upper()
    if confirm == "Y":
        library.delete_game(title)
        print("Game deleted.")
    # any other input: silently return to menu


def save_library(library):
    library.save()
    print("Saved successfully.")


def load_library(library):
    if library.load():
        print(f"Loaded {len(library.games)} games.")
    else:
        print("No save file found.")


def exit_program(library):
    choice = input("Would you like to save before exiting? (Y/N): ").strip().upper()
    if choice == "Y":
        library.save()
        print("Saved successfully.")
    print("Goodbye!")


def main():
    library = GameLibrary()

    actions = {
        "1": add_game,
        "2": view_games,
        "3": search_game,
        "4": update_game,
        "5": delete_game,
        "6": save_library,
        "7": load_library,
    }

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "8":
            exit_program(library)
            break

        action = actions.get(choice)
        if action is None:
            print("Invalid option. Please choose 1-8.")
            continue

        action(library)


if __name__ == "__main__":
    main()