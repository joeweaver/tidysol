"""Tests for our `tidysol times <name>` subcommand."""


from subprocess import PIPE, Popen as popen
from unittest import TestCase

class TestVars(TestCase):
    
    #right now docopt coopts this and shows usage. I'd like to inject a line where it says it's failing due to the lack of a filename
    #for now, just showing usage is enough
    def test_error_no_filename(self):
        proc=popen(['tidysol', 'vars'], stdout=PIPE, stderr=PIPE)
        output,err =proc.communicate()
        err=err.decode("utf-8")
        lines = err.split('\n')
        self.assertTrue(len(lines) != 1)
        self.assertTrue('Usage:' in lines[0])
        
    def test_true(self):
        assert(True)
    #For file format error handling I could probably just assert that this command calls the to be written
    #ComsolExportFile class
    #Actually, I prefer to test the parsing class, which should only throw
    #exceptions, then make sure that either this class or the command
    #base turns those exceptions into ap
#==============================================================================
#     If the file does not exist or is is not given    
#==============================================================================
    #TODO check STDERR instead.
    #TODO exit with error code?
#    expected='x,y,z,wrad [radius of rotating wall],stabrad [non-rotating wall],rotPM [rotations per min],spf2.cellRe [Cell Reynolds number],p2 [Pressure],spf2.sr [Shear rate],u2 ["Velocity field, x component"],v2 ["Velocity field, y component"],w2 ["Velocity field, z component"],spf2.U [Velocity magnitude],spf2.Fx ["Volume force, x component"],spf2.Fy ["Volume force, y component"],spf2.Fz ["Volume force, z component"],spf2.vorticityx ["Vorticity field, x component"],spf2.vorticityy ["Vorticity field, y component"],spf2.vorticityz ["Vorticity field, z component"],spf2.vort_magn [Vorticity magnitude],dvol [Volume scale factor],meshtype'
#    
#    #try a simple file with one time step recorded   
#    def test_single_timestep(self):
#        output = popen(['tidysol', 'vars', 'tests\\commands\\data\\good-single-timestep.txt'], stdout=PIPE).communicate()[0].decode("utf-8")            
#        assert(self.expected in output)
#        
#    #try a simple file with two timee step recorded   
#    def test_multiple_timestep(self):
#        output = popen(['tidysol', 'times', 'tests\\commands\\data\\good-two-timestep.txt'], stdout=PIPE).communicate()[0].decode("utf-8")
#        assert(self.expected in output)
        
    #TODO    
    #should only have one '%<FOO> :' line in header per <FOO>
    #this exists to make sure that we are reading the correct 'Expressions'
    #for example, when checking internal file consistency

    #TODO double check if the header always includes the metadata
