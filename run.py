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
from PIL import Image, ImageDraw

# %%
load_dotenv()

IMAGES_PATH = os.environ["IMAGES_PATH"]
IMAGES_CAPTION = os.environ["IMAGES_CAPTION"]
IMAGES_COPYRIGHT = os.environ["IMAGES_COPYRIGHT"]
PASSWORD = os.environ["PASSWORD"]
USERNAME = os.environ["USERNAME"]


# %%
def main():
    """Main function."""
    images = os.listdir(IMAGES_PATH)
    image = random.choice(images)
    image_path_png = os.path.join(IMAGES_PATH, image)
    image = Image.open(image_path_png)

    draw = ImageDraw.Draw(image)
    draw.text(
        (image.width / 2 - len(IMAGES_COPYRIGHT) * 3, image.height - 16),
        IMAGES_COPYRIGHT,
        fill=(255, 255, 255, 128),
        align="center",
        anchor="mm",
    )
    image_path_jpg = image_path_png.replace(".png", ".jpg")
    image.save(image_path_jpg, "JPEG")

    try:
        ig = Client()
        ig.login(USERNAME, PASSWORD)
        ig.photo_upload(
            image_path_jpg,
            IMAGES_CAPTION,
        )
        os.remove(image_path_jpg)
        os.remove(image_path_png)
    except exceptions.PhotoNotUpload:
        os.remove(image_path_jpg)


# %%
if __name__ == "__main__":
    main()
