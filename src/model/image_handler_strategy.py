"""
This module defines the ImageHandler class.

This serves as the context in the Strategy Design Pattern for image processing.
"""

from .image_strategy import ImageStrategy
from pathlib import Path
from PIL import Image, ImageOps


class ImageHandler:
    """
    The ImageHandler class.

    Serves as the context in the Strategy Design Pattern.
    It is configured with an ImageStrategy.
    Object to delegate the image processing tasks.
    """

    def __init__(self, strategy: ImageStrategy):
        """
        Initializes the ImageHandler with a specific image processing strategy.

        :param strategy: An instance of a class that implements ImageStrategy.
        """
        self.size = (150, 150)
        self.root_dir = Path(__file__).parent.parent / "data" / "Images"
        self.strategy = strategy

    def create_map_image(self, game_map, player, grid=(9, 9)):
        width, height = self.size
        image_size = (width * grid[1], height * grid[0])
        map_image = Image.new("RGB", image_size)

        for row in range(grid[0]):
            for col in range(grid[1]):
                offset = width * col, height * row
                tile = game_map[row][col]

                if tile == 0:
                    new_image = Image.open(str(self.root_dir) + "\\blank.png")
                else:
                    new_image = Image.open(str(self.root_dir) + "\\" + tile.img_src)
                    new_image = self.strategy.process_image(new_image, tile)

                new_image = ImageOps.fit(new_image, self.size, Image.ANTIALIAS)
                map_image.paste(new_image, offset)

        map_image.save(Path(__file__).parent.parent / "generated.png", "PNG")
