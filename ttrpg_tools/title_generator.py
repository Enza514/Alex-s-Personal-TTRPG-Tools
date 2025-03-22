import random
import json
import os


class TitleGenerator:
    def __init__(self, data_file="data/fantasy_titles.json"):
        self.data_file = data_file
        self.title_data = {}
        self.load_title_data()


    def load_title_data(self):
        """Load title data from the JSON file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as file:
                    self.title_data = json.load(file)
                print(f"Successfully loaded title data from {self.data_file}")
            else:
                print(f"Data file {self.data_file} not found. Creating with default title components.")
                self.create_default_title_data()
                self.save_title_data()
        except Exception as e:
            print(f"Error loading title data: {e}")
            print("Creating default title data instead.")
            self.create_default_title_data()
            self.save_title_data()


    def create_default_title_data(self):
        """Create default title components if no file exists"""
        self.title_data = {
            "simple": {
                "positive": [
                    "the Great", "the Wise", "the Brave", "the Mighty", "the Noble",
                    "the Just", "the Merciful", "the Blessed", "the Bold", "the Brilliant",
                    "the Valiant", "the Magnificent", "the Defender", "the Devoted", "the Faithful"
                ],
                "negative": [
                    "the Cursed", "the Cruel", "the Wicked", "the Terrible", "the Grim",
                    "the Vile", "the Feared", "the Ruthless", "the Dark", "the Dreadful",
                    "the Tyrant", "the Fallen", "the Betrayer", "the Accused", "the Malicious"
                ]
            },
            "complex": {
                "positive": {
                    "prefixes": [
                        "The Hero of", "The Guardian of", "The Savior of", "The Protector of", 
                        "The Champion of", "The Defender of", "The Liberator of", "The Light of",
                        "The Shield of", "The Sword of", "The Hope of", "The Friend of",
                        "The Righteous Hand of", "The Blessed One of", "The Chosen of"
                    ],
                    "locations": [
                        "the Western Realms", "the Eastern Kingdoms", "the Northern Lands", "the Southern Isles",
                        "the Misty Mountains", "the Golden Valley", "the Shimmering Forest", "the Sacred Grove",
                        "the Crystal Shores", "the Emerald Hills", "the Sunlit Plains", "the Azure Coast",
                        "the Verdant Woods", "the Peaceful Meadows", "the Radiant Peaks"
                    ]
                },
                "negative": {
                    "prefixes": [
                        "The Scourge of", "The Terror of", "The Bane of", "The Destroyer of",
                        "The Nightmare of", "The Plague of", "The Doom of", "The Butcher of",
                        "The Curse of", "The Ravager of", "The Shadow of", "The Defiler of",
                        "The Tormentor of", "The Despoiler of", "The Devourer of"
                    ],
                    "creations": [
                        "the Scarred Beast", "the Twisted Creature", "the Corrupted Soul", "the Fallen Knight",
                        "the Vengeful Spirit", "the Cursed Wanderer", "the Raging Beast", "the Dark Sorcerer",
                        "the Bloodthirsty Monster", "the Forgotten Heretic", "the Merciless Killer", "the Faceless Horror",
                        "the Wretched Abomination", "the Sinister Specter", "the Deathless Warlord"
                    ],
                    "origins": [
                        "from the Depths", "from the Shadows", "from the Abyss", "from the Void",
                        "from the Netherworld", "from the Darkness", "from the Eternal Night", "from the Forgotten Realm",
                        "from the Cursed Lands", "from the Forsaken Wastes", "from the Blighted Marsh", "from the Charred Ruins",
                        "from the Howling Chasm", "from the Crushing Deep", "from the Ashen Plains"
                    ]
                }
            }
        }


    def save_title_data(self):
        """Save the current title data to the JSON file"""
        try:
            with open(self.data_file, 'w') as file:
                json.dump(self.title_data, file, indent=2)
            print(f"Successfully saved title data to {self.data_file}")
        except Exception as e:
            print(f"Error saving title data: {e}")


    def generate_simple_title(self, sentiment):
        """Generate a simple title with the specified sentiment"""
        if sentiment.lower() not in ["positive", "negative"]:
            return f"Invalid sentiment. Choose 'positive' or 'negative'."
        
        return random.choice(self.title_data["simple"][sentiment.lower()])


    def generate_complex_title(self, sentiment):
        """Generate a complex title with the specified sentiment"""
        if sentiment.lower() not in ["positive", "negative"]:
            return f"Invalid sentiment. Choose 'positive' or 'negative'."
        
        sentiment = sentiment.lower()
        if sentiment == "positive":
            prefix = random.choice(self.title_data["complex"][sentiment]["prefixes"])
            location = random.choice(self.title_data["complex"][sentiment]["locations"])
            return f"{prefix} {location}"
        else:
            prefix = random.choice(self.title_data["complex"][sentiment]["prefixes"])
            creation = random.choice(self.title_data["complex"][sentiment]["creations"])
            origin = random.choice(self.title_data["complex"][sentiment]["origins"])
            return f"{prefix} {creation} {origin}"


    def generate_title(self, complexity, sentiment):
        """Generate a title with the specified complexity and sentiment"""
        if complexity.lower() == "simple":
            return self.generate_simple_title(sentiment)
        elif complexity.lower() == "complex":
            return self.generate_complex_title(sentiment)
        else:
            return f"Invalid complexity. Choose 'simple' or 'complex'."


    def add_title_component(self, complexity, sentiment, component_type, new_components):
        """Add new title components"""
        complexity = complexity.lower()
        sentiment = sentiment.lower()
        
        if complexity not in ["simple", "complex"]:
            return f"Invalid complexity. Choose 'simple' or 'complex'."
        
        if sentiment not in ["positive", "negative"]:
            return f"Invalid sentiment. Choose 'positive' or 'negative'."
        
        if complexity == "simple":
            self.title_data[complexity][sentiment].extend(new_components)
        else:  # complex
            if component_type not in ["prefixes", "locations", "creations", "origins"]:
                return f"Invalid component type for complex titles."
            
            if component_type == "locations" and sentiment == "negative":
                return f"'locations' is not a valid component for negative complex titles."
            
            if component_type in ["creations", "origins"] and sentiment == "positive":
                return f"'{component_type}' is not a valid component for positive complex titles."
            
            if component_type in self.title_data[complexity][sentiment]:
                self.title_data[complexity][sentiment][component_type].extend(new_components)
            else:
                return f"Invalid component type for {sentiment} {complexity} titles."
        
        self.save_title_data()
        return f"Added new {component_type} to {sentiment} {complexity} titles."