# Import functions & Libraries
import keyboard  # Used to be able to make key presses
from addons import *
import time

# Top Variables
refresh_time: int = 5  # Lowering this number might get you flagged
quit_on_join: bool = True  # Quits the program after joining: True / False
attempts: int = 0  # Starts at 0 and gradually increases each discord
return_to_discord: bool = False  # Makes it so you can alt tab during discord refresh count down
normal_color: tuple[int, int, int] = (36, 128, 69)  # The normal RGB value of the button
hover_color: tuple[int, int, int] = (26, 99, 52)  # The RGB values of the join button while hovering

# Starts elapsed time
start: float = time.time()


def main() -> None:
    global attempts
    global return_to_discord

    while not keyboard.is_pressed('q'):  # Hold 'q' to close this script
        # If the mouse hovers over the join button (RGB matches) it will click
        if on_button(normal_color, hover_color):
            return_to_discord = False  # Resets return flag each attempt
            position = on_button(normal_color, hover_color)
            print("Button found!")
            for i in range(5):  # Clicks five times
                pyautogui.click(position[0], position[1])
            print("Joining...")
            time.sleep(1)
            # If the color under the mouse changes to anything else it presumably joined successfully
            if not this_server_is_currently_full(output=True) and on_discord() and not are_you_human():
                print("Computing...")
                time.sleep(2)
                if not this_server_is_currently_full(output=False) and on_discord() and not are_you_human():
                    print("Joined.")
                    # Adds an attempt and prints za total
                    attempts += 1
                    print(f"Total attempts {attempts}")
                    print_time()  # Prints total time
                    # If quitting is enable waits for a keypress to exit
                    if quit_on_join:
                        input("Press Enter to continue...")
                        exit()
                    else:
                        print("Continuing...")
                        pass
                else:
                    pass
            # Otherwise:
            else:
                # Sleeps 5 seconds and checks if discord is showing
                return_to_discord = True  # Turns on window switcher
                for i in range(refresh_time):
                    print(f"Refreshing in {refresh_time - i}")
                    time.sleep(0.5)
                    on_discord()
                # Then refreshes for the next attempt
                keyboard.press_and_release('ctrl+r')
                attempts += 1


if __name__ == '__main__':
    main()