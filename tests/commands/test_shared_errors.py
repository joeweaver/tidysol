"""Tests for errors common between mutliple tidysol commands which open
a comsol file.  For example  `tidysol times <name>`  and 'tidysol vars <name>.
Probably should report the same exact error if there is a missing % Description
field and that test should live in one and only one place."""


from subprocess import PIPE, Popen as popen
from unittest import TestCase

class TestSharedErrors(TestCase):
#==============================================================================
#     If the file does not exist or is is not given    
#==============================================================================
    #TODO check STDERR instead.
    #TODO exit with error code?
    
    #right now docopt coopts this and shows usage. I'd like to inject a line where it says it's failing due to the lack of a filename
    #for now, just showing usage is enough
    def test_error_no_filename(self):
        for c in ['times','vars']:
            with self.subTest(c=c):
                proc=popen(['tidysol', c], stdout=PIPE, stderr=PIPE)
                output,err =proc.communicate()
                err=err.decode("utf-8")
                lines = err.split('\n')
                self.assertTrue(len(lines) != 1)
                self.assertTrue('Usage:' in lines[0])
                
    def test_error_file_does_not_exist(self):
        #TODO can probably extract a function on the popen
        for c in ['times','vars']:
            with self.subTest(c=c):
                output = popen(['tidysol', c, 'tests\\commands\\data\\dne.txt'], stdout=PIPE).communicate()[0].decode("utf-8")
                assert('Could not find file: tests\\commands\\data\\dne.txt' == output.rstrip())