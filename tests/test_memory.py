import tempfile
import unittest
from pathlib import Path
from datetime import datetime
from memory import save, history, clear

class MemoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.db = Path(self.temp.name) / "test.db"

    def tearDown(self):
        self.temp.cleanup()

    def test_initially_empty(self):
        self.assertEqual(history(path=self.db), [])

    def test_save_message(self):
        save("user", "hello", self.db)
        self.assertEqual(history(path=self.db)[0][1], "hello")

    def test_order(self):
        save("user", "first", self.db)
        save("user", "second", self.db)
        self.assertEqual(
            [row[1] for row in history(path=self.db)],
            ["first", "second"]
        )

    def test_timestamp(self):
        timestamp = save("user", "hello", self.db)
        self.assertIsNotNone(
            datetime.fromisoformat(timestamp).tzinfo
        )

    def test_clear(self):
        save("user", "hello", self.db)
        clear(self.db)
        self.assertEqual(history(path=self.db), [])

if __name__ == "__main__":
    unittest.main()
