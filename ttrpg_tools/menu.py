import os
import sys
from ttrpg_tools.dice import Dice
from ttrpg_tools.location_generator import LocationNameGenerator
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
        self.main_options = {1:"Roll dice", 2:"Generate a name",3:"Generate a title", 4:"Generate a location", 5:"Quit"}
        self.name_options = {1:"Generate names", 2:"Add another race", 3:"Delete race", 4:"List available races", 6:"Quit"}
        self.title_options = {1:"Generate a title", 2:"Add title components", 3:"Quit"}
        self.location_options = {1:"Generate a location name", 2:"Save Generated Name", 3:"List Saved Names", 4:"Add Location Name Components", 5:"Quit"}

                
    def print_options(self, options):
        """Print the available options"""
        
        for key, value in options.items():
            print(f"Option {key}: {value}")


    def input_loop(self):
        """Main input loop for the menu"""
        while True:
            self.print_options(self.main_options)
            user_input = input("What would you like to do? (q to quit) ")
            
            if user_input.lower() == "q" or user_input == "5":
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
            
            elif user_input == "4":
                clear_term()
                self.menu_location_names()
            
            else:
                clear_term()
                print("Invalid input. Please try again.")


    def menu_generate_names(self):
        """Menu for generating names based on user input"""
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
        """Menu for generating titles based on user input"""
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


    def menu_location_names(self):
        """Menu for generating location names based on user input"""
        location_generator = LocationNameGenerator()
        saved_names = []
        while True:
            self.print_options(self.location_options)
            user_input = input("What would you like to do? (q to quit) ")
            
            if user_input == '1':
                clear_term()
                self.generate_location_name(location_generator)
                
            elif user_input == '2':
                clear_term()
                saved_names = self.save_generated_name(location_generator)
                
            elif user_input == '3':
                clear_term()
                self.list_saved_names(location_generator, saved_names)
                
            elif user_input == '4':
                clear_term()
                self.add_location_components(location_generator)    
                
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

    ### Fantasy Names related methods
    
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

    ### Title Generator related methods

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

    ### Location Generator related methods

    def generate_location_name(self, generator):
        """Generate a location name"""
        print("\nTERRAIN TYPES:")
        print("1. Generic (Valleys, Plains, etc.)")
        print("2. Mountain (Peaks, Ranges, etc.)")
        print("3. Water (Bays, Coasts, etc.)")
        print("4. Random")
        
        terrain_choice = input("\nChoose terrain type (1-4): ")
        
        terrain_map = {
            "1": "generic",
            "2": "mountain", 
            "3": "water"
        }
        
        terrain = terrain_map.get(terrain_choice, None)
        
        # Generate multiple names
        count = 1
        try:
            count = int(input("\nHow many location names would you like to generate? [1-10]: "))
            count = max(1, min(10, count))  # Limit between 1 and 10
        except ValueError:
            count = 3
            print(f"Using default count of {count}.")
        
        print("\nGenerated Location Names:")
        generated_names = []
        
        for i in range(count):
            name = generator.generate_location_name(terrain)
            print(f"{i+1}. {name}")
            generated_names.append(name)
        
        # Return the list of generated names for potential saving
        return generated_names

    # TODO currently option 1 not implemented
    def save_generated_name(self, generator, saved_names=None): 
        """Save a generated name with optional tags"""
        print("\nSAVE OPTIONS:")
        print("1. Save from recently generated names")
        print("2. Manually enter a name")
        
        save_choice = input("\nChoose save method (1-2): ")
        
        if save_choice == '1' and saved_names is None:
            print("No recently generated names to save.")
            return
        
        elif save_choice == '1' and saved_names is not None:
            # TODO: Implement saving from recently generated names
            pass # Implement this later
        
        elif save_choice == '2':
            name = input("\nEnter the location name to save: ")
            
            # Optional tagging
            add_tags = input("Would you like to add tags to this name? (y/n): ")
            tags = []
            
            if add_tags.lower() == 'y':
                tag_input = input("Enter tags (comma-separated): ")
                tags = [tag.strip() for tag in tag_input.split(',')]
            
            result = generator.save_generated_name(name, tags)
            print(result)


    def list_saved_names(self, generator):
        """List saved names with optional filtering"""
        print("\nLIST OPTIONS:")
        print("1. List all saved names")
        print("2. Filter by tag")
        
        list_choice = input("\nChoose list method (1-2): ")
        
        if list_choice == '1':
            print(generator.list_saved_names())
        elif list_choice == '2':
            tag = input("Enter tag to filter by: ")
            print(generator.list_saved_names(tag))


    def add_location_components(self, generator):
        """Add new location name components"""
        print("\nCOMPONENT TYPES:")
        print("1. Terrain")
        print("2. Prefixes")
        print("3. Suffixes")
        
        component_choice = input("\nChoose component type (1-3): ")
        
        component_type_map = {
            "1": "terrain",
            "2": "prefixes",
            "3": "suffixes"
        }
        
        component_type = component_type_map.get(component_choice)
        
        if not component_type:
            print("Invalid choice.")
            return
        
        # Choose category based on component type
        if component_type == "terrain":
            print("\nTERRAIN CATEGORIES:")
            print("1. Generic")
            print("2. Mountain")
            print("3. Water")
            category_choice = input("\nChoose terrain category (1-3): ")
            category_map = {"1": "generic", "2": "mountain", "3": "water"}
            category = category_map.get(category_choice)
        else:
            print(f"\n{component_type.capitalize()} CATEGORIES:")
            print("1. Mystical")
            print("2. Geographical")
            if component_type == "suffixes":
                print("3. Descriptive")
                print("4. Mysterious")
            
            category_choice = input("\nChoose category (1-4): ")
            category_map = {
                "prefixes": {"1": "mystical", "2": "geographical"},
                "suffixes": {"1": "mystical", "2": "geographical", "3": "descriptive", "4": "mysterious"}
            }
            category = category_map.get(component_type, {}).get(category_choice)
        
        if not category:
            print("Invalid category.")
            return
        
        # Get new components
        print("\nEnter new components (comma-separated):")
        components_input = input("> ")
        new_components = [comp.strip() for comp in components_input.split(",")]
        
        if not new_components or all(comp == "" for comp in new_components):
            print("No valid components entered.")
            return
        
        result = generator.add_location_name_component(component_type, category, new_components)
        print(result)
    
### General methods

def clear_term() -> None:
    """Clear the terminal screen"""
    os.system(CLEAR)