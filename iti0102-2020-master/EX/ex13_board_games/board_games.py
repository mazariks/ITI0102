"""EX13. Board games."""


class Player:
    """People who play board games."""

    def __init__(self, name: str):
        """Constructor of player."""
        self.player_name = name


class Game:
    """Board games class."""

    def __init__(self, name: str):
        """Constructor of board game."""
        self.game_name = name
        self.result_type = ""
        self.played_times = 1
        self.players = []
        self.results = []
        self.possible_types = ["places", "winner", "points"]
        self.winner = None
        self.loser = None

    def set_result_type(self, value: str) -> bool:
        """Set type of result."""
        if value in self.possible_types:
            self.result_type += value
            return True
        return False

    def add_player_to_game(self, player: Player) -> bool:
        """Add player to this game."""
        if player not in self.players:
            self.players.append(player)
            return True
        return False

    def add_results_to_game(self, value: str):
        """Add results to this game."""
        if "\n" in value:
            value = value[:-1]
        self.results = value.split(",")

    def winner_of_game(self) -> Player:
        """Find winner of the game."""
        if self.result_type == "winner" or self.result_type == "places":
            return_value = self.results[0]
            for player in self.players:
                if player.player_name == return_value:
                    self.winner = player
                    return player
        elif self.result_type == "points":
            dict_of_results = {x.player_name: int(y) for (x, y) in zip(self.players, self.results)}
            dict_keys = list(dict_of_results.keys())
            dict_values = list(dict_of_results.values())
            max_point = max(dict_of_results.values())
            winner_name = dict_keys[dict_values.index(max_point)]
            for player in self.players:
                if player.player_name == winner_name:
                    self.winner = player
                    return player

    def loser_of_game(self) -> Player:
        """Find the loser of the game."""
        if self.result_type == "places":
            return_value = self.results[-1]
            for player in self.players:
                if player.player_name == return_value:
                    self.loser = player
                    return player
        elif self.result_type == "points":
            dict_of_results = {x.player_name: int(y) for (x, y) in zip(self.players, self.results)}
            dict_keys = list(dict_of_results.keys())
            dict_values = list(dict_of_results.values())
            min_point = min(dict_of_results.values())
            loser_name = dict_keys[dict_values.index(min_point)]
            for player in self.players:
                if player.player_name == loser_name:
                    self.loser = player
                    return player


class Statistics:
    """Main class for all the statistics."""

    def __init__(self, filename: str):
        """Constructor of statistics class."""
        self.filename = filename
        self.games = self.create_games()
        self.players = self.arrange_players()

    def get(self, path: str):
        """Result of given query."""
        split_path = path.split("/")
        if "" in split_path:
            split_path.remove("")
        action = ""
        dictionary_of_choices = {"": None}
        if len(split_path) > 0:
            if len(split_path) == 1:
                action = split_path[0]
                dictionary_of_choices = {"players": self.player_names(),
                                         "games": self.game_names(),
                                         "total": self.total_amount_of_played_games()}

            elif len(split_path) == 2 and split_path[1] in ["places", "points", "winner"]:
                action = split_path[0] + "/" + split_path[1]
                dictionary_of_choices = {
                    f"total/{split_path[1]}": self.total_amount_of_played_games_certain_type(split_path[1])}

            elif len(split_path) == 3:
                action = split_path[0] + "/" + split_path[1] + "/" + split_path[2]
                if split_path[0] == "player":
                    dictionary_of_choices = {
                        f"player/{split_path[1]}/amount": self.player_amount_of_games(split_path[1]),
                        f"player/{split_path[1]}/favourite": self.player_favourite_game(split_path[1]),
                        f"player/{split_path[1]}/won": self.player_wins(split_path[1])}

                elif split_path[0] == "game":
                    dictionary_of_choices = {
                        f"game/{split_path[1]}/amount": self.amount_of_times_of_certain_game_played(split_path[1]),
                        f"game/{split_path[1]}/player-amount": self.the_most_frequent_number_of_players_in_game
                        (split_path[1]),
                        f"game/{split_path[1]}/most-wins": self.player_with_highest_number_of_wins_in_game(
                            split_path[1]),
                        f"game/{split_path[1]}/most-frequent-winner": self.player_with_highest_win_rate_in_game
                        (split_path[1]),
                        f"game/{split_path[1]}/most-losses": self.player_with_highest_number_of_losses_in_game
                        (split_path[1]),
                        f"game/{split_path[1]}/most-frequent-loser": self.player_with_highest_lose_rate_in_game
                        (split_path[1]),
                        f"game/{split_path[1]}/record-holder": self.record_holder(split_path[1])}
        return dictionary_of_choices[action]

    def get_data_from_file(self) -> list:
        """Read file data into list."""
        with open(self.filename, "r+") as file:
            return file.readlines()

    def create_games(self) -> list:
        """Create game objects from data."""
        list_of_games = []
        list_of_data = self.get_data_from_file()
        for lines in list_of_data:
            split_line = lines.split(";")  # 0 - game name; 1 - involved players; 2 - result type; 3 - results
            players_list = split_line[1].split(",")
            game_to_create = Game(split_line[0])
            game_to_create.set_result_type(split_line[2])
            game_to_create.add_results_to_game(split_line[3])
            for player_name in players_list:
                player = Player(player_name)
                game_to_create.add_player_to_game(player)
            game_to_create.winner_of_game()
            game_to_create.loser_of_game()
            list_of_games.append(game_to_create)
        return list_of_games

    def arrange_players(self) -> list:
        """Get players out of games' list and operate at them."""
        seen_names = []
        list_of_players = []
        for game in self.games:
            for player in game.players:
                player_name = player.player_name
                if player_name not in seen_names:
                    seen_names.append(player_name)
                    list_of_players.append(player)
        return list_of_players

    def total_amount_of_played_games(self) -> int:
        """Amount of total games played."""
        return len(self.games)

    def total_amount_of_played_games_certain_type(self, given_type: str) -> int:
        """Find all the games with certain type given."""
        counter = 0
        for game in self.games:
            if given_type == game.result_type:
                counter += 1
        return counter

    def player_names(self) -> list:
        """Listed players' names."""
        list_of_names = []
        for player in self.players:
            list_of_names.append(player.player_name)
        return list_of_names

    def game_names(self) -> list:
        """Listed games' names."""
        list_of_names = []
        for game in self.games:
            if game.game_name not in list_of_names:
                list_of_names.append(game.game_name)
        return list_of_names

    def player_amount_of_games(self, name: str) -> int:
        """Number of played games by player."""
        counter = 0
        for game in self.games:
            for player in game.players:
                if name == player.player_name:
                    counter += 1
        return counter

    def player_favourite_game(self, name: str) -> str:
        """Find the favourite game of the exact player."""
        # https://www.geeksforgeeks.org/python-get-key-from-value-in-dictionary/
        dictionary_of_games = {x: 0 for x in self.game_names()}
        for game in self.games:
            for player in game.players:
                if player.player_name == name:
                    dictionary_of_games[game.game_name] += 1

        dict_keys = list(dictionary_of_games.keys())
        max_number = max(dictionary_of_games.values())
        dict_values = list(dictionary_of_games.values())
        value_to_return = dict_keys[dict_values.index(max_number)]
        if max_number == 0:
            return "Player did not play any game."
        return value_to_return

    def player_wins(self, name: str):
        """Amount of wins of the player."""
        counter = 0
        for game in self.games:
            if game.winner.player_name == name:
                counter += 1
        return counter

    def amount_of_times_of_certain_game_played(self, game_name: str) -> int:
        """Number of played games of certain name."""
        counter = 0
        for game in self.games:
            if game.game_name == game_name:
                counter += 1
        return counter

    def the_most_frequent_number_of_players_in_game(self, game_name: str) -> int:
        """The most frequent number of players in the game."""
        list_of_player_numbers = []
        number_of_plays = 0
        for game in self.games:
            if game.game_name == game_name:
                number_of_plays += 1
                length = len(game.players)
                list_of_player_numbers.append(length)
        if number_of_plays == 0:
            return 0
        return int(sum(list_of_player_numbers) / number_of_plays)

    def player_with_highest_number_of_wins_in_game(self, game_name: str) -> str:
        """Find a player who has maximum wins in certain game."""
        dictionary = {"": 0}
        for game in self.games:
            if game.game_name == game_name:
                if game.winner.player_name not in dictionary.keys():
                    dictionary[game.winner.player_name] = 1
                else:
                    dictionary[game.winner.player_name] += 1
        dict_keys = list(dictionary.keys())
        dict_values = list(dictionary.values())
        max_wins = max(dictionary.values())
        return dict_keys[dict_values.index(max_wins)]

    def amount_of_certain_game_player_managed_to_play(self, game_name: str, player_name: str) -> int:
        """Find how many times person played a certain game."""
        counter = 0
        for game in self.games:
            if game.game_name == game_name:
                for player in game.players:
                    if player_name == player.player_name:
                        counter += 1
        return counter

    def player_with_highest_win_rate_in_game(self, game_name: str) -> str:
        """Player name who has the highest win rate in certain game."""
        dictionary = {"": 0}
        dictionary_of_names_played_times = {"": 0}
        for game in self.games:
            if game.game_name == game_name:
                number_of_plays = self.amount_of_certain_game_player_managed_to_play(game_name, game.winner.player_name)
                if game.winner.player_name not in dictionary_of_names_played_times.keys():
                    dictionary_of_names_played_times[game.winner.player_name] = number_of_plays

                if game.winner.player_name not in dictionary.keys():
                    dictionary[game.winner.player_name] = 1
                else:
                    dictionary[game.winner.player_name] += 1
        final_dict = {"": 0}
        for key1, value1 in dictionary_of_names_played_times.items():
            for key2, value2 in dictionary.items():
                if key1 == key2:
                    if value1 == 0:
                        continue
                    final_dict[key1] = value2 / value1
        dict_keys = list(final_dict.keys())
        dict_values = list(final_dict.values())
        max_value = max(final_dict.values())
        return dict_keys[dict_values.index(max_value)]

    def player_with_highest_number_of_losses_in_game(self, game_name: str) -> str:
        """Player name who has the highest number of losses."""
        dictionary = {"": 0}
        for game in self.games:
            if game.game_name == game_name and (game.result_type == "points" or game.result_type == "places"):
                if game.loser.player_name not in dictionary.keys():
                    dictionary[game.loser.player_name] = 1
                else:
                    dictionary[game.loser.player_name] += 1
        dict_keys = list(dictionary.keys())
        dict_values = list(dictionary.values())
        max_losses = max(dictionary.values())
        return dict_keys[dict_values.index(max_losses)]

    def player_with_highest_lose_rate_in_game(self, game_name: str) -> str:
        """Player name who has the highest lose rate in certain game."""
        dictionary = {"": 0}
        dictionary_of_names_and_played_times = {"": 0}
        for game in self.games:
            if game.game_name == game_name and (game.result_type == "points" or game.result_type == "places"):
                number_of_plays = self.amount_of_certain_game_player_managed_to_play(game_name, game.loser.player_name)
                if game.loser.player_name not in dictionary_of_names_and_played_times.keys():
                    dictionary_of_names_and_played_times[game.loser.player_name] = number_of_plays
                if game.loser.player_name not in dictionary.keys():
                    dictionary[game.loser.player_name] = 1
                else:
                    dictionary[game.loser.player_name] += 1
        final_dict = {"": 0}
        for key1, value1 in dictionary_of_names_and_played_times.items():
            for key2, value2 in dictionary.items():
                if key1 == key2:
                    if value1 == 0:
                        continue
                    final_dict[key1] = value2 / value1
        dict_keys = list(final_dict.keys())
        dict_values = list(final_dict.values())
        max_value = max(final_dict.values())
        return dict_keys[dict_values.index(max_value)]

    def record_holder(self, game_name: str) -> str:
        """Find the record holder in the certain game."""
        counter = 0
        player_nickname = ""
        for game in self.games:
            if game.game_name == game_name and game.result_type == "points":
                dict_of_results = {x.player_name: int(y) for (x, y) in zip(game.players, game.results)}
                for key, value in dict_of_results.items():
                    if value > counter:
                        counter = value
                        player_nickname = key
        return player_nickname


if __name__ == '__main__':
    player1 = Player("Andrei")
    player2 = Player("Yana")
    player3 = Player("Ago")
    game1 = Game("7 wonders")
    game2 = Game("chess")
    game3 = Game("game of thrones")
    statistics1 = Statistics("results.txt")
    print(statistics1.get("game/terraforming mars/most-frequent-loser"))
