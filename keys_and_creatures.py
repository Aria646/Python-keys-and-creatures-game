# DO NOT modify or add any import statements
from support import *
from display import KCView

# Name:Chenzhao Zhu
# Favorite Author: Leo Tolstoy
# -----------------------------------------------------------------------------

# Define your classes and functions here

class Tile:
    """
    Abstract class Tile.
    """
    
    def __init__(self):
        """Instantiate a new tile."""
        pass
    
    def __str__(self) -> str:
        """Returns the identifier that represents this tile."""
        return TILE_ID
    
    def __repr__(self) -> str:
        """
        Returns a string which could be copied and pasted into a REPL to 
        construct a new instance identical to self.
        """
        return f"{self.__class__.__name__}()"
    
    def is_blocking(self) -> bool:
        """Returns if this tile is blocking or not."""
        # Abstract tiles are not blocking
        return False


class Floor(Tile):
    """
    Class Floor, a non-blocking tile, representing walkable ground.
    """
    
    def __str__(self) -> str:
        """Returns the identifier that represents this tile."""
        # need override
        return FLOOR_ID


class Wall(Tile):
    """
    Class Wall, a blocking tile, representing impassable dungeon walls.
    """
    
    def __str__(self) -> str:
        """Returns the identifier that represents this tile."""
        # need override
        return WALL_ID
    
    def is_blocking(self) -> bool:
        """Returns if this tile is blocking or not."""
        # Abstract tile is non-blocking, wall is blocking, need override
        return True


class Door(Tile):
    """
    Class Door, a tile that represents a goal for the player.
    Can be open or closed
    """
    
    def __init__(self, is_open: bool):
        """
        Initialise a new Door instance with parameter `is_open`
        
        Parameter:
            is_open (bool): the door is open or not
        """
        super().__init__()
        # add slash to avoid conflict with method name
        self._is_open = is_open
    
    def __str__(self) -> str:
        """Returns the identifier that represents this tile."""
        return OPEN_ID if self._is_open else DOOR_ID
    
    def __repr__(self) -> str:
        """
        Returns a string which could be copied and pasted into a REPL to 
        construct a new instance identical to self.
        """
        return f"{self.__class__.__name__}({self._is_open})"
    
    def is_blocking(self) -> bool:
        """Returns if this tile is blocking or not."""
        return not self._is_open
    
    def is_open(self) -> bool:
        """Return if this door is currently open or not."""
        return self._is_open
    
    def set_open(self, is_open: bool):
        """
        Set the door to be open or closed.
        
        Parameter:
            is_open (bool): the door is open or not
        """
        self._is_open = is_open


class Entity:
    """
    Abstract class Entity.
    """
    
    def __init__(self, pos: Position, speed: int, magic: int):
        """
        Instantiate a new entity with  position, speed, and magic
        
        Parameter:
            pos (Position): Position of the entity
            speed (int): Speed of the entity
            magic (int): Magic of the entity
        """
        self._pos = pos
        self._speed = speed
        self._magic = magic
    
    def __repr__(self) -> str:
        """
        Returns a string which could be copied and pasted into a REPL to 
        construct a new instance identical to self.
        """
        return f"{self.__class__.__name__}" + \
            f"({self._pos}, {self._speed}, {self._magic})"
    
    def __str__(self) -> str:
        """
        Returns this entities identifier, row, column, speed, and magic.
        """
        return f"{self.get_id()},{self._pos[0]},{self._pos[1]}," + \
            f"{self._speed},{self._magic}"
    
    def get_id(self) -> str:
        """Returns the single character that represents this entity."""
        return ENTITY_ID
    
    def get_position(self) -> Position:
        """Returns this entity's position"""
        return self._pos
    
    def set_position(self, new_pos: Position):
        """
        Set this entity's position.
        
        Parameter:
            new_pos (Position): New position for the entity
        """
        self._pos = new_pos
    
    def get_speed(self) -> int:
        """Returns this entity's speed."""
        return self._speed
    
    def set_speed(self, new_speed: int):
        """
        Set this entity's speed
        
        Parameter:
            new_speed (int): New speed for the entity
        """
        self._speed = new_speed
    
    def get_magic(self) -> int:
        """Returns this entity's magic."""
        return self._magic
    
    def set_magic(self, new_magic: int):
        """
        Set this entity's magic.
        
        Parameter:
            new_magic (int): New magic for the entity
        """
        self._magic = new_magic


class Player(Entity):
    """
    Class Player, an entity controlled by the player. Can be attacked 
    by creatures.
    """
    
    def __init__(self, pos: Position, speed: int, magic: int, health: int):
        """
        Instantiate a new player with position, speed, magic, and health.
        
        Parameter:
            pos (Position): Position of the player
            speed (int): Speed of the player
            magic (int): Magic of the player
            health (int): Health of the player
        """
        super().__init__(pos, speed, magic)
        self._health = health
    
    def __repr__(self) -> str:
        """
        Returns a string which could be copied and pasted into a REPL to 
        construct a new instance identical to self.
        """
        return f"{self.__class__.__name__}({self._pos}, " + \
            f"{self._speed}, {self._magic}, {self._health})"
    
    def __str__(self) -> str:
        """
        Returns this player's identifier, row, column, speed, magic, and 
        health.
        """
        return f"{self.get_id()},{self._pos[0]},{self._pos[1]}," + \
            f"{self._speed},{self._magic},{self._health}"
    
    def get_id(self) -> str:
        """Returns the single character that represents this player."""
        return PLAYER_ID
    
    def get_health(self) -> int:
        """Returns this player's health."""
        return self._health
    
    def set_health(self, new_health: int):
        """
        Set this player's health.
        
        Parameter:
            new_health (int): new health for the player
        """
        self._health = new_health
    
    def is_alive(self) -> bool:
        """Returns True if this player is alive, and False otherwise."""
        return self._health > 0
    
    def adjacent_positions(self) -> tuple[Position]:
        """
        Returns a tuple containing the positions directly adjacent to this 
        player. Diagonal positions are not considered adjacent. Order: above,
        left, right, below.
        """
        row, col = self._pos
        return (
            (row - 1, col),  # Above
            (row, col - 1),  # Left
            (row, col + 1),  # Right
            (row + 1, col)   # Below
        )


class Creature(Entity):
    """
    Class Creature, an entity with some level of autonomy. They can select 
    movement directions to bring them closer to their target.
    """
    
    def get_id(self) -> str:
        """Returns the single character that represents this creature."""
        return CREATURE_ID
    
    def choose_move(self, target: Entity) -> str:
        """
        Return the movement direction that would result in the smallest 
        euclidean distance to the given target.
        
        Parameter:
            target (Entity): the target entity to move towards
            
        Returns:
            str: the direction to move
        """
        current_pos = self.get_position()
        target_pos = target.get_position()
        directions = [UP, LEFT, RIGHT, DOWN]
        min_distance = float('inf')
        select_move = UP
        
        # Find the best move that minimizes the distance to the target
        for direction in directions:
            delta = DELTAS[direction]
            new_pos = (current_pos[0] + delta[0], current_pos[1] + delta[1])
            distance = euclidean_distance(new_pos, target_pos)
            if distance < min_distance:
                min_distance = distance
                select_move = direction

        return select_move


class Item(Tile):
    """
    Abstract class Item, a special type of non-blocking tile.
    """
    
    def __init__(self, consumed: bool):
        """
        Instantiate a new Item with parameter `consumed`
        
        Parameter:
            consumed (bool): the item is consumed or not
        """
        super().__init__()
        self._consumed = consumed
    
    def __repr__(self) -> str:
        """
        Returns a string which could be copied and pasted into a REPL to 
        construct a new instance identical to self.
        """
        return f"{self.__class__.__name__}({self._consumed})"
    
    def __str__(self) -> str:
        """Returns the identifier that represents this item."""
        if self._consumed:
            return PICKED_ID
        return ITEM_ID
    
    def is_consumed(self) -> bool:
        """Returns True if this item is consumed, and False otherwise."""
        return self._consumed
    
    def pick_up(self, entity: Entity):
        """
        Attempts to have the given entity pick up and consume this item, 
        applying any relevant effects. Does nothing if the item has already 
        been consumed.
        
        Parameter:
            entity (Entity): the entity attempting to pick up the item
        """
        if not self._consumed:
            self._consumed = True
        # Generic items have no effect


class SpeedPotion(Item):
    """
    Class SpeedPotion, an item that increases the speed of the entity that 
    picked it up by 1.
    """
    
    def __str__(self) -> str:
        """Returns the identifier that represents this item."""
        if self._consumed:
            return PICKED_ID
        return SPEED_ID
    
    def pick_up(self, entity: Entity):
        """
        Attempts to have the given entity pick up and consume this item, 
        increasing the entity's speed by 1. Does nothing if the item has 
        already been consumed.
        
        Parameter:
            entity (Entity): The entity attempting to pick up the item
        """
        if not self._consumed:
            self._consumed = True
            # speed increase by 1
            entity.set_speed(entity.get_speed() + 1)


class MagicPotion(Item):
    """
    Class MagicPotion, an item that increases the magic of the entity that 
    picked it up by 1.
    """
    
    def __str__(self) -> str:
        """Returns the identifier that represents this item."""
        if self._consumed:
            return PICKED_ID
        return MAGIC_ID
    
    def pick_up(self, entity: Entity):
        """
        Attempts to have the given entity pick up and consume this item, 
        increasing the entity's magic by 1. Does nothing if the item has 
        already been consumed.
        
        Parameter:
            entity (Entity): The entity attempting to pick up the item
        """
        if not self._consumed:
            self._consumed = True
            # magic increase by 1
            entity.set_magic(entity.get_magic() + 1)


class Key(Item):
    """
    Class Key, a special item that can only be picked up by player entities.
    They have no direct effect when picked up.
    """
    
    def __str__(self) -> str:
        """Returns the identifier that represents this item."""
        if self._consumed:
            return PICKED_ID
        return KEY_ID
    
    def pick_up(self, entity: Entity):
        """
        Attempts to have the given entity pick up and consume this item. 
        Only player entities can pick up keys, and keys have no effect when
        picked up.
        
        Parameter:
            entity (Entity): The entity attempting to pick up the item
        """
        # only players can pick up keys
        if not self._consumed and isinstance(entity, Player):
            self._consumed = True
        # keys have no effect when picked up


class Dungeon:
    """
    Class Dungeon, represents a level of Keys and Creatures. A dungeon is 
    structured as a rectangular set of tiles.
    """
    
    def __init__(self, tiles: list[list[Tile]]):
        """
        Instantiate a dungeon with the given tiles
        
        Parameter:
            tiles (list[list[Tile]]): 2d list of tiles
        """
        self._tiles = tiles
    
    def __repr__(self) -> str:
        """
        Returns a string which could be copied and pasted into a REPL to 
        construct a new instance identical to self.
        """
        return f"Dungeon({self._tiles!r})"
    
    def __str__(self) -> str:
        """
        Returns the string representation of each tile in the dungeon
        """
        return '\n'.join(''.join(str(tile) for tile in row) 
                         for row in self._tiles)
    
    def get_tiles(self) -> list[list[Tile]]:
        """
        Returns the structured set of tiles representing this dungeon.
        """
        return self._tiles
    
    def get_doors(self) -> dict[Position, Door]:
        """
        Returns a dictionary containing all doors within the dungeon.
        """
        doors = {}
        for i, row in enumerate(self._tiles):
            for j, tile in enumerate(row):
                if isinstance(tile, Door):
                    doors[(i, j)] = tile
        return doors
    
    def get_items(self) -> dict[Position, Item]:
        """
        Returns a dictionary containing all items within the dungeon.
        """
        items = {}
        for i, row in enumerate(self._tiles):
            for j, tile in enumerate(row):
                if isinstance(tile, Item):
                    items[(i, j)] = tile
        return items
    
    def keys_remaining(self) -> int:
        """
        Returns the number of keys that have not yet been picked up within 
        this dungeon.
        """
        num = 0
        for row in self._tiles:
            for tile in row:
                if isinstance(tile, Key) and not tile.is_consumed():
                    num += 1
        return num
    
    def open_doors(self):
        """
        Open all doors within this dungeon.
        """
        for door in self.get_doors().values():
            door.set_open(True)


class KCModel:
    """
    Class KCModel, models the logical state of a game of Keys and Creatures.
    """
    
    def __init__(self, dungeon: Dungeon,
                 player: Player,
                 creatures: list[Creature]):
        """
        Instantiates a new KCModel with dungeon, player, and creatures.
        
        Parameter:
            dungeon (Dungeon): the dungeon instance
            player (Player): the player instance
            creatures (list[Creature]): list of creatures
        """
        self._dungeon = dungeon
        self._player = player
        self._creatures = creatures
    
    def __repr__(self) -> str:
        """
        Returns a string which could be copied and pasted into a REPL to 
        construct a new instance identical to self.
        """
        return f"KCModel({self._dungeon!r}, " + \
            f"{self._player!r}, {self._creatures!r})"
    
    def __str__(self) -> str:
        """
        Returns the string representation of the dungeon.
        """
        tiles = self._dungeon.get_tiles()
        result = []
        
        for i, row in enumerate(tiles):
            row_str = ""
            for j, tile in enumerate(row):
                pos = (i, j)
                # Check if player is at this position
                if self._player.get_position() == pos:
                    row_str += self._player.get_id()
                # Check if any creature is at this position
                elif any(creature.get_position() == pos 
                         for creature in self._creatures):
                    row_str += CREATURE_ID
                # Otherwise, use the tile's string representation
                else:
                    row_str += str(tile)
            result.append(row_str)
        return '\n'.join(result)
    
    def get_dungeon(self) -> Dungeon:
        """
        Return this model's dungeon instance.
        """
        return self._dungeon
    
    def get_player(self) -> Player:
        """
        Return this model's player instance.
        """
        return self._player
    
    def get_creatures(self) -> list[Creature]:
        """
        Return this model's creatures, in decreasing order of priority.
        """
        return self._creatures
    
    def has_won(self) -> bool:
        """
        Return True if the player has won the game, and False otherwise.
        Player wins when alive and on an open door.
        """
        # check player alive
        if not self._player.is_alive():
            return False
        
        player_pos = self._player.get_position()
        doors = self._dungeon.get_doors()
        
        if player_pos in doors:
            # player alive and on a door
            return doors[player_pos].is_open()
        
        return False
    
    def has_lost(self) -> bool:
        """
        Return True if the player has lost the game, and False otherwise.
        Player loses when not alive.
        """
        return not self._player.is_alive()
    
    def move_entity(self, entity: Entity, move: str):
        """
        Moves the given entity in the direction specified by move.
        
        Parameter:
            entity (Entity): The entity to move
            move (str): The direction to move (up, down, left, right, or wait)
        """
        delta = DELTAS[move]
        speed = entity.get_speed()
        row_n = len(self._dungeon.get_tiles())
        col_n = len(self._dungeon.get_tiles()[0])
        
        for _ in range(speed):
            current_pos = entity.get_position()
            new_pos = (current_pos[0] + delta[0], current_pos[1] + delta[1])
            
            # Check if new position is valid
            tiles = self._dungeon.get_tiles()
            if not (0 <= new_pos[0] < row_n and 0 <= new_pos[1] < col_n):
                break
            
            # Check if tile at new position is blocking
            tile = tiles[new_pos[0]][new_pos[1]]
            if tile.is_blocking():
                break
            
            # Check if another entity is at new position
            if self._player.get_position() == new_pos and entity != self._player:
                break
            if any(creature.get_position() == new_pos and creature != entity 
                   for creature in self._creatures):
                break
            
            entity.set_position(new_pos)
        
        # Try to pick up item at final position
        current_pos = entity.get_position()
        items = self._dungeon.get_items()
        if current_pos in items:
            items[current_pos].pick_up(entity)
            # Check if all keys are picked up
            if self._dungeon.keys_remaining() == 0:
                self._dungeon.open_doors()
    
    def make_move(self, move: str):
        """
        Performs the player's desired action, then each creature moves.
        
        Parameter:
            move (str): The direction for the player to move
        """
        # Player moves first
        self.move_entity(self._player, move)
        
        # Each creature moves in priority order
        new_creatures = []
        for creature in self._creatures:
            creature_alive = True
            # Creature moves towards player
            direction = creature.choose_move(self._player)
            self.move_entity(creature, direction)
            
            # Check if creature is adjacent to player and attacks
            creature_pos = creature.get_position()
            if creature_pos in self._player.adjacent_positions():
                # Creature attacks player
                if self._player.get_magic() <= creature.get_magic():
                    # Player loses health
                    self._player.set_health(self._player.get_health() - 1)
                else:
                    # Player expends magic and teleports creature away
                    self._player.set_magic(self._player.get_magic() - 1)
                    creature_alive = False
            # use a new list to avoid modifying the list while iterating
            if creature_alive:
                new_creatures.append(creature)
        self._creatures = new_creatures


def _tile_id_to_instance(tile_id: str) -> Tile:
    """
    Helper function to convert a tile identifier to a Tile instance.
    
    Parameter:
        tile_id (str): The identifier of the tile.
        
    Returns:
        Tile: The corresponding Tile instance. None if the identifier is
                invalid.
    """
    if tile_id == FLOOR_ID:
        return Floor()
    elif tile_id == WALL_ID:
        return Wall()
    elif tile_id == DOOR_ID:
        return Door(False)
    elif tile_id == OPEN_ID:
        return Door(True)
    elif tile_id == KEY_ID:
        return Key(False)
    elif tile_id == PICKED_ID:
        return Item(True)
    elif tile_id == SPEED_ID:
        return SpeedPotion(False)
    elif tile_id == MAGIC_ID:
        return MagicPotion(False)
    elif tile_id == ITEM_ID:
        return Item(False)
    elif tile_id == TILE_ID:
        return Tile()
    else:
        return None


def load_model(file: str) -> KCModel:
    """
    Attempts to load a KCModel from the file located at the specified path.
    
    Parameter:
        file (str): Path to the file containing the game state.
        
    Returns:
        KCModel: The loaded game model
        
    Raises:
        ValueError: If the file contains invalid data
    """
    with open(file, "r") as f:
        content = f.read()

    parts = content.split('\n\n')
    dungeon_content = parts[0]
    entity_contents = parts[1].strip().split('\n')
    
    # Parse dungeon
    dungeon_rows = dungeon_content.split('\n')
    tiles = []
    for row_str in dungeon_rows:
        row = []
        for char in row_str:
            tile_instance = _tile_id_to_instance(char)
            if tile_instance is None:
                raise ValueError(INVALID_TILE_MSG)
            row.append(tile_instance)
        tiles.append(row)
    dungeon = Dungeon(tiles)
    
    # Parse player
    player_line = entity_contents[0]
    player_params = player_line.split(',')
    try:
        if player_params[0] != PLAYER_ID:
            raise ValueError(INVALID_PLAYER_MSG)
        row = int(player_params[1])
        col = int(player_params[2])
        speed = int(player_params[3])
        magic = int(player_params[4])
        health = int(player_params[5])
        player = Player((row, col), speed, magic, health)
    except (ValueError, IndexError):
        raise ValueError(INVALID_PLAYER_MSG)
    
    # Parse creatures
    creatures = []
    for i in range(1, len(entity_contents)):
        creature_line = entity_contents[i]
        creature_params = creature_line.split(',')
        try:
            if creature_params[0] != CREATURE_ID:
                raise ValueError(INVALID_CREATURE_MSG)
            row = int(creature_params[1])
            col = int(creature_params[2])
            speed = int(creature_params[3])
            magic = int(creature_params[4])
            creatures.append(Creature((row, col), speed, magic))
        except (ValueError, IndexError):
            raise ValueError(INVALID_CREATURE_MSG)
    
    return KCModel(dungeon, player, creatures)


class KCController:
    """
    Controller class for the overall game of Keys and Creatures.
    """
    
    def __init__(self, initial_state: KCModel):
        """
        Instantiates the controller using the given state.
        
        Parameter:
            initial_state (KCModel): The initial game state
        """
        self._model = initial_state
        self._view = KCView()
    
    def __repr__(self) -> str:
        """
        Returns a string which could be copied and pasted into a REPL to 
        construct a new instance identical to self.
        """
        return f"KCController({self._model!r})"
    
    def __str__(self) -> str:
        """
        Returns the string representation of the model instance.
        """
        return str(self._model)
    
    def print_game(self):
        """
        Update the display by printing out the current game state.
        """
        tiles = self._model.get_dungeon().get_tiles()
        player = self._model.get_player()
        creatures = self._model.get_creatures()
        self._view.draw_game(tiles, player, creatures)
    
    def load_game(self, file: str):
        """
        Replace the current game state with the state contained in file.
        
        Parameter:
            file (str): Path to the file containing the game state
            
        Raises:
            ValueError: If the file contains invalid data
        """
        self._model = load_model(file)
    
    def get_command(self) -> str:
        """
        Repeatedly prompts the user until they enter a valid command.
        
        Returns:
            str: The first valid command entered by the user (in lowercase)
        """
        simple_commands = {HELP, QUIT, WAIT}
        valid_dirs = {UP, DOWN, LEFT, RIGHT}
        
        while True:
            command = input(COMMAND_PROMPT).lower()
            # simple commands
            if command in simple_commands:
                return command
            # move commands
            if command[:4] == MOVE and len(command) > 5 \
                and command[5:] in valid_dirs:
                return command
            # load commands
            if command[:4] == LOAD and len(command) > 5 \
                and command[4] == ' ' and ' ' not in command[5:]:
                return command
            # invalid command
            print(INVALID_COMMAND_MSG)
    
    def play(self):
        """
        Conducts a game of Keys and Creatures from start to finish.
        """
        # Initial display
        self.print_game()
        print(WELCOME_MSG)
        
        # Main game loop
        while not self._model.has_won() and not self._model.has_lost():
            command = self.get_command()
            cmds = command.split()
            update_flag = True
            
            if cmds[0] == HELP:
                print(HELP_MSG)
            elif cmds[0] == QUIT:
                return
            elif cmds[0] == WAIT:
                self._model.make_move(WAIT)
            elif cmds[0] == MOVE:
                direction = cmds[1]
                self._model.make_move(direction)
            elif cmds[0] == LOAD:
                file_path = cmds[1]
                try:
                    self.load_game(file_path)
                    print(LOAD_MSG)
                except FileNotFoundError:
                    print(FILE_NOT_FOUND_MSG)
                    update_flag = False
                except ValueError as e:
                    print(str(e))
                    update_flag = False
            else:
                update_flag = False
            # Update display after each valid command
            if update_flag:
                self.print_game()
        
        # Game over
        if self._model.has_won():
            print(WIN_MSG)
        else:
            print(LOSE_MSG)


def play_game(file: str):
    """
    Load a game state from file and play a game of Keys and Creatures
    
    Parameter:
        file (str): Path to the file containing the initial game state
    """
    model = load_model(file)
    controller = KCController(model)
    controller.play()


def main() -> None:
    """
    Main function to run the game.
    """
    play_game('levels/level1.txt')


if __name__ == "__main__":
    main()
