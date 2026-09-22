from pynput.keyboard import Controller, Key
from delays import Delay
import numpy as np

adjacent_keys = {
    "q": "weasz",
    "w": "qerasdx",
    "e": "qwrtsdfc",
    "r": "wetydfgv",
    "t": "eryufghb",
    "y": "rtuighjn",
    "u": "tyiohjkm",
    "i": "yuopjkl",
    "o": "uipkl",
    "p": "iol[",
    "a": "qwsdzx",
    "s": "qweadfzxc",
    "d": "werasfgxcv",
    "f": "ertsdghcvb",
    "g": "rtydfhjvbn",
    "h": "tyufgjkbnm",
    "j": "yuighklnm",
    "k": "uiohjlm",
    "l": "iopjk;",
    "z": "qasxc",
    "x": "wasdzcv",
    "c": "esdfzxvb ",
    "v": "rdfgxcbn ",
    "b": "tfghcvnm ",
    "n": "yghjvbm ",
    "m": "uhjkbn ,."
}


class Typos:
    def __init__(self, keyboardController: Controller, delayController: Delay):
        self.keyboardController = keyboardController
        self.delayController = delayController

    def random(self, current_key: str):
        function_list = [self.substitute_adjacent_keys, self.key_repeat]
        func = np.random.choice(function_list)
        func(current_key)


    def substitute_adjacent_keys(self, current_key: str):
        new_key = np.random.choice(list(adjacent_keys[current_key.lower()]))
        if current_key.isupper():
            new_key = new_key.upper()
        self.keyboardController.press(new_key)
        self.keyboardController.release(new_key)
        self.delayController.wait(0.4)
        self.keyboardController.press(Key.backspace)
        self.keyboardController.release(Key.backspace)
        self.delayController.backspace()
        self.keyboardController.press(current_key)
        self.keyboardController.release(current_key)
        self.delayController.next()
        self.delayController.wait()

    def key_repeat(self, current_key: str):
        num_of_repeats = np.random.geometric(0.8) + 1
        for _ in range(num_of_repeats):
            self.keyboardController.press(current_key)
            self.keyboardController.release(current_key)
            self.delayController.next()
            self.delayController.wait()

        self.delayController.wait(0.4)
        for _ in range(num_of_repeats - 1):
            self.keyboardController.press(Key.backspace)
            self.keyboardController.release(Key.backspace)
            self.delayController.backspace()

    def capitalization_error(self, current_word: str):
        len_before_detect = min(np.random.poisson(3), len(current_word))

        for i in range(len_before_detect):
            self.keyboardController.press(current_word[i].upper())
            self.keyboardController.release(current_word[i].upper())
            self.delayController.next()
            self.delayController.wait()

        self.delayController.wait(0.4)
        for _ in range(len_before_detect - 1):
            self.keyboardController.press(Key.backspace)
            self.keyboardController.release(Key.backspace)
            self.delayController.backspace()
