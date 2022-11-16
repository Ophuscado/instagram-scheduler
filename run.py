#!.venv/bin/python

"""
Instagram Scheduler

Publishes a random image from a folder to Instagram.
"""

# %%
import os
import random

from dotenv import load_dotenv
from instagrapi import Client, exceptions
from PIL import Image

# %%
load_dotenv()

IMAGES_PATH = os.environ["IMAGES_PATH"]
IMAGES_CAPTION = os.environ["IMAGES_CAPTION"]
USERNAME = os.environ["USERNAME"]
PASSWORD = os.environ["PASSWORD"]


# %%
def main():
    """Main function."""
    cl = Client()
    cl.login(USERNAME, PASSWORD)

    images = os.listdir(IMAGES_PATH)
    image = random.choice(images)
    image_path_png = os.path.join(IMAGES_PATH, image)

    # From PNG to JPG
    image = Image.open(image_path_png)
    image = image.convert("RGB")
    image_path_jpg = image_path_png.replace(".png", ".jpg")
    image.save(image_path_jpg, "JPEG")

    try:
        cl.photo_upload(
            image_path_jpg,
            IMAGES_CAPTION,
        )
        os.remove(image_path_jpg)
        os.remove(image_path_png)
    except exceptions.PhotoNotUpload:
        os.remove(image_path_jpg)
        print("Photo not uploaded.")


# %%
if __name__ == "__main__":
    main()
