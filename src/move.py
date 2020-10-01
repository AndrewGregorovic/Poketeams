class Move():

    def __init__(self, name, accuracy, power, pp,
                 types, effect_chance, effect):
        self.name = "None"
        self.accuracy = "None"
        self.power = "None"
        self.pp = "None"
        self.types = ("None")
        self.effect_chance = "None"
        self.effect = "None"

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
