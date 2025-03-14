from ttrpg_tools.dice import Dice
from ttrpg_tools.name_generator import NameGenerator

class Menu:
    """Class to handle the main menu and user input"""
    def __init__(self):
        self.main_options = {1:"Roll dice", 2:"Generate a name", 3:"Quit"}
        self.name_options = {1:"Generate names", 2:"Add ne race", 3:"Delete race", 4:"List available races", 5:"Quit"}        

                
    def print_options(self, options):
        """Print the available options"""
        
        for key, value in options.items():
            print(f"Option {key}: {value}")


    def roll_dice(self):
        """Roll dice based on user input"""
        
        while True: 
                    user_input = input("What dice and how many would you like to roll? (r to return to main menu) ")
                    
                    if user_input.lower() == "r":
                        break
                    
                    dice = Dice(user_input)
                    dice.roll()


    def generate_fantasy_names(self, generator):
        """Generate names for a selected race"""
        
        available_races = generator.get_available_races()
        
        if not available_races:
            print("No races available. Please add a race first.")
            return
        
        print("\nAvailable races: " + ", ".join(available_races))
        race = input("Enter a race to generate names for: ")
        
        if race.lower() not in generator.races:
            print(generator.generate_name(race))
            return
        
        try:
            count = int(input("How many names would you like to generate? [1-10]: "))
            count = max(1, min(10, count))  # Limit between 1 and 10
        
        except ValueError:
            count = 5
            print(f"Using default count of {count}.")
        
        print(f"\n{race.capitalize()} names:")
        names = generator.generate_multiple_names(race, count)
        for i, name in enumerate(names, 1):
            print(f"{i}. {name}")


    def add_new_race(self, generator):
        """Add a new race to the generator"""
        
        race = input("Enter the name of the new race: ")
        race = race.lower()
        
        if race in generator.races:
            overwrite = input(f"Race '{race}' already exists. Overwrite? (y/n): ")
            if overwrite.lower() != 'y':
                print("Operation cancelled.")
                return
        
        print("Enter prefixes (comma-separated):")
        prefixes_input = input("> ")
        prefixes = [prefix.strip() for prefix in prefixes_input.split(",")]
        
        print("Enter suffixes (comma-separated):")
        suffixes_input = input("> ")
        suffixes = [suffix.strip() for suffix in suffixes_input.split(",")]
        
        if not prefixes or not suffixes:
            print("Both prefixes and suffixes are required.")
            return
        
        result = generator.add_race(race, prefixes, suffixes)
        print(result)


    def delete_race(self, generator):
        """Delete a race from the generator"""
        
        available_races = generator.get_available_races()
        if not available_races:
            print("No races available to delete.")
            return
        
        print("\nAvailable races: " + ", ".join(available_races))
        race = input("Enter the race to delete: ")
        
        confirm = input(f"Are you sure you want to delete the '{race}' race? (y/n): ")
        
        if confirm.lower() == 'y':
            result = generator.delete_race(race)
            print(result)
            
        else:
            print("Operation cancelled.")


    def list_races(self, generator):
        """List all available races and their name components"""
        
        races = generator.races
        
        if not races:
            print("No races available.")
            return
        
        print("\nAvailable Races:")
        print("----------------")
        
        for race, components in races.items():
            print(f"\n{race.capitalize()}:")
            print(f"  Prefixes ({len(components['prefixes'])}): {', '.join(components['prefixes'])}")
            print(f"  Suffixes ({len(components['suffixes'])}): {', '.join(components['suffixes'])}")


    def input_loop(self):
        while True:
            self.print_options(self.main_options)
            user_input = input("What would you like to do? (q to quit) ")
            if user_input.lower() == "q" or user_input == "3":
                break
            
            elif user_input == "1":
                self.roll_dice()
            
            elif user_input == "2":
                self.generate_names()
            
            else:
                print("Invalid input. Please try again.")


    def generate_names(self):
        """Generate names based on user input"""
        generator = NameGenerator()
        while True:
            self.print_options(self.name_options)
            user_input = input("What would you like to do? (q to quit) ")
            if user_input.lower() == "q" or user_input == "5":
                break
            
            elif user_input == "1":
                self.generate_fantasy_names(generator)
            
            elif user_input == "2":
                self.add_new_race(generator)
            
            elif user_input == "3":
                self.delete_race(generator)
            
            elif user_input == "4":
                self.list_races(generator)
            
            else:
                print("Invalid input. Please try again.")