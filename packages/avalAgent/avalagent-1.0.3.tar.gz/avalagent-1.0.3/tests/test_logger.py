
import unittest
import logging
from avalAgent.logger import get_logger

class TestLogger(unittest.TestCase):

    def test_logger_initialization(self):
        logger = get_logger("TestLogger")
        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(logger.name, "TestLogger")

    def test_logger_error(self):
        logger = get_logger("TestLogger")
        with self.assertLogs(logger, level="ERROR") as log:
            logger.error("This is an error")
        self.assertIn("This is an error", log.output[0])

if __name__ == "__main__":
    unittest.main()
