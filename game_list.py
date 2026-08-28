import json
import os

class games:
    json_file = "game_list.json"

    def __init__(self, title, price, synopsis):
        self.title = title
        self.price = price
        self.synopsis = synopsis

    def add_game(self):
        """Adds the game to the JSON file."""
        # Load existing games
        if os.path.exists(self.json_file):
            with open(self.json_file, "r") as f:
                try:
                    games_list = json.load(f)
                except json.JSONDecodeError:
                    games_list = []
        else:
            games_list = []
        
        # Add the new game
        game_data = {
            "title": self.title,
            "price": f"€{self.price}",
            "synopsis": self.synopsis
        }
        games_list.append(game_data)
        
        # Save back to JSON file
        with open(self.json_file, "w") as f:
            json.dump(games_list, f, indent=4)
        
        print(f"'{self.title}' has been added to the game list.")
