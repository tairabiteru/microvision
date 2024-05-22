"""Module handles the keystrokes which ultimately switch mics."""
import pynput


class Keyboard:
    """
    Class abstracts pynput's keyboard system.

    This basically just allows us a shortcut to pressing
    key combinations.
    """
    SPECIAL = {
        'ctrl': pynput.keyboard.Key.ctrl_l,
        'alt': pynput.keyboard.Key.alt_l,
        'shift': pynput.keyboard.Key.shift_l
    }

    def __init__(self):
        self.controller = pynput.keyboard.Controller()
    
    def send(self, keys):
        """
        Press then release a key combination.

        keys: str - The key combination to press, separated by
            spaces. Ex: "CTRL ALT SHIFT A" 
        """
        keys = list(map(lambda x: x.lower(), keys.split(" ")))
        for key in keys:
            if key in self.SPECIAL:
                self.controller.press(self.SPECIAL[key])
            else:
                self.controller.press(key)
        for key in keys:
            if key in self.SPECIAL:
                self.controller.release(self.SPECIAL[key])
            else:
                self.controller.release(key)