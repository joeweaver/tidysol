"""Tests for our `tidysol times <name>` subcommand."""

from subprocess import PIPE, Popen as popen
from unittest import TestCase

class TestTimes(TestCase):
        
    #try a simple file with one time step recorded   
    def test_single_timestep(self):
        output = popen(['tidysol', 'times', 'tests\\commands\\data\\good-single-timestep.txt'], stdout=PIPE).communicate()[0].decode("utf-8")
        assert('1.1' == output.rstrip())
        
    #try a simple file with two time steps recorded   
    def test_multiple_timestep(self):
        output = popen(['tidysol', 'times', 'tests\\commands\\data\\good-two-timestep.txt'], stdout=PIPE).communicate()[0].decode("utf-8")
        assert('0.1, 0.2' == output.rstrip())
    
    