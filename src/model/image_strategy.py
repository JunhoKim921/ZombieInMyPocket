"""
This module defines strategies for image processing and their implementations.

It follows the Strategy Design Pattern to allow
interchangeable image processing behaviors.
"""

from abc import ABC, abstractmethod


class ImageStrategy(ABC):
    """
    Abstract base class representing an image processing strategy.

    Concrete implementations of this class
    should define specific image processing methods.
    """

    @abstractmethod
    def process_image(self, image):
        """
        Process an image according to the strategy.

        :param image: Image object to be processed.
        :return: Processed Image object.
        """
        pass
