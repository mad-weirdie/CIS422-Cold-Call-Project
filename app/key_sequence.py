
"""
We want a certain sequence of key presses to trigger the random verification mode.
This keeps track of those key presses.
"""
LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3

class KeySequence:
    def __init__(self,target=None):
        self.key_sequence = []
        if target:
            self.target_sequence = target
        else:
            self.target_sequence = [LEFT] * 10

    def add_key(self, key):
        self.key_sequence.append(key)
        if len(self.key_sequence) > len(self.target_sequence):
            self.key_sequence = self.key_sequence[-len(self.target_sequence):]

    def check_for_match(self):
        return self.key_sequence == self.target_sequence

    def reset(self):
        self.key_sequence = []