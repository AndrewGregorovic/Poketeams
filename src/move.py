class Move():

    def __init__(self, name: str, accuracy: int, power: int, pp: int, types: tuple, effect_chance: int, effect: str):
        self.name: str = name
        self.accuracy: int = accuracy
        self.power: int = power
        self.pp: int = pp
        self.types: tuple = types
        self.effect_chance: int = effect_chance
        self.effect: str = effect

    @classmethod
    def from_json(cls, data):
        return cls(**data)

    @classmethod
    def from_response(cls, response):
        pass

    def view_move(self):
        pass

    def move_menu(self):
        pass

    def view_move_list(self, pokemon):
        learnt_moves = [move.name for move in pokemon.move_set]
        unlearnt_moves = []
        for move in pokemon.move_list:
            if move not in learnt_moves:
                unlearnt_moves.append(f" {move} ")

        while len(unlearnt_moves) % 4 != 0:
            unlearnt_moves.append("")

        print(f"{pokemon.name} can learn the following moves:\n")
        for a, b, c, d in zip(unlearnt_moves[::4], unlearnt_moves[1::4], unlearnt_moves[2::4], unlearnt_moves[3::4]):
            print("{:<29}{:<29}{:<29}{:<29}".format(a, b, c, d))

    def select_move(self):
        pass

    def confirm_move(self):
        pass
