import unittest
import os
from unittest.mock import MagicMock

from PIL import Image
from model.image_handler import ImageHandler
from pathlib import Path


class TestImageHandler(unittest.TestCase):
    def setUp(self):
        # Configure the ImageHandler with a test-specific directory
        self.image_handler = ImageHandler()
        self.image_handler.root_dir = Path(__file__).parent / "test_images"

    def test_create_map_image_with_known_images(self):
        # Use a simple test map with known images
        test_game_map = [
            [MagicMock(rotate_factor=0, img_src="yard1.png"), MagicMock(rotate_factor=1, img_src="yard2.png")],
            [0, MagicMock(rotate_factor=2, img_src="yard3.png")]
        ]
        mock_player = MagicMock()
        output_path = Path(__file__).parent.parent / "generated_test.png"

        self.image_handler.create_map_image(test_game_map, mock_player)

        # Check if the image file was created
        self.assertTrue(os.path.exists(output_path))

        # Additional checks can be made here, e.g., image dimensions
        with Image.open(output_path) as generated_image:
            self.assertEqual(generated_image.size, (300, 300))  # Example check

        # Cleanup
        os.remove(output_path)

    def test_create_map_image_with_empty_game_map(self):
        test_game_map = []
        mock_player = MagicMock()
        output_path = Path(__file__).parent.parent / "generated_test_empty.png"

        with self.assertRaises(ValueError):
            self.image_handler.create_map_image(test_game_map, mock_player)

        self.assertFalse(os.path.exists(output_path))


if __name__ == '__main__':
    unittest.main()
