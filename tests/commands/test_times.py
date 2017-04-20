"""Tests for our `tidysol times <name>` subcommand."""


from subprocess import PIPE, Popen as popen
from unittest import TestCase

class TestTimes(TestCase):
#==============================================================================
#     If the file does not exist or is is not given    
#==============================================================================
    #TODO check STDERR instead.
    #TODO exit with error code?
    
    #right now docopt coopts this and shows usage. I'd like to inject a line where it says it's failing due to the lack of a filename
    #for now, just showing usage is enough
    def test_error_no_filename(self):
        proc=popen(['tidysol', 'times'], stdout=PIPE, stderr=PIPE)
        output,err =proc.communicate()
        err=err.decode("utf-8")
        lines = err.split('\n')
        self.assertTrue(len(lines) != 1)
        self.assertTrue('Usage:' in lines[0])

    def test_error_file_does_not_exist(self):
        #TODO can probably extract a function on the popen
        output = popen(['tidysol', 'times', 'dne.txt'], stdout=PIPE).communicate()[0].decode("utf-8")
        assert('Could not find file: dne.txt' in output)
    ###########################################################################    
    #potential parser issues (file does not appear to be COMSOL file or potential regex bugs
    ###########################################################################
    def test_error_multiple_vars_lines(self):
        output = popen(['tidysol', 'times', 'tests\\commands\\data\\bad-two-varsline.txt'], stdout=PIPE).communicate()[0].decode("utf-8")
        self.assertTrue('Found more than one line naming variables: 9 & 10' in output)        

    def test_error_no_vars_lines(self):
        output = popen(['tidysol', 'times', 'tests\\commands\\data\\bad-no-varsline.txt'], stdout=PIPE).communicate()[0].decode("utf-8")
        assert('Could not find a line defining variables' in output)  

    #these are a bit strict, but probably a good idea. Testing the file
    #for internal consistency

    #the number of variables found '% Expressions'' should be the same as
    #'% Dimension :' + the number of matches on the varsline
    def test_error_wrong_number_of_vars(self):
        output = popen(['tidysol', 'times', 'tests\\commands\\data\\bad-wrong-num-vars.txt'], stdout=PIPE).communicate()[0].decode("utf-8")
        assert('Expected 21 variables (3 dimensions and 18 expressions) but found 22 (3 dimensions and 19 expressions)' in output)  

    #sub case of test_error_wrong_number_of_vars if %Expressions is not given
    def test_error_no_expressions_meta(self):
        output = popen(['tidysol', 'times', 'tests\\commands\\data\\bad-no-expressionsmeta.txt'], stdout=PIPE).communicate()[0].decode("utf-8")
        assert('Could not find an % Expressions line' in output)
        
    #sub case of test_error_wrong_number_of_vars if %Dimension is not given
    def test_error_no_dimensions_meta(self):
        output = popen(['tidysol', 'times', 'tests\\commands\\data\\bad-no-dimensionsmeta.txt'], stdout=PIPE).communicate()[0].decode("utf-8")
        assert('Could not find a % Dimensions line' in output)

    #TODO handle vars counting when more than one time step is recorded

    #the number of lines which do not begin with % should be the same as the
    #% nodes value in the metadata
    def test_error_wrong_num_nodes(self):
        output = popen(['tidysol', 'times', 'tests\\commands\\data\\bad-wrong-num-nodes.txt'], stdout=PIPE).communicate()[0].decode("utf-8")
        assert('Expected 5 nodes but read 6' in output)    
    
    #sub case of test_error_wrong_number_of_nodes if % nodes is not given
    def test_error_no_nodes_meta(self):
        output = popen(['tidysol', 'times', 'tests\\commands\\data\\bad-no-nodesmeta.txt'], stdout=PIPE).communicate()[0].decode("utf-8")
        assert('Could not find a % Nodes line' in output)
        
    #The number of descriptions is the same as number listed in % Expressions
    #descriptions are allowed to be a blank string    
    #unfortunately, descriptions can also contain unescaped commas - such as: Velocity field, z component
    def test_error_wrong_num_descriptions(self):
        output = popen(['tidysol', 'times', 'tests\\commands\\data\\bad-wrong-num-descriptions.txt'], stdout=PIPE).communicate()[0].decode("utf-8")
        assert('Expected 18 descriptions of variables but read 20' in output)
    
    #sub case of test_error_wrong_num_descriptions if % descriptions not given    
    def test_error_no_description_meta(self):
        output = popen(['tidysol', 'times', 'tests\\commands\\data\\bad-no-descriptionsmeta.txt'], stdout=PIPE).communicate()[0].decode("utf-8")
        assert('Could not find a % Description line' in output)
    
    
    #try a simple file with one tim step recorded   
    def test_sing_timestep(self):
        output = popen(['tidysol', 'times', 'tests\\commands\\data\\good-single-timestep.txt'], stdout=PIPE).communicate()[0].decode("utf-8")
        assert('1.1' in output)
        
    #TODO    
    #should only have one '%<FOO> :' line in header per <FOO>
    #this exists to make sure that we are reading the correct 'Expressions'
    #for example, when checking internal file consistency

    #TODO double check if the header always includes the metadata
    

"""  def test_error_file_is_not_COMSOL_export(self):
        self.assertTrue(False)

    #fails if #cols not what predicted by timestep 
    def test_error_timestep_vs_cols_sanity_test(self):
        self.assertTrue(False)

    #try for two files with single different timestep values
    def test_identifies_single_timestep(self):
        self.assertTrue(False)

    #try for two files, each containing a different number of timesteps with different values
    def test_identifies_single_timestep(self):
        self.assertTrue(False)    
"""
"""    def test_returns_multiple_lines(self):
        output = popen(['tidysol', 'hello'], stdout=PIPE).communicate()[0].decode("utf-8")
        lines = output.split('\n')
        self.assertTrue(len(lines) != 1)

    def test_returns_hello_world(self):
        output = popen(['tidysol', 'hello'], stdout=PIPE).communicate()[0]
        self.assertTrue(b'Hello, world!' in output)"""
