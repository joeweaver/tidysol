"""Tests for our `tidysol tidy subcommand."""


from subprocess import PIPE, Popen as popen
from unittest import TestCase
import shutil, tempfile
import os

class TestTidy(TestCase):
    #temp directory method of testing files courtesy of  https://gist.github.com/odyniec/d4ea0959d4e0ba17a980
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)
            
    #time not found
    def test_single_timestep_time_not_found(self):
        time=12.3        
        expected = "Could not find data for time {0}".format(time)
        output = popen(['tidysol', 'tidy', 'tests\\commands\\data\\good-single-timestep.txt','--times={0}'.format(time)], stdout=PIPE,bufsize=16384).communicate()[0].decode("utf-8")
        assert(expected == output.rstrip())        
        
    #time is not correct format LAST or numerals and decimals
    #not explicitly testing regex here, just that if regex fails we get this
    def test_single_timestep_time_format_bad(self):
        time="twelve"        
        expected = "{0} is not a valid timestep. Only digits and a single decimal point allowed".format(time)
        output = popen(['tidysol', 'tidy', 'tests\\commands\\data\\good-single-timestep.txt','--times={0}'.format(time)], stdout=PIPE,bufsize=16384).communicate()[0].decode("utf-8")
        assert(expected == output.rstrip())  
    
    #base case for single time step, default time,defualt vars
    def test_single_timestep_all_default(self):     
        #TODO some odd gymnastics to handle test files and temp file writing. There's probably  a better way        
        fgold = open("tests\\commands\\data\\goldfiles\\single_timestep_all_default.csv")
        savewd = os.getcwd()
        shutil.copyfile('tests\\commands\\data\\good-single-timestep.txt',self.test_dir+"\\good-single-timestep.txt")
        os.chdir(self.test_dir)   
        popen(['tidysol', 'tidy', self.test_dir+"\\good-single-timestep.txt"], stdout=PIPE).communicate()[0].decode("utf-8")
        fwritten = open(self.test_dir+"\\good-single-timestep.csv")
        goldtext=fgold.read()
        writtentext=fwritten.read()
        fgold.close()
        fwritten.close()       
        os.chdir(savewd)       
        self.maxDiff=None
        self.assertMultiLineEqual(goldtext,writtentext)    
        
    #two time steps default time,defualt vars
    def test_multiple_timestep_all_default(self):   
        #TODO some odd gymnastics to handle test files and temp file writing. There's probably  a better way        
        fgold = open("tests\\commands\\data\\goldfiles\\two_timestep_all_default.csv")
        savewd = os.getcwd()
        shutil.copyfile('tests\\commands\\data\\good-two-timestep.txt',self.test_dir+"\\good-two-timestep.txt")
        os.chdir(self.test_dir)   
        popen(['tidysol', 'tidy', self.test_dir+"\\good-two-timestep.txt"], stdout=PIPE).communicate()[0].decode("utf-8")
        fwritten = open(self.test_dir+"\\good-two-timestep.csv")
        goldtext=fgold.read()
        writtentext=fwritten.read()
        fgold.close()
        fwritten.close()       
        os.chdir(savewd)     
        fdebug = open("tests\\debug-dump.txt","w")
        fdebug.write(writtentext)
        self.maxDiff=None
        self.assertMultiLineEqual(goldtext,writtentext)  
        
    #two time steps only first time,defualt vars, output to terminal
    
    #two time steps LAST kewword time,defualt vars, output to terminal
    
    #two time steps both times explicit keyword time,incorrect var name, output to terminal  
      
    #two time steps default time,do not inlcude pressure var, output to terminal 
        
    #two time steps default time,do not inlcude dat metadatar, output to terminal      
        
    #two time steps LAST kewword time,defualt vars, output to non-default file
    
    #test for duplicate specfied timesteps
    
    #test for duplicate specified vars
    
    #test for specified incorrect directory
