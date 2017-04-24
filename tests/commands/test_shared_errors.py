"""Tests for errors common between mutliple tidysol commands which open
a comsol file.  For example  `tidysol times <name>`  and 'tidysol vars <name>.
Probably should report the same exact error if there is a missing % Description
field and that test should live in one and only one place."""


from subprocess import PIPE, Popen as popen
from unittest import TestCase

class TestSharedErrors(TestCase):
    def setUp(self):
        self.commands=['times','vars','meta']

#==============================================================================
#     If the file does not exist or is is not given    
#==============================================================================
    #TODO check STDERR instead.
    #TODO exit with error code?
    
    #right now docopt coopts this and shows usage. I'd like to inject a line where it says it's failing due to the lack of a filename
    #for now, just showing usage is enough
    def test_error_no_filename(self):
        for c in self.commands:
            with self.subTest(c=c):
                proc=popen(['tidysol', c], stdout=PIPE, stderr=PIPE)
                output,err =proc.communicate()
                err=err.decode("utf-8")
                lines = err.split('\n')
                self.assertTrue(len(lines) != 1)
                self.assertTrue('Usage:' in lines[0])
                
    def test_error_file_does_not_exist(self):
        #TODO can probably extract a function on the popen
        for c in self.commands:
            with self.subTest(c=c):
                output = popen(['tidysol', c, 'tests\\commands\\data\\dne.txt'], stdout=PIPE).communicate()[0].decode("utf-8")
                assert('Could not find file: tests\\commands\\data\\dne.txt' == output.rstrip())
                
                       
#==============================================================================
#  potential parser issues (file does not appear to be COMSOL file or potential regex bugs
#==============================================================================
    def test_error_multiple_vars_lines(self):
        for c in self.commands:
            with self.subTest(c=c):   
                output = popen(['tidysol', c, 'tests\\commands\\data\\bad-two-varsline.txt'], stdout=PIPE).communicate()[0].decode("utf-8")
                assert('Found more than one line naming variables: 9 & 10' == output.rstrip())
                
    def test_error_no_vars_lines(self):
        for c in self.commands:
            with self.subTest(c=c): 
                output = popen(['tidysol', c, 'tests\\commands\\data\\bad-no-varsline.txt'], stdout=PIPE).communicate()[0].decode("utf-8")
                assert('Could not find a line defining variables' == output.rstrip())  
                
    #these are a bit strict, but probably a good idea. Testing the file
    #for internal consistency

    #the number of variables found '% Expressions'' should be the same as
    #'% Dimension :' + the number of matches on the varsline
    def test_error_wrong_number_of_vars(self):
        for c in self.commands:
            with self.subTest(c=c): 
                output = popen(['tidysol', c, 'tests\\commands\\data\\bad-wrong-num-vars.txt'], stdout=PIPE).communicate()[0].decode("utf-8")
                assert('Expected 21 variables (3 dimensions and 18 expressions) but found 22 (3 dimensions and 19 expressions)' == output.rstrip())  


    #sub case of test_error_wrong_number_of_vars if %Expressions is not given
    def test_error_no_expressions_meta(self):
        for c in self.commands:
            with self.subTest(c=c):
                output = popen(['tidysol', c, 'tests\\commands\\data\\bad-no-expressionsmeta.txt'], stdout=PIPE).communicate()[0].decode("utf-8")
                assert('Could not find an % Expressions line' == output.rstrip())
        
    #sub case of test_error_wrong_number_of_vars if %Dimension is not given
    def test_error_no_dimensions_meta(self):
        for c in self.commands:
            with self.subTest(c=c):
                output = popen(['tidysol', c, 'tests\\commands\\data\\bad-no-dimensionsmeta.txt'], stdout=PIPE).communicate()[0].decode("utf-8")
                assert('Could not find a % Dimensions line' == output.rstrip())
                
    #the number of lines which do not begin with % should be the same as the
    #% nodes value in the metadata
    def test_error_wrong_num_nodes(self):
        for c in self.commands:
            with self.subTest(c=c):
                output = popen(['tidysol', c, 'tests\\commands\\data\\bad-wrong-num-nodes.txt'], stdout=PIPE).communicate()[0].decode("utf-8")
                assert('Expected 5 nodes but read 6' == output.rstrip())    
    
    #sub case of test_error_wrong_number_of_nodes if % nodes is not given
    def test_error_no_nodes_meta(self):
        for c in self.commands:
            with self.subTest(c=c):
                output = popen(['tidysol', c, 'tests\\commands\\data\\bad-no-nodesmeta.txt'], stdout=PIPE).communicate()[0].decode("utf-8")
                assert('Could not find a % Nodes line' == output.rstrip())
        
    #The number of descriptions is the same as number listed in % Expressions
    #descriptions are allowed to be a blank string    
    #unfortunately, descriptions can also contain unescaped commas - such as: Velocity field, z component
    def test_error_wrong_num_descriptions(self):
        for c in self.commands:
            with self.subTest(c=c):
                output = popen(['tidysol', c, 'tests\\commands\\data\\bad-wrong-num-descriptions.txt'], stdout=PIPE).communicate()[0].decode("utf-8")
                assert('Expected 19 descriptions of variables but read 21' == output.rstrip())
    
    #sub case of test_error_wrong_num_descriptions if % descriptions not given    
    def test_error_no_description_meta(self):
        for c in self.commands:
            with self.subTest(c=c):
                output = popen(['tidysol', c, 'tests\\commands\\data\\bad-no-descriptionsmeta.txt'], stdout=PIPE).communicate()[0].decode("utf-8")
                assert('Could not find a % Description line' == output.rstrip())