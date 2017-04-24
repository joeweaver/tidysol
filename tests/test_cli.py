"""Tests for our main skele CLI module."""


from subprocess import PIPE, Popen as popen
from unittest import TestCase

from tidysol import __version__ as VERSION


class TestHelp(TestCase):
    def test_returns_usage_information(self):
        output = popen(['tidysol', '-h'], stdout=PIPE,bufsize=16384).communicate()[0]
        self.assertTrue(b'Usage:' in output)

        output = popen(['tidysol', '--help'], stdout=PIPE,bufsize=16384).communicate()[0]
        self.assertTrue(b'Usage:' in output)


class TestVersion(TestCase):
    def test_returns_version_information(self):
        output = popen(['tidysol', '--version'], stdout=PIPE,bufsize=16384).communicate()[0].decode("utf-8")
        self.assertEqual(output.strip(), VERSION)
