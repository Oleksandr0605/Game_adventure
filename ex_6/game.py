"""
Game
"""
import random

class Weapon:
    """
    Weapon class that every person can hold

    Attributes:
        name: name of this weapon
        damage: how many health this weapon can take
    >>> w = Weapon("Sword", "right")
    >>> assert str(w) == "Sword, damage: {}".format(w.damage)
    """
    def __init__(self, name: str, strong_side: str) -> None:
        self.name = name
        self.strong_side = strong_side
        self.damage = random.randint(1, 12)

    def __str__(self) -> str:
        return f"{self.name}, damage: {self.damage}"


class Bonus:
    """
    Bonus class that can add health to the player

    Attributes:
        health: amount of health in bonus
    >>> b = Bonus()
    >>> assert b.health >= 20 and b.health <= 30
    """
    def __init__(self) -> None:
        self.health = random.randint(20, 30)


class Person:
    """
    Person class

    Attributes:
        name: name of  this person
        phrase: what person talk to you at the meeting
        weapon: object of class Weapon that person holds
        damage: person's damage with weapon
    >>> p = Person("Alice", "Hello, nice to meet you!")
    >>> assert p.name == "Alice"
    >>> assert p.phrase == "Hello, nice to meet you!"
    """
    def __init__(self, name: str, phrase: str) -> None:
        self.name = name
        self.phrase = phrase


class Friend(Person):
    """
    Friend class, that can be with player

    Attributes:
        all that have Person
    """
    def __init__(self, name: str, phrase: str, weapon = None) -> None:
        super().__init__(name, phrase)
        self.weapon = weapon
        self.damage = 1

    def add_weapon(self, weapon: Weapon) -> None:
        """
        Self gets weapon
        """
        self.weapon = weapon


class Enemy(Person):
    """
    Enemy class, that can attack player

    Attributes:
        all that have Person
        health: health of the enemy
        damage: damage of the enemy
    """
    def __init__(self, name: str, phrase: str, clas: str) -> None:
        super().__init__(name, phrase)
        self.health = random.randint(50, 65)
        self.damage = random.randint(10, 12)
        self.clas = clas

    def fight(self, player):
        """
        Simulate the fight with enemy
        """
        print(f"Клас ворога: {self.clas}. В нього {self.health} життя")
        player.choose_weapon()
        while self.health > 0 and player.health > 0:
            if player.weapon.strong_side == self.clas:
                self.health -= int(player.player_damage() * (3 / 2))
            else:
                self.health -= player.player_damage()
            player.health -= self.damage
        if player.health > 0:
            print(f"Ти переміг! В тебе залишилось {player.health} життя.\n")
        else:
            print("Ти вмер(")


class Room:
    """
    Room class. In this room player can walk

    Attributes:
        south_room, north_room, west_room, east_room: other rooms that player can visit
        goods: list of goods (weapon or bonuses)
        person: person (friend or enemy)
        name: number of the room

    >>> goods = [Weapon("sword", "melee"), Weapon("bow", "ranged")]
    >>> person = Friend("John", "hehe")
    >>> room = Room(goods, person, "living room", None, "dining room")
    >>> room.name
    \'living room\'
    >>> room.goods[0].name
    \'sword\'
    >>> room.view_rooms()
    \'down room\'
    >>> room.view_rooms(goto=True, inp="down room")
    \'dining room\'
    """
    def __init__(self, goods: list, person, name: str, up_room = None,\
                 down_room = None, left_room = None, right_room = None,) -> None:
        self.up_room = up_room
        self.down_room = down_room
        self.left_room = left_room
        self.right_room = right_room
        self.goods = goods
        self.person = person
        self.name = name
        self.visited = False

    def view_weapon(self) -> str:
        """
        Shows weapon in room
        """
        return ''.join("".join(("- ", weapon.name,\
                                " (damage: ", str(weapon.damage),\
                                ", сильна сторона: ", weapon.strong_side, ")\n"\
                              )) for weapon in self.goods)

    def view_rooms(self, inp = "", goto = False):
        """
        Shows all avaliable rooms
        """
        rooms = {}
        rooms["up room"] = self.up_room
        rooms["down room"] = self.down_room
        rooms["left room"] = self.left_room
        rooms["right room"] = self.right_room
        if goto:
            return rooms[inp]
        return ', '.join([elm for elm in rooms.keys() if rooms[elm] != None])


class Field:
    """
    Field class. Save all data about field in list of rooms

    Attributes:
        rooms: matrix of rooms
        size: size of field
    """
    def __init__(self, rooms: list[Room], size: int) -> None:
        self.rooms = rooms
        self.size = size

class Bag:
    """
    Bag class. It can store weapon.

    Attributes:
        weapons: list of weapons
    """
    def __init__(self, weapons = []) -> None:
        self.weapons = weapons

    def add_weapon(self, weapon: Weapon) -> None:
        """
        Add weapon to bag
        """
        self.weapons.append(weapon)

    def view_weapon(self) -> str:
        """
        Shows list of weapon
        """
        return ''.join("".join(("\n- ", weapon.name,\
                                " (damage: ", str(weapon.damage),\
                                ", сильна сторона: ", weapon.strong_side, ")"\
                              )) for weapon in self.weapons)

    def give_weapon(self, player):
        """
        Removes weapon from bag and return it
        """
        flag = True
        while flag:
            try:
                ind = int(input(">>> "))
                player.friends[-1].add_weapon(self.weapons[ind - 1])
                self.weapons.pop(ind - 1)
                print(f"Тепер {player.friends[-1].name} має {player.friends[-1].weapon.name}\n")
                flag = False
            except:
                print("Не коректне число, введи ще раз")

class Player:
    """
    Player class

    Attributes:
        room: room where player is placed
        friends: list of player's friends
        bag: bag where player store weapons
        health: player's health
        weapon: weapon that player holds
    """
    def __init__(self, room: Room, friends: list[Friend], bag: Bag, weapon: Weapon) -> None:
        self.room = room
        self.friends = friends
        self.bag = bag
        self.health = 100
        self.weapon = weapon

    def choose_weapon(self):
        """
        Give an oportunity to choose weapon
        """
        print("Обери якою зброєю ти хочеш битися: ")
        print(self.bag.view_weapon())
        flag = True
        while flag:
            try:
                self.weapon = self.bag.weapons[int(input(">>> ")) - 1]
                print(f"Ти взяв у руки {self.weapon.name}. У бій!\n")
                input()
                flag = False
            except:
                print("Не коректне число, введи ще раз")

    def player_damage(self):
        """
        Calculate player damage
        """
        return self.weapon.damage + sum([elm.weapon.damage for elm in self.friends])

    def view_friends(self) -> str:
        """
        Returns the info about player's friends
        """
        return ''.join("".join(("\n- ", friend.name,\
                                " (weapon: ", str(friend.weapon), ")"\
                              )) for friend in self.friends)


def generate_goods() -> list:
    """
    Returns list of goods (bonuses, weapon) that will be in room
    """
    goods = []
    weapon_name = {"нечиста сила": ["Свята вода", "Хрест", "Кадило", "Молитва",\
                                    "Китайський чай з Аліекспресу"],\
                   "неприємний монстр": ["Пес Патрон", "Гарпун водолаза", "Вилка", "Сковорідка",\
                                      "Нашийник", "Вонючий носок (вонючіший ніж монстр)"],\
                   "цивільний": ["Молоток судді", "Заява в поліцію",\
                                 "Шланг пожежника", "Цивільний кодекс", "Розпечена смола"]}
    goods.append(Bonus())
    num = random.randint(2, 4)
    for _ in range(num):
        strong_side = random.choice(list(weapon_name.keys()))
        name = random.choice(weapon_name[strong_side])
        goods.append(Weapon(name, strong_side))
    return goods


def generate_person() -> Enemy:
    """
    Returns the random enemy or the Friend.
    """
    num = random.randint(1, 2)
    clases_enemy_names = {"нечиста сила": ["Єретик", "Скейтер", "Наркоман", "Сатаніст"],\
                          "неприємний монстр": ["Москаль", "Янукович", "Білка зі сказом",\
                                             "Тарган гігант (Таргант)"],\
                          "цивільний": ["Крадій дітей", "Зла продавщиця (тьотя Валя)", "Безхатько",\
                                        "Чоловік з агресивною собакою", "Грицак і Джеджора"]}
    clases_friend_names = ["Борис Ґудзяк", "Степан Фединяк", "сестра Антонія",\
                           "сестра Єлена", "Магістр", "Костя Грицюк", "Петро Мозіль",\
                           "Микола Висоцький"]
    if num == 1:
        clas = random.choice(list(clases_enemy_names.keys()))
        name = random.choice(clases_enemy_names[clas])
        return Enemy(name, "hehehe", clas)
    else:
        name = random.choice(clases_friend_names)
        return Friend(name, "Привіт, я допоможу тобі, тепер я твій друг")


def generate_field(size) -> list[Room]:
    """
    Generates field with rooms with size: size x size.
    """
    rooms = []
    for ind in range(size):
        temp = []
        for jnd in range(size):
            temp.append(Room(generate_goods(), generate_person(), str(ind) + str(jnd)))
        rooms.append(temp)
    for ind in range(size):
        for jnd in range(size):
            if ind != 0:
                rooms[ind][jnd].up_room = rooms[ind - 1][jnd]
            if ind != len(rooms) - 1:
                rooms[ind][jnd].down_room = rooms[ind + 1][jnd]
            if jnd != 0:
                rooms[ind][jnd].left_room = rooms[ind][jnd - 1]
            if jnd != len(rooms) - 1:
                rooms[ind][jnd].right_room = rooms[ind][jnd + 1]
    return rooms


def print_field(matrix, player):
    """
    Prints field with player placing and show which rooms are visited
    """
    matrix[int(player.room.name[0])][int(player.room.name[1])] = "P"
    print(f"\n\
-------------------------\n\
|00  {matrix[0][0]}|01  {matrix[0][1]}|02  {matrix[0][2]}|03  {matrix[0][3]}|\n\
|_____|_____|_____|_____|\n\
|10  {matrix[1][0]}|11  {matrix[1][1]}|12  {matrix[1][2]}|13  {matrix[1][3]}|\n\
|_____|_____|_____|_____|\n\
|20  {matrix[2][0]}|21  {matrix[2][1]}|22  {matrix[2][2]}|23  {matrix[2][3]}|\n\
|_____|_____|_____|_____|\n\
|30  {matrix[3][0]}|31  {matrix[3][1]}|32  {matrix[3][2]}|33  {matrix[3][3]}|\n\
|     |     |     |     |\n\
------------------------")


def visited_rooms(field: list[list[Room]]) -> bool:
    """
    Checks whether all rooms are visited
    """
    flag = False
    for rooms in field:
        for room in rooms:
            if not room.visited:
                flag = True
                break
    if flag:
        return True
    return False


def main():
    """
    """
    print("Привіт, радий вітати тебе у нашій грі")
    print("Натисни Enter щоби грати")
    input()
    field_size = 4
    field = Field(generate_field(field_size), field_size)
    weap = Weapon("Палка", "цивільний")
    player = Player(field.rooms[0][0], [], Bag(weapons=[weap]), weap)

    matrix = []
    for ind in range(field_size):
        temp = []
        for jnd in range(field_size):
            temp.append(" ")
        matrix.append(temp)

    print("Твій герой знаходиться в тій кімнаті де є буква P, V - там де вже був герой:")
    print_field(matrix, player)
    print("Тепер твоє завдання дослідити всі кімнати, щасти!")

    while visited_rooms(field.rooms):
        if not player.room.visited:
            player.room.visited = True
            print(f"\nЦе кімната {player.room.name}")
            print(f"Health: {player.health}")
            print(f"Weapon in bag:{player.bag.view_weapon()}")
            print(f"Friends: {player.view_friends()}\n")
            print(f"Ти заходиш в кімнату, а посеред неї стоїть {player.room.person.name}")
            print(f"\'{player.room.person.phrase}\'\n")

            if isinstance(player.room.person, Friend):
                player.friends.append(player.room.person)
                print("Обери яку зброю ти хочеш дати своєму другові: ")
                print(player.bag.view_weapon())
                player.bag.give_weapon(player)
            else:
                player.room.person.fight(player)

            if player.health <= 0:
                return "Гра закінчена, ти програв"

            print(f"Вітаю, ти отримав бонус, він дає тобі {player.room.goods[0].health} \
одиниць життя!\n")
            player.health += player.room.goods.pop(0).health
            print(f"У цій кімнаті є:\n{player.room.view_weapon()}")
            print("Впиши номер зброї (починаючи від 1) яку ти б хотів забрати собі в рюкзак:")

            flag = True
            while flag:
                try:
                    player.bag.add_weapon(player.room.goods[int(input(">>> ")) - 1])
                    print(f"Ти взяв {player.bag.weapons[-1].name}")
                    flag = False
                except:
                    print("Не коректне число, введи ще раз")

            print("\nТепер ти можеш піти у іншу кімнату. Введи у яку ти хочеш піти:")
            print(player.room.view_rooms())
            matrix[int(player.room.name[0])][int(player.room.name[1])] = "V"
            flag = True
            while flag:
                try:
                    player.room = player.room.view_rooms(input(">>> "), True)
                    flag = False
                except:
                    print("Не коректна кімната, введи ще раз")
            print_field(matrix, player)

        else:
            print("Обери у яку кімнату хочеш піти: ")
            matrix[int(player.room.name[0])][int(player.room.name[1])] = "V"
            flag = True
            while flag:
                try:
                    player.room = player.room.view_rooms(input(">>> "), True)
                    flag = False
                except:
                    print("Не коректна кімната, введи ще раз")
            print_field(matrix, player)

    print("Вітаю! Ти Пройшов гру!")
    return None


if __name__ == "__main__":
    main()
    # import doctest
    # print(doctest.testmod())
