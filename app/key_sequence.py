################################################################################
"""
Script Name:    KeySequence class

Description:    This module keeps track of the key presses that are sent to it,
                and checks if a certain pattern is met in the most recent
                keystrokes. This is used for tracking if the sequence of keys
                that triggers random verification mode have been pressed.

Authors:        EnterPrize Labs:
                Arden Butterfield, Madison Werries, Amy Reichold,
                Quinn Fetrow, and Derek Martin

Last Edited:    1/28/2022
Last Edit By:   Arden Butterfield
"""
################################################################################

class KeySequence:
    """
    A class to store and check the most recent sequence of key presses.
    Attributes
    ============================================================================
    target_sequence:
        A list of the pattern of keys, in sequence, that we need to press.
    key_sequence:
        A list of the <n> most recent keys pressed, where <n> is the length of
        the target_sequence.
    The names of the keys here are the <keysym>s defined by Tkinter. They are
    stored as strings.
    Methods
    ============================================================================
    add_key(key)
        Add the most recently pressed key to the key sequence. This should be
        called after every key press.
    check_for_match()
        Does the recent sequence of key presses match the target sequence?
    reset()
        Remove all keystrokes from the key sequence.
    """
    def __init__(self,target=None):
        self.key_sequence = []
        if target:
            self.target_sequence = target
        else:
            self.target_sequence = ["Left"] * 10

    def add_key(self, key):
        """
        Add the most recently pressed key to the key sequence. This should be
        called after every key press.

        key: the keysym string of the most recent key pressed.
        """
        self.key_sequence.append(key)
        if len(self.key_sequence) > len(self.target_sequence):
            # If the key sequence becomes longer than the target, we trim off
            # the old key presses, to only consider the most recent ones.
            self.key_sequence = self.key_sequence[-len(self.target_sequence):]

    def check_for_match(self):
        """
        Does the recent sequence of key presses match the target sequence?
        Returns: true if it does match, false if it does not.
        """
        return self.key_sequence == self.target_sequence

    def reset(self):
        """
        Remove all keystrokes from the key sequence.
        """
        self.key_sequence = []