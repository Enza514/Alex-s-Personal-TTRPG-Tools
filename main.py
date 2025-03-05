from ttrpg_tools.dice import Dice

def input_loop():
    while True:
        print("Option 1: Roll dice")
        print("Option 2: Quit")
        user_input = input("What would you like to do> (q to quit) ")
        if user_input.lower() == "q" or user_input == "2":
            break
        elif user_input == "1":
            while True: 
                user_input = input("What dice and how many would you like to roll? (r to return to main menu) ")
                if user_input.lower() == "r":
                    break
                dice = Dice(user_input)
                dice.roll()
        else:
            print("Invalid input. Please try again.")
def main():
    input_loop()

if __name__ == "__main__":
    main()