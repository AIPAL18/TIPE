# https://www.codeconvert.ai/ruby-to-python-converter?id=53c006b8-082b-4f67-b0fb-c4439cb8f09e
# I used https://www.codeconvert.ai/ because idk Ruby at all
#   and I approximately don't have the time to learn Ruby's OOP...
#   Though, it needed some adjustments cause it was wrong


class RollingHash:
    def __init__(self, hash=None):
        if hash is None:
            hash = {}
        default_hash = {
            'base': 257,  # prime
            'mod': 1000000007
        }
        default_hash.update(hash)
        self.base = default_hash['base']
        self.mod = default_hash['mod']
        self._prev_hash = None
        self._prev_input: list = []
        self._highest_power: int = int()

    # @staticmethod
    # def modulo_exp(n, power, mod):
    #     value = 1
    #     for _ in range(power):
    #         value = (n * value) % mod
    #     return value

    # def modulo_exp(self, power):
    #     return self.__class__.modulo_exp(self.base, power, self.mod)

    def modulo_exp(self, *args):
        n = None
        power = None
        mod = None
        if len(args) == 1:  # power
            n = self.base
            power = args[0]
            mod = self.mod
        elif len(args) == 3:
            n = args[0]
            power = args[1]
            mod = args[2]
        else:
            raise TypeError(f"modulo_exp() takes 1 or 3 positional argument(s) but {len(args)} were given")
        value = 1
        for _ in range(power):
            value = (n * value) % mod
        return value

    def hash(self, input_str):
        hash_val = 0
        characters = list(input_str)
        input_length = len(characters)

        for index, character in enumerate(characters):
            hash_val += (ord(character) * self.modulo_exp(input_length - 1 - index)) % self.mod
            hash_val %= self.mod

        self._prev_hash = hash_val
        self._prev_input = list(input_str)
        self._highest_power = input_length - 1
        return hash_val

    def next_hash(self, character):
        char_to_subtract = self._prev_input[0]
        hash_val = self._prev_hash

        hash_val = hash_val - ord(char_to_subtract) * (self.base ** self._highest_power)
        hash_val = (hash_val * self.base) + ord(character)
        hash_val %= self.mod

        self._prev_input.pop(0)
        self._prev_input.append(character)
        self._prev_hash = hash_val

        return hash_val
