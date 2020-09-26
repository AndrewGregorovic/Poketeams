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
