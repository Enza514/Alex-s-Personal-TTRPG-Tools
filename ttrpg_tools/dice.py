import random
import re

class Dice:
    """ Class to handle rolling dice based on user input."""
    def __init__(self, dice_input):
        self.dice_input = dice_input.strip()
    
    def roll(self):
        """ Roll the dice based on the user input."""
        dice_patterns = re.findall(r"(\d*)d(\d+)", self.dice_input, re.IGNORECASE)
        if not dice_patterns:
            print("Invalid input. Please use the format XdY (e.g., 1d6, 2d20, 1d20 + 2d8 + 1d4).")
            return
        
        modifier_choice = input("Would you like to add a modifier to each roll or to the total? (each/total/none): ").strip().lower()
        modifier = 0
        if modifier_choice in ("each", "total"):
            modifier = int(input("Enter the modifier value: "))
        
        total_rolls = []
        grand_total = 0
        for num, sides in dice_patterns:
            num_dice = int(num) if num else 1  # Default to 1 if omitted
            dice_sides = int(sides)
            
            rolls = [random.randint(1, dice_sides) for _ in range(num_dice)]
            if modifier_choice == "each":
                modified_rolls = [r + modifier for r in rolls]
                roll_str = f"{num_dice}d{dice_sides}: {', '.join(f'{r} (+{modifier})' for r in modified_rolls)}"
            else:
                roll_str = f"{num_dice}d{dice_sides}: {', '.join(map(str, rolls))}"
            
            total_rolls.append(roll_str)
            grand_total += sum(modified_rolls) if modifier_choice == "each" else sum(rolls)
        
        if modifier_choice == "total":
            grand_total += modifier
            total_rolls.append(f"(+{modifier})")
        
        print("Rolling:")
        print(" | ".join(total_rolls))
        print(f"Total: {grand_total}")
