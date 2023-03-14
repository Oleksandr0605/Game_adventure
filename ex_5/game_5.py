"""
Module for game
"""

counter = 0
class Item:
    """
    """
    def __init__(self, name, description = None) -> None:
        self.name = name
        self.description = description

    def set_description(self, description) -> None:
        """
        Sets description
        """
        self.description = description

    def describe(self):
        """
        describes
        """
        print(f"The [{self.name}] is here - {self.description}")

    def get_name(self):
        """
        gets name
        """
        return self.name


class Character:
    """
    Character class
    """
    def __init__(self, name, describes, conversation = None, weakness = None) -> None:
        self.name = name
        self.describes = describes
        self.conversation = conversation
        self.weakness = weakness

    def set_conversation(self, conversation) -> None:
        """
        Sets conversations
        """
        self.conversation = conversation

    def set_weakness(self, weakness) -> None:
        """
        Sets weaknes
        """
        self.weakness = weakness

    def describe(self):
        """
        describes
        """
        print(f"{self.name} is here!\n{self.describes}")


class Room:
    """
    """
    def __init__(self, name, description = None, link = {},\
                 character = None, item = None) -> None:
        self.name = name
        self.description = description
        self.link = link
        self.character = character
        self.item = item

    def set_description(self, description) -> None:
        """
        Sets description
        """
        self.description = description

    def link_room(self, room, world: str) -> None:
        """
        links room
        """
        self.link[world] = room

    def set_character(self, character: Character) -> None:
        """
        Sets character
        """
        self.character = character

    def set_item(self, item: Item) -> None:
        """
        Set items
        """
        self.item = item

    def get_item(self) -> None:
        """
        Set items
        """
        return self.item


    def get_details(self) -> str:
        """
        returns details
        """
        prints = ""
        for key in self.link.keys():
            prints += f"The {self.link[key].name} is {key}.\n"
        print(f"{self.name}\n{self.description}\n\
--------------------\n\
{prints}")

    def get_character(self) -> None:
        """
        gets character
        """
        return self.character

    def move(self, command):
        """
        Moves
        """
        return self.link[command]


class Enemy(Character):
    """
    Enemy class
    """
    def __init__(self, name, conversation=None) -> None:
        super().__init__(name, conversation)

    def talk(self) -> None:
        """
        talks
        """
        print(f"[{self.name} says]: {self.conversation}")

    def fight(self, fight_with):
        """
        fights
        """
        if self.weakness == fight_with:
            counter += 1
            return True
        return False

    def get_defeated(self) -> int:
        """
        defeated
        """
        return counter