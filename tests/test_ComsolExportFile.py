"""Tests for our `tidysol times <name>` subcommand."""

from unittest import TestCase
import sys
sys.path.append('..')
from tidysol import ComsolExportFile
from tidysol.Exceptions import TidysolException

class TestComsolExportFile(TestCase):
    ###########################################################################    
    #Do better than standard file not found error
    ###########################################################################
    def test_error_file_does_not_exist(self):
        with self.assertRaises(TidysolException) as context:
            ComsolExportFile('tests\\commands\\data\\dne.txt')
        assert('Could not find file: tests\\commands\\data\\dne.txt'==str(context.exception))

    ###########################################################################    
    #potential parser issues (file does not appear to be COMSOL file or potential regex bugs
    ###########################################################################
    def test_error_multiple_vars_lines(self):
        with self.assertRaises(TidysolException) as context:
            ComsolExportFile('tests\\commands\\data\\bad-two-varsline.txt')
        assert('Found more than one line naming variables: 9 & 10' == str(context.exception)) 
        
    def test_error_no_vars_lines(self):
        with self.assertRaises(TidysolException) as context:
            ComsolExportFile('tests\\commands\\data\\bad-no-varsline.txt')
        assert('Could not find a line defining variables' == str(context.exception)) 
        
    #these are a bit strict, but probably a good idea. Testing the file
    #for internal consistency

    #the number of variables found '% Expressions'' should be the same as
    #'% Dimension :' + the number of matches on the varsline
    def test_error_wrong_number_of_vars(self):
        with self.assertRaises(TidysolException) as context:
            ComsolExportFile('tests\\commands\\data\\bad-wrong-num-vars.txt')
        assert('Expected 21 variables (3 dimensions and 18 expressions) but found 22 (3 dimensions and 19 expressions)' == str(context.exception)) 

    #sub case of test_error_wrong_number_of_vars if %Expressions is not given
    def test_error_no_expressions_meta(self):
        with self.assertRaises(TidysolException) as context:
            ComsolExportFile('tests\\commands\\data\\bad-no-expressionsmeta.txt')
        assert('Could not find a \"% Expressions:\" line' == str(context.exception))

    #sub case of test_error_wrong_number_of_vars if %Dimensions is not given
    def test_error_no_dimensions_meta(self):
        with self.assertRaises(TidysolException) as context:
            ComsolExportFile('tests\\commands\\data\\bad-no-dimensionsmeta.txt')
        assert('Could not find a \"% Dimension:\" line' == str(context.exception))
        
    #the number of lines which do not begin with % should be the same as the
    #% nodes value in the metadata
    def test_error_wrong_num_nodes(self):
        with self.assertRaises(TidysolException) as context:
            ComsolExportFile('tests\\commands\\data\\bad-wrong-num-nodes.txt')
        assert('Expected 5 nodes but read 6' == str(context.exception))

    #sub case of test_error_wrong_number_of_nodes if % nodes is not given
    def test_error_no_nodes_meta(self):
        with self.assertRaises(TidysolException) as context:
            ComsolExportFile('tests\\commands\\data\\bad-no-nodesmeta.txt')
        assert('Could not find a \"% Nodes:\" line' == str(context.exception))
        
    #The number of descriptions is the same as number listed in % Expressions
    #descriptions are allowed to be a blank string    
    #unfortunately, descriptions can also contain unescaped commas - such as: Velocity field, z component
    def test_error_wrong_num_descriptions(self):
        with self.assertRaises(TidysolException) as context:
            ComsolExportFile('tests\\commands\\data\\bad-wrong-num-descriptions.txt')
        assert('Expected 19 descriptions of variables but read 21' == str(context.exception))
        
    #sub case of test_error_wrong_num_descriptions if % descriptions not given    
    def test_error_no_description_meta(self):
        with self.assertRaises(TidysolException) as context:
            ComsolExportFile('tests\\commands\\data\\bad-no-descriptionsmeta.txt')
        assert('Could not find a \"% Description:\" line' == str(context.exception))
    