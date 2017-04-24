"""Tests for our `tidysol meta <name>` subcommand."""


from subprocess import PIPE, Popen as popen
from unittest import TestCase
import ast

class TestMeta(TestCase):
        
    #return a dictionary-importable string of variables with values if --values  
    def test_single_timestep_with_descriptions(self):
        expected = "{'Dimension': '3', 'Date': 'Apr 5 2017, 16:28', 'Description': 'radius of rotating wall, non-rotating wall, rotations per min, Cell Reynolds number, Pressure, Shear rate, Velocity field, x component, Velocity field, y component, Velocity field, z component, Velocity magnitude, Volume force, x component, Volume force, y component, Volume force, z component, Vorticity field, x component, Vorticity field, y component, Vorticity field, z component, Vorticity magnitude, Volume scale factor, ', 'Expressions': '19', 'Nodes': '6', 'Model': '3d sliding wall - oCTB - Hyun 50.mph', 'Version': 'COMSOL 4.3.1.110'}"
        output = popen(['tidysol', 'meta', 'tests\\commands\\data\\good-single-timestep.txt','--values'], stdout=PIPE,bufsize=16384).communicate()[0].decode("utf-8")
        assert(ast.literal_eval(expected) == ast.literal_eval(output.rstrip()))

    #return a siple csv of metadata variable names (with commas replaced by ' - ') if --values is not true
    def test_single_timestep(self):
        expected = "Date, Description, Dimension, Expressions, Model, Nodes, Version"
        output = popen(['tidysol', 'meta', 'tests\\commands\\data\\good-single-timestep.txt'], stdout=PIPE,bufsize=16384).communicate()[0].decode("utf-8")
        assert(expected == output.rstrip())
