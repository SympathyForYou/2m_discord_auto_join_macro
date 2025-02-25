# Imports
from main import *

# Used libraries
import time  # Used to make program wait (sleep)
from datetime import datetime  # Used to tell the current time of the OS
from typing import Union  # Fixes type annotation
import pyautogui  # Used to move the cursor
from PIL.Image import Image  # Used to take screenshots (Server Full / Not)


def on_button(normal_color: tuple[int, int, int], hover_color: tuple[int, int,int]) -> Union[tuple[int, int], bool]:
    """
    Takes a 1 by 1 pixel screenshot, and it cheeks the color against the given colors
    :param normal_color: The rgb tuple of the normal color of the button you want to find
    :param hover_color: The rgb tuple of the hover color of button you want to find
    :return: The position of the button or False bool if it doesn't match
    """

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
    """
    It takes a screenshot of the entire screen each couple moments and tries to find the given image
    :param image: The path of the image you want to find
    :return: True or False
    """

    try:  # Tries to find the image if it can't it throws an error
        if pyautogui.locateOnScreen(image, grayscale=True, confidence=0.7) is not None:
            return True
    except pyautogui.ImageNotFoundException:
        return False  # Returns false (It didn't find)


def this_server_is_currently_full(output) -> bool | None:
    """
    Based on is_on_screen() // It tries to find the full server image
    :param output: True to display debug messages & False for not to
    :return: True or False
    """

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
    """
    Based on is_on_screen() // It tries to find the discord menu buttons
    :return: True or False
    """

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
    """
   It tries to find the captcha on the screen
   Based on is_on_screen(image)
    :return: True or False
    """
    if is_on_screen('images/are_you_human.png'):
        print("Human check on screen")
        return True
    else:
        print("No human check on screen")
        return False


def print_time() -> None:  # Basic timer
    """
    It elapses the time from run to end, and it prints in the output (E.g. the time it took to complete)
    Plus the current time (E.g. the time this script ended)
    """

    elapsed_time: float = time.time() - start
    minutes: int = int((elapsed_time // 60))
    seconds: int = int((elapsed_time % 60))
    print(f"Elapsed time: {minutes}:{seconds:02d}")

    # Get the current time of your system
    current_time = datetime.now()
    formatted_time = current_time.strftime("%H:%M:%S")
    print(f"Current time: {formatted_time}")