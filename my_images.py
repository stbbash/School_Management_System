import os
import sys

import PyInstaller


def get_favicon():
    if not os.path.exists("favicon.ico"):
        try:
            temp_dir = sys._MEIPASS
            favicon = os.path.join(temp_dir, "favicon.ico")
        except Exception as e:
            print(f"{e}: Error getting image")
        try:
            favicon = PyInstaller.resource_path("favicon.ico")
        except Exception as e:
            print(f"{e}: Error getting image")
        try:
            script_dir = os.path.dirname(__file__)
            favicon = os.path.join(script_dir, "favicon.ico")
        except Exception as e:
            print(f"{e}: Error getting image")
    elif os.path.exists("favicon.gif/favicon.ico"):
        favicon = "favicon.gif/favicon.ico"
    else:
        favicon = "favicon.ico"
    return favicon


def get_gif():
    if not os.path.exists("favicon.gif"):
        try:
            temp_dir = sys._MEIPASS
            gif = os.path.join(temp_dir, "favicon.gif")
        except Exception as e:
            print(f"{e}: Error getting image")
        try:
            gif = PyInstaller.resource_path("favicon.gif")
        except Exception as e:
            print(f"{e}: Error getting image")
        try:
            script_dir = os.path.dirname(__file__)
            gif = os.path.join(script_dir, "favicon.gif")
        except Exception as e:
            print(f"{e}: Error getting image")
    elif os.path.exists("favicon.gif/favicon.gif"):
        gif = "favicon.gif/favicon.gif"
    else:
        gif = "favicon.gif"
    return gif


def get_bg_image():
    if not os.path.exists("background_image.jpg"):
        try:
            temp_dir = sys._MEIPASS
            bg_image = os.path.join(temp_dir, "background_image.jpg")
        except Exception as e:
            print(f"{e}: Error getting image")
        try:
            bg_image = PyInstaller.resource_path("background_image.jpg")
        except Exception as e:
            print(f"{e}: Error getting image")
        try:
            script_dir = os.path.dirname(__file__)
            bg_image = os.path.join(script_dir, "background_image.jpg")
        except Exception as e:
            print(f"{e}: Error getting image")
    elif os.path.exists("background_image.jpg/background_image.jpg"):
        favicon = "background_image.jpg/background_image.jpg"
    else:
        bg_image = "background_image.jpg"
    return bg_image


favicon_image = get_favicon()
gif_image = get_gif()
background_image = get_bg_image()
