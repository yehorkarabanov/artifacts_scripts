from settings import settings
from character_controller import CharacterController
from actionqueue import ActionQueue


class GameController:
    def __init__(self):
        # self.bank = Bank()

        self.character_list = []
        for name in settings.CHARACTER_NAMES:
            character = CharacterController(name)
            self.character_list.append(character)

        self.action_queue = ActionQueue(self.character_list)

    def find_character_with_highest_level(self, characteristic):
        character_top = self.character_list[0]
        for character in self.character_list:
            if (
                character.data[f"{characteristic}_level"]
                > character_top.data[f"{characteristic}_level"]
            ):
                character_top = character
        return character_top

    def main_loop_start(self):
        pass
