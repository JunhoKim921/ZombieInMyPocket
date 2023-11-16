"""
This module defines the RotateImageStrategy class.

This is a concrete implementation of the ImageStrategy interface.
It provides a strategy for rotating images, specifically
implementing a 90-degree rotation.
"""

from image_strategy import ImageStrategy


class RotateImageStrategy(ImageStrategy):
    """Concrete strategy class for rotating an image."""

    def process_image(self, image):
        """
        Rotates the given image by 90 degrees.

        :param image: Image object to be rotated.
        :return: Rotated Image object.
        """
        rotated_image = image.rotate(90)
        return rotated_image
