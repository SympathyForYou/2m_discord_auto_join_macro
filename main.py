# ----------------------------------------------- #
# Hover your mouse over the join button           #
# It will try to join if it fails it will refresh #
# Then it will try again and stop once it joined  #
# ----------------------------------------------- #

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


def this_server_is_currently_full(output) -> bool | None:
    try:
        # Searches for the full server png
        if pyautogui.locateOnScreen('images/full_server.png', grayscale=True, confidence=0.7) is not None:
            print("This server is currently full, refreshing:")
            time.sleep(0.5)
            return True
        else:
            pass
        # Pauses the program you are back on discord (Full Server Png is visible)
    except pyautogui.ImageNotFoundException:
        if output:
            print("Lost focus on the join button...")
        else:
            time.sleep(0.5)
            return False


def on_discord() -> bool | None:
    if not return_to_discord:
        try:
            # Searches for Discord's upper right menu buttons
            if pyautogui.locateOnScreen('menu.png', grayscale=True, confidence=0.7) is not None:
                #print("On discord")
                time.sleep(0.5)
                return True
            # If it can't find them it will wait (Not on Discord)
        except pyautogui.ImageNotFoundException:
            #print("Not on discord")
            time.sleep(0.5)
            return False
    else:
        try:
            # Now on discord
            if pyautogui.locateOnScreen('menu.png', grayscale=True, confidence=0.7) is not None:
                time.sleep(0.5)
                pass
        # Get back to discord
        except pyautogui.ImageNotFoundException:
            print("Get back to discord")
            time.sleep(1)
            on_discord()


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


def main() -> None:
    global attempts
    global return_to_discord

    while not keyboard.is_pressed('q'):  # Hold 'q' to close this script
        # If the mouse hovers over the join button (RGB matches)
        if on_button():
            return_to_discord = False  # Resets return flag each attempt
            position = on_button()
            print("Button found!")
            for i in range(5):  # Clicks twice
                pyautogui.click(position[0], position[1])
            time.sleep(1)
            print("Joining...")
            time.sleep(1)
            # If the color under the mouse changes to anything else it presumably joined successfully
            if not this_server_is_currently_full(output=True) and on_discord():
                print("Computing...")
                time.sleep(2)
                if not this_server_is_currently_full(output=False) and on_discord():
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
                time.sleep(1)
                return_to_discord = True  # Turns on window switcher
                for i in range(refresh_time):
                    print(f"Refreshing in {5 - i}")
                    time.sleep(0.5)
                    on_discord()
                # Then refreshes for the next attempt
                keyboard.press_and_release('ctrl+r')
                attempts += 1


if __name__ == '__main__':
    main()