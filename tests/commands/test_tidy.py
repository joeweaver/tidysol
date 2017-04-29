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
        expected = "{0} is not a valid timestep".format(time)
        output = popen(['tidysol', 'tidy', 'tests\\commands\\data\\good-single-timestep.txt','--times={0}'.format(time)], stdout=PIPE,bufsize=16384).communicate()[0].decode("utf-8")
        assert(expected == output.rstrip())  
    
    #base case for single time step, default time,defualt vars
    def test_single_timestep_all_default(self):     
        #TODO some odd gymnastics to handle test files and temp file writing. There's probably  a better way        
        #TODO should probably factor out all the common file handling in the next few tests        
        fgold = open("tests\\commands\\data\\goldfiles\\single_timestep_all_default.csv")
        savewd = os.getcwd()
        shutil.copyfile('tests\\commands\\data\\good-single-timestep.txt',self.test_dir+"\\good-single-timestep.txt")
        os.chdir(self.test_dir)   
        fwritten=None
        try:        
            popen(['tidysol', 'tidy', self.test_dir+"\\good-single-timestep.txt"], stdout=PIPE).communicate()[0].decode("utf-8")
            fwritten = open(self.test_dir+"\\good-single-timestep.csv")
            goldtext=fgold.read()
            writtentext=fwritten.read()
            self.maxDiff=None
            self.assertMultiLineEqual(goldtext,writtentext)    
        finally:
            os.chdir(savewd)     
            fgold.close()
            if fwritten is not None:
                fwritten.close()      
            os.chdir(savewd)   
        
    #two time steps default time,defualt vars
    def test_multiple_timestep_all_default(self):   
        #TODO some odd gymnastics to handle test files and temp file writing. There's probably  a better way        
        fgold = open("tests\\commands\\data\\goldfiles\\two_timestep_all_default.csv")
        fdebug= open("tests\\debug-dump.txt","w")
        fwritten=None
        savewd = os.getcwd()
        shutil.copyfile('tests\\commands\\data\\good-two-timestep.txt',self.test_dir+"\\good-two-timestep.txt")
        os.chdir(self.test_dir)   
        try:        
            popen(['tidysol', 'tidy', self.test_dir+"\\good-two-timestep.txt"], stdout=PIPE).communicate()[0].decode("utf-8")
            fwritten = open(self.test_dir+"\\good-two-timestep.csv")
            goldtext=fgold.read()
            writtentext=fwritten.read()
            fgold.close()
            fwritten.close()       
            os.chdir(savewd)     

            fdebug.write(writtentext)
            self.maxDiff=None
            self.assertMultiLineEqual(goldtext,writtentext)
        finally:
            os.chdir(savewd)     
            fgold.close()
            if fwritten is not None:
                fwritten.close()
            fdebug.close()
            os.chdir(savewd)   
        
    #two time steps only first time,defualt vars
    def test_multiple_timestep_first_timestep(self):   
        #TODO some odd gymnastics to handle test files and temp file writing. There's probably  a better way        
        fgold = open("tests\\commands\\data\\goldfiles\\two_timestep_first_only.csv")     
        fdebug= open("tests\\debug-dump.txt","w")
        fwritten=None
        savewd = os.getcwd()
        shutil.copyfile('tests\\commands\\data\\good-two-timestep.txt',self.test_dir+"\\good-two-timestep.txt")
        os.chdir(self.test_dir)  
        try:
            popen(['tidysol', 'tidy', self.test_dir+"\\good-two-timestep.txt",'--times=0.1'], stdout=PIPE).communicate()[0].decode("utf-8")
            fwritten = open(self.test_dir+"\\good-two-timestep.csv") 
            goldtext=fgold.read()
            writtentext=fwritten.read()
            fgold.close()
            fwritten.close()       
            os.chdir(savewd)     

            fdebug.write(writtentext)
            self.maxDiff=None
            self.assertMultiLineEqual(goldtext,writtentext)
        finally:
            os.chdir(savewd)     
            fgold.close()
            fdebug.close()
            os.chdir(savewd)
            if fwritten is not None:
                fwritten.close()

    #two time steps LAST kewword time,defualt vars
    #TODO bother with making sure last is case insensitive?
    def test_multiple_timestep_last_keyword(self):   
        #TODO some odd gymnastics to handle test files and temp file writing. There's probably  a better way        
        fgold = open("tests\\commands\\data\\goldfiles\\two_timestep_second_only.csv")     
        fdebug= open("tests\\debug-dump.txt","w")
        fwritten=None
        savewd = os.getcwd()
        shutil.copyfile('tests\\commands\\data\\good-two-timestep.txt',self.test_dir+"\\good-two-timestep.txt")
        os.chdir(self.test_dir)  
        try:
            popen(['tidysol', 'tidy', self.test_dir+"\\good-two-timestep.txt",'--times=LAST'], stdout=PIPE).communicate()[0].decode("utf-8")
            fwritten = open(self.test_dir+"\\good-two-timestep.csv") 
            goldtext=fgold.read()
            writtentext=fwritten.read()
            fgold.close()
            fwritten.close()       
            os.chdir(savewd)     

            fdebug.write(writtentext)
            self.maxDiff=None
            self.assertMultiLineEqual(goldtext,writtentext)
        finally:
            os.chdir(savewd)     
            fgold.close()
            fdebug.close()
            os.chdir(savewd)  
            if fwritten is not None:
                fwritten.close()
                
    #two time steps both times explicit keyword time,incorrect var name  
    def test_multiple_timestep_bad_var_name(self):   
        badvar="spf.sr"
        expected = "Could not find data for variable {0}".format(badvar)        
        output=popen(['tidysol', 'tidy', 'tests\\commands\\data\\good-single-timestep.txt','--cols={0}'.format(badvar)], stdout=PIPE).communicate()[0].decode("utf-8")
        assert(expected == output.rstrip())     
                
    #two time steps default time,only inlcude shear rate var
    #just name 'spf2.sr'
    def test_multiple_timestep_only_one_var(self):   
        #TODO some odd gymnastics to handle test files and temp file writing. There's probably  a better way        
        fgold = open("tests\\commands\\data\\goldfiles\\two_timestep_one_var.csv")     
        fdebug= open("tests\\debug-dump.txt","w")
        fwritten=None
        savewd = os.getcwd()
        shutil.copyfile('tests\\commands\\data\\good-two-timestep.txt',self.test_dir+"\\good-two-timestep.txt")
        os.chdir(self.test_dir)  
        try:
            popen(['tidysol', 'tidy', self.test_dir+"\\good-two-timestep.txt",'--cols=spf2.sr'], stdout=PIPE).communicate()[0].decode("utf-8")
            fwritten = open(self.test_dir+"\\good-two-timestep.csv") 
            goldtext=fgold.read()
            writtentext=fwritten.read()
            fgold.close()
            fwritten.close()       
            os.chdir(savewd)     

            fdebug.write(writtentext)
            self.maxDiff=None
            self.assertMultiLineEqual(goldtext,writtentext)
        finally:
            os.chdir(savewd)     
            fgold.close()
            fdebug.close()
            os.chdir(savewd)  
            if fwritten is not None:
                fwritten.close()
                
    #name with desc spf2.sr [Shear rate]
    def test_multiple_timestep_only_one_var_w_desc(self):   
        #TODO some odd gymnastics to handle test files and temp file writing. There's probably  a better way        
        fgold = open("tests\\commands\\data\\goldfiles\\two_timestep_one_var.csv")     
        fdebug= open("tests\\debug-dump.txt","w")
        fwritten=None
        savewd = os.getcwd()
        shutil.copyfile('tests\\commands\\data\\good-two-timestep.txt',self.test_dir+"\\good-two-timestep.txt")
        os.chdir(self.test_dir)  
        try:
            output=popen(['tidysol', 'tidy', self.test_dir+"\\good-two-timestep.txt",'--cols="spf2.sr [Shear rate]"'], stdout=PIPE).communicate()[0].decode("utf-8")
            print(output)            
            fwritten = open(self.test_dir+"\\good-two-timestep.csv") 
            goldtext=fgold.read()
            writtentext=fwritten.read()
            fgold.close()
            fwritten.close()       
            os.chdir(savewd)     

            fdebug.write(writtentext)
            self.maxDiff=None
            self.assertMultiLineEqual(goldtext,writtentext)
        finally:
            os.chdir(savewd)     
            fgold.close()
            fdebug.close()
            os.chdir(savewd)  
            if fwritten is not None:
                fwritten.close()         
    #two time steps both times explicit keyword time,incorrect var desc  
                 
                
    #same with two vars
    #two time steps default time,do not inlcude dat metadatar, output to terminal      
        
    #two time steps LAST kewword time,defualt vars, output to non-default file & directory
        
    #dir does not exist
        
    #large file?
    
    #NOHEAD for headers
    
    #test for duplicate specfied timesteps
    
    #test for duplicate specified vars
    
    #test for specified incorrect directory
