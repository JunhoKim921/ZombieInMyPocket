from PIL import Image, ImageOps
from pathlib import Path


class ImageHandler:
    def __init__(self):
        self.size = (150, 150)
        self.root_dir = Path(__file__).parent.parent / "data" / "Images"

    def create_map_image(self, game_map, player, grid=(9, 9)):
        width, height = self.size
        image_size = (width * grid[1], height * grid[0])
        map_image = Image.new("RGB", image_size)

        # Check if game_map size matches the grid size
        if len(game_map) != grid[0] or any(len(row) != grid[1] for row in game_map):
            raise ValueError("game_map size does not match the expected grid size.")

        for row in range(grid[0]):
            for col in range(grid[1]):
                offset = width * col, height * row
                tile = game_map[row][col]

                if tile == 0:
                    new_image = Image.open(str(self.root_dir) + "\\blank.png")
                else:
                    new_image = Image.open(str(self.root_dir) + "\\" + tile.img_src)

                    # Rotate the image based on tile's rotate factor
                    rotated_image = None
                    match tile.rotate_factor:
                        case 0:
                            rotated_image = new_image
                        case 1:
                            rotated_image = new_image.rotate(270)
                        case 2:
                            rotated_image = new_image.rotate(180)
                        case 3:
                            rotated_image = new_image.rotate(90)

                    new_image = ImageOps.fit(rotated_image, self.size, Image.ANTIALIAS)

                map_image.paste(new_image, offset)

        map_image.save(Path(__file__).parent.parent / "generated.png", "PNG")
