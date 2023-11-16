import unittest
from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path
import pickle
import os
from model.file_handler import FileHandler
from model.game_data import GameData


class TestFileHandler(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data='{"key": "value"}')
    def test_load_data_from_json(self, mock_file):
        # Setup
        handler = FileHandler()
        filename = "testfile"

        # Action
        result = handler.load_data_from_json(filename)

        # Assert
        expected_file_path = str(handler.root_dir / "data" / (filename + ".json"))
        mock_file.assert_called_with(expected_file_path)
        self.assertEqual(result, {"key": "value"})

    @patch('pickle.dump')
    @patch('builtins.open', new_callable=mock_open)
    @patch('tkinter.filedialog.asksaveasfilename', return_value="testpath.pkl")
    def test_save_game_with_pickle(self, mock_asksaveasfilename, mock_open, mock_pickle_dump):
        # Setup
        handler = FileHandler()
        game_data = {"level": 10, "score": 100}  # Example game data
        filename = "testgame"

        # Action
        handler.save_game_with_pickle(game_data, filename)

        # Assert
        mock_asksaveasfilename.assert_called_with(initialfile=filename, defaultextension=".pkl",
                                                  filetypes=[("Pickle Files", "*.pkl")])
        mock_open.assert_called_with("testpath.pkl", "wb")
        mock_pickle_dump.assert_called_with(game_data, mock_open())


class TestFileHandlerWithShelve(unittest.TestCase):

    @patch('tkinter.filedialog.asksaveasfilename', return_value="testpath.shelf")
    def test_save_game_with_shelve_file_dialog_interaction(self, mock_asksaveasfilename):
        # Setup
        handler = FileHandler()
        game_data = {"level": 20, "score": 200}

        # Action
        handler.save_game_with_shelve(game_data)

        # Assert
        mock_asksaveasfilename.assert_called_once_with(initialfile="", defaultextension=".shelf",
                                                       filetypes=[("Shelve Files", "*.shelf"), ("All Files", "*.*")])

    def test_save_game_with_shelve_with_filename(self):
        # Setup
        handler = FileHandler()
        game_data = {"level": 20, "score": 200}
        filename = "testgame"
        expected_file_base = str(handler.root_dir / "saves" / filename)

        # Check for any of the shelve files
        shelve_files_exist = any(os.path.exists(expected_file_base + ext) for ext in ['.db.dat', '.db.bak', '.db.dir'])

        print("Shelve files exist before method call:", shelve_files_exist)

        # Ensure the files do not exist before the test
        if shelve_files_exist:
            for ext in ['.db.dat', '.db.bak', '.db.dir']:
                os.remove(expected_file_base + ext)

        # Action
        handler.save_game_with_shelve(game_data, filename)

        # Assert
        shelve_files_exist = any(os.path.exists(expected_file_base + ext) for ext in ['.db.dat', '.db.bak', '.db.dir'])
        print("Shelve files exist after method call:", shelve_files_exist)
        self.assertTrue(shelve_files_exist)

        # Cleanup
        if shelve_files_exist:
            for ext in ['.db.dat', '.db.bak', '.db.dir']:
                os.remove(expected_file_base + ext)


# Run the tests
if __name__ == '__main__':
    unittest.main()
