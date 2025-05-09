import unittest

from tracklr.main import main


class TestMain(unittest.TestCase):
    def test_main(self):
        main(argv=["ls"])
