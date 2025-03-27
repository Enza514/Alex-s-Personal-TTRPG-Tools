import random
import json
import os
from datetime import datetime


class LocationNameGenerator:
    """A generator for fantasy location names"""
    def __init__(self, data_file="data/fantasy_locations.json", history_file="data/fantasy_locations_history.json"):
        self.data_file = data_file
        self.history_file = history_file
        self.location_data = {}
        self.name_history = {}
        self.load_location_data()
        self.load_name_history()


    def load_location_data(self):
        """Load location name data from the JSON file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as file:
                    self.location_data = json.load(file)
                print(f"Successfully loaded location name data from {self.data_file}")
                
            else:
                print(f"Data file {self.data_file} not found. Creating with default location name components.")
                self.create_default_location_data()
                self.save_location_data()
                
        except Exception as e:
            print(f"Error loading location name data: {e}")
            print("Creating default location name data instead.")
            self.create_default_location_data()
            self.save_location_data()


    def load_name_history(self):
        """Load previously generated and saved names"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as file:
                    self.name_history = json.load(file)
                print(f"Successfully loaded name history from {self.history_file}")
                
            else:
                self.name_history = {"saved_names": []}
                self.save_name_history()
                
        except Exception as e:
            print(f"Error loading name history: {e}")
            self.name_history = {"saved_names": []}
            self.save_name_history()


    def create_default_location_data(self):
        """Create default location name components"""
        self.location_data = {
            "terrain": {
                "generic": [
                    "Valley", "Hills", "Plains", "Plateau", "Meadows", 
                    "Woods", "Forest", "Glade", "Highlands", "Lowlands"
                ],
                "mountain": [
                    "Peak", "Mountains", "Crags", "Highlands", "Cliffs", 
                    "Summit", "Ranges", "Peaks", "Ridgeline", "Escarpment"
                ],
                "water": [
                    "Bay", "Coast", "Shore", "Islands", "Archipelago", 
                    "Reef", "Cove", "Delta", "Lagoon", "Inlet"
                ]
            },
            "prefixes": {
                "mystical": [
                    "Mystic", "Enchanted", "Eternal", "Forgotten", "Sacred", 
                    "Whispering", "Moonlit", "Starry", "Ethereal", "Radiant"
                ],
                "geographical": [
                    "Misty", "Verdant", "Emerald", "Golden", "Silver", 
                    "Azure", "Crimson", "Crystal", "Shadow", "Hidden"
                ]
            },
            "suffixes": {
                "descriptive": [
                    "Haven", "Realm", "Domain", "Kingdom", "Lands", 
                    "Territory", "Dominion", "Expanse", "Sanctuary", "Frontier"
                ],
                "mysterious": [
                    "Whisper", "Secret", "Dream", "Prophecy", "Destiny", 
                    "Legend", "Myth", "Wonder", "Enigma", "Harmony"
                ]
            }
        }
    
    def save_location_data(self):
        """Save the current location name data to the JSON file"""
        try:
            with open(self.data_file, 'w') as file:
                json.dump(self.location_data, file, indent=2)
            print(f"Successfully saved location name data to {self.data_file}")
            
        except Exception as e:
            print(f"Error saving location name data: {e}")
    
    def save_name_history(self):
        """Save the name history to the JSON file"""
        try:
            with open(self.history_file, 'w') as file:
                json.dump(self.name_history, file, indent=2)
            print(f"Successfully saved name history to {self.history_file}")
            
        except Exception as e:
            print(f"Error saving name history: {e}")


    def generate_location_name(self, terrain=None):
        """Generate a location name"""
        # If no specific terrain is provided, choose a random terrain
        if not terrain:
            terrain_categories = list(self.location_data["terrain"].keys())
            terrain = random.choice(terrain_categories)
        
        # Choose components
        prefix_category = random.choice(list(self.location_data["prefixes"].keys()))
        suffix_category = random.choice(list(self.location_data["suffixes"].keys()))
        
        # Select random components
        prefix = random.choice(self.location_data["prefixes"][prefix_category])
        terrain_type = random.choice(self.location_data["terrain"][terrain])
        suffix = random.choice(self.location_data["suffixes"][suffix_category])
        
        # Combine to create location name
        if random.random() < 0.5:
            # Prefix + Terrain + Suffix
            location_name = f"{prefix} {terrain_type} of the {suffix}"
            
        else:
            # Terrain of the Prefix Suffix
            location_name = f"{terrain_type} of the {prefix} {suffix}"
        
        return location_name


    def save_generated_name(self, name, tags=None):
        """Save a generated name to the history"""
        save_entry = {
            "name": name,
            "timestamp": datetime.now().isoformat(),
            "tags": tags or []
        }
        
        # Add to saved names
        self.name_history["saved_names"].append(save_entry)
        self.save_name_history()
        return f"Saved location name: {name}"


    def list_saved_names(self, filter_tag=None):
        """List saved names, optionally filtered by tag"""
        saved_names = self.name_history["saved_names"]
        
        if filter_tag:
            saved_names = [entry for entry in saved_names if filter_tag in entry.get("tags", [])]
        
        if not saved_names:
            return "No saved names found."
        
        # Format the output
        output = "Saved Location Names:\n"
        for i, entry in enumerate(saved_names, 1):
            output += f"{i}. {entry['name']} (Saved: {entry['timestamp']})"
            if entry.get("tags"):
                output += f" [Tags: {', '.join(entry['tags'])}]"
            output += "\n"
        
        return output


    def add_location_name_component(self, component_type, category, new_components):
        """Add new location name components"""
        # Validate component type
        if component_type not in ["terrain", "prefixes", "suffixes"]:
            return f"Invalid component type. Choose 'terrain', 'prefixes', or 'suffixes'."
        
        # For terrain, require a specific sub-category
        if component_type == "terrain" and category not in ["generic", "mountain", "water"]:
            return f"Invalid terrain category. Choose 'generic', 'mountain', or 'water'."
        
        # For prefixes and suffixes, require a specific sub-category
        if component_type in ["prefixes", "suffixes"] and category not in ["mystical", "geographical", "descriptive", "mysterious"]:
            return f"Invalid {component_type} category. Choose from available categories."
        
        # Add the new components
        if category in self.location_data[component_type]:
            self.location_data[component_type][category].extend(new_components)
            
        else:
            self.location_data[component_type][category] = new_components
        
        # Save the updated data
        self.save_location_data()
        return f"Added new components to {component_type} - {category}"
