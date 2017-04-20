"""Tests for our `tidysol times <name>` subcommand."""

from unittest import TestCase
import sys
sys.path.append('..')
from tidysol import ComsolExportFile
from tidysol.Exceptions import TidysolException

class TestComsolExportFile(TestCase):
        def test_error_file_does_not_exist(self):
            with self.assertRaises(TidysolException) as context:
                ComsolExportFile('tests\\commands\\data\\dne.txt')
            assert('Could not find file: tests\\commands\\data\\dne.txt'==str(context.exception))
