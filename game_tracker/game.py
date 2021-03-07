import random
from constants.alphabet import ALPHABET
from game_tracker.running_games import currently_running_games


class Game:
    def __init__(self, game_creator, snake_pos):
        self.game_name = random.choices(ALPHABET, k=6)
        while self.game_name in currently_running_games.keys():
            self.game_name = random.choices(ALPHABET, k=6)

        self.game_creator = game_creator
        self.players = [game_creator]
        self.snakes = {self.game_creator: snake_pos}

        currently_running_games[self.game_name] = self

    def join_game(self, player, snake_pos):
        if len(self.players) >= 2:
            return "Room full"

        self.players.append(player)
        self.snakes[player] = snake_pos
        return "Joined room"

    def update_pos(self, player, new_pos):
        self.snakes[player] = new_pos

    def get_opponent_position(self, player):
        for key, value in self.snakes.items():
            if key != player:
                return value
