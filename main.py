# Used libraries
import time  # Used to make program wait (sleep)
from datetime import datetime  # Used to tell the current time of the OS
from typing import Union  # Fixes type annotation
import keyboard  # Used to be able to make key presses
import pyautogui  # Used to move the cursor
from PIL.Image import Image  # Used to take screenshots (Server Full / Not)

# Variables
refresh_time: int = 5  # Lowering this number might get you flagged
quit_on_join: bool = False  # Quits the program after joining: True / False
normal_color: tuple[int, int, int] = (36, 128, 69)  # The normal RGB value of the button
hover_color: tuple[int, int, int] = (26, 99, 52)  # The RGB values of the join button while hovering
attempts: int = 0  # Starts at 0 and gradually increases each discord
return_to_discord: bool = False  # Makes it so you can alt tab during discord refresh count down


def on_button() -> Union[tuple[int, int], bool]:
    # Get current position of the mouse
    position = pyautogui.position()
    # Takes a 1 by 1 screenshot of where your cursor is placed
    screenshot: Image = pyautogui.screenshot(region=(position[0], position[1], 1, 1))
    # Save the RBG value of the pixel
    rgb: float = screenshot.getpixel((0, 0))
    # Compare against the button
    if rgb == hover_color or rgb == normal_color:
        return position[0], position[1]
    else:
        time.sleep(1)
        print("Searching button to press...")
        return False  # And continue searching


def is_on_screen(image) -> bool | None:
    try:  # Tries to find the image if it can't it throws an error
        if pyautogui.locateOnScreen(image, grayscale=True, confidence=0.7) is not None:
            return True
    except pyautogui.ImageNotFoundException:  # Returns false (It didn't find)
        return False


def this_server_is_currently_full(output) -> bool | None:
    # Tries to find the discord full_server widget
    if is_on_screen('images/full_server.png'):
        if output:
            print("This server is currently full, refreshing:")
        time.sleep(0.5)
        # If returned true it will refresh discord
        return True
    # Else don't refresh
    elif output:  # This check makes the output silent
        print("Lost focus on the join button...")
    time.sleep(0.5)
    return False


def on_discord() -> bool | None:
    if not return_to_discord:
        # Searches for Discord's upper right menu buttons
        if is_on_screen('images/menu.png'):
            #print("On discord")
            time.sleep(0.5)
            return True
            # If it can't find them it will wait (Not on Discord)
        else:
            #print("Not on discord")
            time.sleep(0.5)
            return False
    else:
        # Now on discord
        if is_on_screen('images/menu.png'):
            time.sleep(0.5)
            pass
        # Get back to discord
        else:
            print("Get back to discord")
            time.sleep(1)
            on_discord()


def are_you_human() -> bool | None:
    if is_on_screen('images/are_you_human.png'):
        print("Human check on screen")
        return True
    else:
        print("No human check on screen")
        return False


def print_time() -> None:  # Basic timer
    elapsed_time: float = time.time() - start
    minutes: int = int((elapsed_time // 60))
    seconds: int = int((elapsed_time % 60))
    print(f"Elapsed time: {minutes}:{seconds:02d}")

    # Get the current time of your system
    current_time = datetime.now()
    formatted_time = current_time.strftime("%H:%M:%S")
    print(f"Current time: {formatted_time}")


start: float = time.time()  # Times joining

if this_server_is_currently_full(output=False):
    keyboard.press_and_release('ctrl+r')

def main() -> None:
    global attempts
    global return_to_discord

    while not keyboard.is_pressed('q'):  # Hold 'q' to close this script
        # If the mouse hovers over the join button (RGB matches) it will click
        if on_button():
            return_to_discord = False  # Resets return flag each attempt
            position = on_button()
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