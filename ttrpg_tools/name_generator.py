import random
import json
import os


class NameGenerator:
    def __init__(self, data_file="data/fantasy_names.json"):
        self.data_file = data_file
        self.races = {}
        self.load_races()

    
    def load_races(self):
        """Load race data from the JSON file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as file:
                    self.races = json.load(file)
                print(f"Successfully loaded {len(self.races)} races from {self.data_file}")
            else:
                print(f"Data file {self.data_file} not found. Creating with default races.")
                self.create_default_races()
                self.save_races()
        except Exception as e:
            print(f"Error loading races: {e}")
            print("Creating default races instead.")
            self.create_default_races()
            self.save_races()

    
    def create_default_races(self):
        """Create default races if no file exists"""
        self.races = {
            "elf": {
                "prefixes": ["Ael", "Aer", "Ara", "Cal", "Elr", "Eir", "Fae", "Gal", "Ill", "Leg", "Lor", "Mel", "Nae", "Sil", "Thar", "Vaer"],
                "suffixes": ["adan", "ael", "alin", "alos", "ari", "arion", "emar", "ian", "iel", "il", "inar", "ion", "orin", "olas", "ondel", "wyn"]
            },
            "dwarf": {
                "prefixes": ["Bal", "Bar", "Dain", "Dar", "Dor", "Dur", "Gim", "Glor", "Grun", "Kaz", "Mor", "Nal", "Thor", "Thra", "Tor", "Thrain"],
                "suffixes": ["adin", "ain", "ack", "ar", "ein", "dok", "fur", "grad", "grim", "heim", "il", "in", "lig", "or", "rim", "und"]
            },
            "orc": {
                "prefixes": ["Az", "Bol", "Dag", "Dru", "Gash", "Graz", "Grim", "Krug", "Mog", "Nar", "Rak", "Shak", "Thok", "Urag", "Vrak", "Zog"],
                "suffixes": ["aga", "ash", "gak", "gar", "gol", "goth", "grash", "gul", "mak", "nar", "rub", "shak", "thar", "thog", "tor", "zul"]
            },
            "human": {
                "prefixes": ["Al", "And", "Bran", "Cal", "Dan", "Ed", "Ger", "Joh", "Kel", "Mal", "Ric", "Rob", "Stan", "Tho", "Wal", "Wil"],
                "suffixes": ["an", "ard", "bert", "don", "eth", "fred", "gan", "hard", "in", "mer", "mund", "on", "rad", "son", "vin", "ward"]
            }
        }

    
    def save_races(self):
        """Save the current races to the JSON file"""
        try:
            with open(self.data_file, 'w') as file:
                json.dump(self.races, file, indent=2)
            print(f"Successfully saved races to {self.data_file}")
        except Exception as e:
            print(f"Error saving races: {e}")

    
    def generate_name(self, race):
        """Generate a random name for the specified race"""
        race = race.lower()
        if race not in self.races:
            return f"Sorry, '{race}' is not a recognized race. Available races: {', '.join(self.races.keys())}"
        name_parts = self.races[race]
        prefix = random.choice(name_parts["prefixes"])
        suffix = random.choice(name_parts["suffixes"])
        return f"{prefix}{suffix}"

    
    def generate_multiple_names(self, race, count=5):
        """Generate multiple names for the specified race"""
        names = []
        for _ in range(count):
            names.append(self.generate_name(race))
        return names

    
    def get_available_races(self):
        """Return a list of available races"""
        return list(self.races.keys())

    
    def add_race(self, race, prefixes, suffixes):
        """Add a new race with name components"""
        race = race.lower()
        self.races[race] = {
            "prefixes": prefixes,
            "suffixes": suffixes
        }
        self.save_races()
        return f"Added race: {race}"


    def delete_race(self, race):
        """Delete a race from the data"""
        race = race.lower()
        if race in self.races:
            del self.races[race]
            self.save_races()
            return f"Deleted race: {race}"
        return f"Race '{race}' not found"
    