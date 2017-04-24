"""Tests for our `tidysol vars <name>` subcommand."""


from subprocess import PIPE, Popen as popen
from unittest import TestCase

class TestVars(TestCase):
        
    #try a simple file with one time step recorded   
    def test_single_timestep(self):
        output = popen(['tidysol', 'vars', 'tests\\commands\\data\\good-single-timestep.txt'], stdout=PIPE,bufsize=16384).communicate()[0].decode("utf-8")
        assert('x [ ], y [ ], z [ ], spf2.cellRe [Cell Reynolds number], p2 [Pressure], spf2.sr [Shear rate], u2 [Velocity field - x component], v2 [Velocity field - y component], w2 [Velocity field - z component], spf2.U [Velocity magnitude], spf2.Fx [Volume force - x component], spf2.Fy [Volume force - y component], spf2.Fz [Volume force - z component], spf2.vorticityx [Vorticity field - x component], spf2.vorticityy [Vorticity field - y component], spf2.vorticityz [Vorticity field - z component], spf2.vort_magn [Vorticity magnitude], dvol [Volume scale factor]' == output.rstrip())
        
    def test_multiple_timestep(self):
        output = popen(['tidysol', 'vars', 'tests\\commands\\data\\good-two-timestep.txt'], stdout=PIPE,bufsize=16384).communicate()[0].decode("utf-8")
        assert('x [ ], y [ ], z [ ], spf2.cellRe [Cell Reynolds number], p2 [Pressure], spf2.sr [Shear rate], u2 [Velocity field - x component], v2 [Velocity field - y component], w2 [Velocity field - z component], spf2.U [Velocity magnitude], spf2.Fx [Volume force - x component], spf2.Fy [Volume force - y component], spf2.Fz [Volume force - z component], spf2.vorticityx [Vorticity field - x component], spf2.vorticityy [Vorticity field - y component], spf2.vorticityz [Vorticity field - z component], spf2.vort_magn [Vorticity magnitude], dvol [Volume scale factor]' == output.rstrip())