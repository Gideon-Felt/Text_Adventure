from dataclasses import dataclass, field
from rich.console import Console
from rich.table import Table


class GameMap:
    locations = {
        'The Forest': {
            'id': 1,
            'The Cabin': {
                'id': 5,
                'Cabin Entrance': {
                    'id': 7,
                    'The Living Room': {
                        'id': 8,
                    },
                    'Long Hallway': {
                        'id': 8,
                    },
                    'Short Hallway': {
                        'id': 10,
                    },
                    'The Kitchen': {
                        'id': 11,
                    },
                    'The Bathroom': {
                        'id': 12,
                    },
                    'The Bedroom': {
                        'id': 13,
                    },
                    'The Attic': {
                        'id': 14,
                    },
                    'The Closet': {
                        'id': 15,
                    },
                    'The Balcony': {
                        'id': 16,
                    },
                    'The Backyard': {
                        'id': 21,
                        'Secret Tunnel': {
                            'id': 22,
                            'The Cave': {
                                'id': 'The Forest.The Cave',
                            }
                        }
                    },
                },
                'The Mountain': {
                    'id': 6,
                    'Climb Mountain': {
                        'id': 17,
                        'The Mountain Temple': {
                            'id': 18,
                            'Enter Mountain Temple': {
                                'id': 19,
                            },
                        }
                    },
                    'Circle The Mountain': {
                        'id': 20,
                    }
                }
            },
            'The Cave': {
                'id': 2,
            },
            'The Pond': {
                'id': 3,
            },
            'The River': {
                'id': 4,
            },
        }
    }

    def get_available_locations(self, current_location):
        world_depth: list[str] = current_location.split('.')
        previous_path = world_depth[0]
        traced_path = dict({})
        string_path = ''
        for path in world_depth:
            string_path = string_path + '.' + path
            traced_path: dict = self.locations[path] if path == world_depth[0] else traced_path[path]
            if path == world_depth[-1]:
                previous_path = world_depth[-2] if len(world_depth) > 1 else path
                break

        string_path = string_path[1:]
        location_paths = list(
            filter(
                lambda i: i != 'id',
                list(set(([previous_path] if current_location != 'The Forest' else [])
                         +
                         list(map(
                             lambda i: string_path + '.' + i if i != 'id' else string_path,
                             list(traced_path.keys())))))))
        location_paths.sort()
        location_paths = list(filter(lambda i: f"{world_depth[-1]}.{world_depth[-1]}" not in i, location_paths))
        location_paths = list(filter(lambda i: i != current_location, location_paths))
        return location_paths

    def get_available_locations_trees(self):
        ...


@dataclass
class Item:
    is_weapon: bool = False
    is_eatable: bool = False
    is_usable: bool = False


@dataclass
class Inventory:
    weapon: Item = None
    food: list[Item] = None
    utilities: list[Item] = None


@dataclass
class Player:
    name: str = "Isaac"
    inventory: Inventory = Inventory()
    game_map = GameMap()
    location: str = "The Forest"
    choices: list[str] = field(default_factory=lambda: ['Inspect Area For Items', 'Navigate Elsewhere', 'Eat Food'])

    def player_info_prompt(self, console: Console) -> str:
        console.print(f"[bold cyan]{self.name} [white]- [yellow]({self.location.split('.')[-1]})")
        return console.input("[purple]?:")

    @staticmethod
    def generate_table_boiler_plate(title: str) -> Table:
        styled_two_column_table: Table = Table(title=title)
        styled_two_column_table.add_column("#", justify="right", style="cyan", no_wrap=False)
        styled_two_column_table.add_column("Choice", style="magenta")
        return styled_two_column_table

    def ask_choice(self, console, choices, recursion: bool = False, table: Table = None) -> int:
        if not table:
            console.print("\n".join([f'{i[0]}: {i[1]}' for i in enumerate(choices)]) + "\n")
            current_choice = str(self.player_info_prompt(console)).strip()
        else:
            _ = [table.add_row(f"{i[0]}", i[1]) for i in enumerate(choices) if not recursion]
            console.print(table)
            current_choice = self.player_info_prompt(console=console)

        if current_choice.isalpha():
            console.print(f'[bold red]choice must be an integer between 0 - {len(choices)}')
            current_choice = self.ask_choice(console=console, choices=choices, recursion=True, table=table)
            if recursion:
                return current_choice
        elif int(current_choice) > len(choices):
            console.print(f'[bold red]choice must be an integer between 0 - {len(choices)}')
            current_choice = self.ask_choice(console=console, choices=choices, recursion=True, table=table)
            if recursion:
                return current_choice
        return int(current_choice)

    def make_choice(self, console: Console, non_standard_choices: list = None):
        available_choices = non_standard_choices or self.choices
        navigation_table = self.generate_table_boiler_plate(title="Navigations Available are:")
        current_choice: int = self.ask_choice(console=console, choices=available_choices, table=navigation_table)
        # Player Choice is valid - Update World And Perform Player Choices
        if self.choices[current_choice] == 'Inspect Area For Items':
            console.print('[bold red]Not Yet Implemented')
        elif self.choices[current_choice] == 'Eat Food':
            console.print('[bold red]Not Yet Implemented')
        elif self.choices[current_choice] == 'Navigate Elsewhere':
            available_navigations: list[str] = self.game_map.get_available_locations(current_location=self.location)
            # available_navigations: list[str] = self.game_map.get_available_locations_trees(current_location=self.location)
            navigation_table = Table(title="Navigations Available are:")
            navigation_table.add_column("#", justify="right", style="cyan", no_wrap=False)
            navigation_table.add_column("Choice", style="magenta")
            tree_less_navigation_options = [i.split('.')[-1] for i in available_navigations]
            navigation_choice: int = self.ask_choice(
                console=console, choices=tree_less_navigation_options, table=navigation_table)
            self.location = available_navigations[navigation_choice]
            # TODO: HANDLE NEGATIVE WORLD TREE TRAVERSAL.
            # TODO: HANDLE STRING ID'S AND LINKING PLAYERS TO DIFFERENT PARTS OF THE WORLD TREE.


class GameWorld:
    def __init__(self):
        self.console = Console()
        self.player = Player(
            name=str(self.console.input("What is [i]your[/i] [bold red]name[/] :smiley: \n[purple]?: ")).strip().capitalize()
        )
        self.start_game()

    def start_game(self):
        while True:
            self.player.make_choice(self.console)


if __name__ == "__main__":
    game_world = GameWorld()
    game_world.start_game()
