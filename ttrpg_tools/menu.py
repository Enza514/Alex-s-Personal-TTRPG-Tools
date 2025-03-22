import os
import sys
from ttrpg_tools.dice import Dice
from ttrpg_tools.name_generator import NameGenerator
from ttrpg_tools.title_generator import TitleGenerator


""" defines how CLEAR functions based on the platform"""
if sys.platform in ('linux', 'darwin'):
    CLEAR = 'clear'
elif sys.platform == 'win32':
    CLEAR = 'cls'
else:
    print('Platfrom not supported', file=sys.stderr)
    exit(1)


class Menu:
    """Class to handle the main menu and user input"""
    def __init__(self):
        self.main_options = {1:"Roll dice", 2:"Generate a name",3:"Generate a title", 4:"Quit"}
        self.name_options = {1:"Generate names", 2:"Add another race", 3:"Delete race", 4:"List available races", 6:"Quit"}
        self.title_options = {1:"Generate a title", 2:"Add title components", 3:"Quit"}

                
    def print_options(self, options):
        """Print the available options"""
        
        for key, value in options.items():
            print(f"Option {key}: {value}")


    def input_loop(self):
        """Main input loop for the menu"""
        while True:
            self.print_options(self.main_options)
            user_input = input("What would you like to do? (q to quit) ")
            if user_input.lower() == "q" or user_input == "4":
                clear_term()
                break
            
            elif user_input == "1":
                clear_term()
                self.roll_dice()
            
            elif user_input == "2":
                clear_term()
                self.menu_generate_names()
                
            elif user_input == "3":
                clear_term()
                self.menu_generate_titles()
            
            else:
                clear_term()
                print("Invalid input. Please try again.")


    def menu_generate_names(self):
        """Generate names based on user input"""
        name_generator = NameGenerator()
        while True:
            self.print_options(self.name_options)
            user_input = input("What would you like to do? (q to quit) ")
            if user_input.lower() == "q" or user_input == "5":
                clear_term()
                break
            
            elif user_input == "1":
                clear_term()
                self.generate_fantasy_names(name_generator)
            
            elif user_input == "2":
                clear_term()
                self.add_new_race(name_generator)
            
            elif user_input == "3":
                clear_term()
                self.delete_race(name_generator)
            
            elif user_input == "4":
                clear_term()
                self.list_races(name_generator)
            
            else:
                clear_term()
                print("Invalid input. Please try again.")


    def menu_generate_titles(self):
        """Generate titles based on user input"""
        title_generator = TitleGenerator()
        while True:
            self.print_options(self.title_options)
            user_input = input("What would you like to do? (q to quit) ")
            if user_input == '1':
                clear_term()
                self.generate_title(title_generator)
                
            elif user_input == '2':
                clear_term()
                self.add_title_components(title_generator)
                
            elif user_input == '3' or user_input.lower() == 'q':
                clear_term()
                break
            
            else:
                clear_term()
                print("Invalid choice. Please try again.")


    def roll_dice(self):
        """Roll dice based on user input"""
        
        while True:
            user_input = input("What dice and how many would you like to roll? (q to quit) ")
                    
            if user_input.lower() == "q":
                clear_term()
                break
            
            clear_term()        
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
        """Add a new race to the name_generator"""
        
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
        """Delete a race from the name_generator"""
        
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


    def generate_title(self, generator):
        """Generate a title based on user preferences"""
        print("\nCOMPLEXITY:")
        print("1. Simple (e.g., 'the Great', 'the Cursed')")
        print("2. Complex (e.g., 'The Hero of the Western Realms', 'The Scourge of the Scarred Beast from the Depths')")
        
        complexity_choice = input("\nChoose complexity (1-2): ")
        complexity = "simple" if complexity_choice == "1" else "complex"
        
        print("\nSENTIMENT:")
        print("1. Positive (heroic, noble, good)")
        print("2. Negative (villainous, dark, evil)")
        
        sentiment_choice = input("\nChoose sentiment (1-2): ")
        sentiment = "positive" if sentiment_choice == "1" else "negative"
        
        count = 1
        try:
            count = int(input("\nHow many titles would you like to generate? [1-10]: "))
            count = max(1, min(10, count))  # Limit between 1 and 10
        except ValueError:
            count = 3
            print(f"Using default count of {count}.")
        
        print(f"\n{complexity.capitalize()} {sentiment} titles:")
        for i in range(count):
            title = generator.generate_title(complexity, sentiment)
            print(f"{i+1}. {title}")


    def add_title_components(self, generator):
        """Add new title components to the generator"""
        print("\nCOMPLEXITY:")
        print("1. Simple (e.g., 'the Great', 'the Cursed')")
        print("2. Complex (e.g., 'The Hero of the Western Realms', 'The Scourge of the Scarred Beast from the Depths')")
        
        complexity_choice = input("\nChoose complexity (1-2): ")
        complexity = "simple" if complexity_choice == "1" else "complex"
        
        print("\nSENTIMENT:")
        print("1. Positive (heroic, noble, good)")
        print("2. Negative (villainous, dark, evil)")
        
        sentiment_choice = input("\nChoose sentiment (1-2): ")
        sentiment = "positive" if sentiment_choice == "1" else "negative"
        
        component_type = None
        if complexity == "complex":
            print("\nCOMPONENT TYPE:")
            if sentiment == "positive":
                print("1. Prefixes (e.g., 'The Hero of', 'The Guardian of')")
                print("2. Locations (e.g., 'the Western Realms', 'the Misty Mountains')")
                
                type_choice = input("\nChoose component type (1-2): ")
                component_type = "prefixes" if type_choice == "1" else "locations"
            else:  # negative
                print("1. Prefixes (e.g., 'The Scourge of', 'The Terror of')")
                print("2. Creations (e.g., 'the Scarred Beast', 'the Twisted Creature')")
                print("3. Origins (e.g., 'from the Depths', 'from the Shadows')")
                
                type_choice = input("\nChoose component type (1-3): ")
                if type_choice == "1":
                    component_type = "prefixes"
                elif type_choice == "2":
                    component_type = "creations"
                else:
                    component_type = "origins"
        
        print("\nEnter new components (comma-separated):")
        components_input = input("> ")
        new_components = [comp.strip() for comp in components_input.split(",")]
        
        if not new_components or all(comp == "" for comp in new_components):
            print("No valid components entered.")
            return
        
        result = generator.add_title_component(complexity, sentiment, component_type, new_components)
        print(result)


def clear_term() -> None:
    """Clear the terminal screen"""
    os.system(CLEAR)