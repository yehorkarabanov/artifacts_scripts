from settings import settings
from character_controller import CharacterController
from bank import Bank


class GameController:
    def __init__(self):
        self.bank = Bank()

        self.character_list = []
        for name in settings.CHARACTER_NAMES:
            character = CharacterController(name)
            self.character_list.append(character)

    def find_character_with_highest_level(self, characteristic):
        character_top = self.character_list[0]
        for character in self.character_list:
            if (
                character.character[f"{characteristic}_level"]
                > character_top.character[f"{characteristic}_level"]
            ):
                character_top = character
        return character_top

    def main_loop_start(self):
        pass
