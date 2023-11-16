"""
This module provides the ResizeImageStrategy class.

A concrete strategy conforming to the ImageStrategy interface.
It focuses on resizing images to a specific size.
"""

from image_strategy import ImageStrategy
from PIL import Image, ImageOps


class ResizeImageStrategy(ImageStrategy):
    """Concrete strategy class for resizing an image."""

    def process_image(self, image):
        """
        Resizes the image to a predefined size.

        :param image: Image object to be resized.
        :return: Resized Image object.
        """
        size = (150, 150)  # Define the target size
        resized_image = ImageOps.fit(image, size, Image.ANTIALIAS)
        return resized_image
