"""Tests for our `tidysol tidy subcommand."""


from subprocess import PIPE, Popen as popen
from unittest import TestCase
import shutil, tempfile
import os
import re

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
        #one option is to test the output string in  ComsolExportFile to_csv() then either trust tidy to make the correct call to_csv and write file
        #or do a little mocking
        #TODO should probably factor out all the common file handling in the next few tests        
        fgold = open("tests\\commands\\data\\goldfiles\\single_timestep_all_default.csv")
        savewd = os.getcwd()
        shutil.copyfile('tests\\commands\\data\\good-single-timestep.txt',self.test_dir+"\\good-single-timestep.txt")
        fdebug= open("tests\\debug-dump.txt","w")
        os.chdir(self.test_dir)   
        fwritten=None
        try:        
            popen(['tidysol', 'tidy', self.test_dir+"\\good-single-timestep.txt"], stdout=PIPE).communicate()[0].decode("utf-8")
            fwritten = open(self.test_dir+"\\good-single-timestep.csv")
        finally:
            goldtext=fgold.read()
            writtentext=fwritten.read()
            fgold.close()
            fwritten.close()       
            os.chdir(savewd)     
            fdebug.write(writtentext)
            fdebug.close()
            self.maxDiff=None
            self.assertMultiLineEqual(goldtext,writtentext)
            os.chdir(savewd)     
            if fwritten is not None:
                fwritten.close()
                
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
        finally:
            goldtext=fgold.read()
            writtentext=fwritten.read()
            fgold.close()
            fwritten.close()       
            os.chdir(savewd)     
            fdebug.write(writtentext)
            fdebug.close()
            self.maxDiff=None
            self.assertMultiLineEqual(goldtext,writtentext)
            os.chdir(savewd)     
            if fwritten is not None:
                fwritten.close()
        
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
        finally:
            goldtext=fgold.read()
            writtentext=fwritten.read()
            fgold.close()
            fwritten.close()       
            os.chdir(savewd)     
            fdebug.write(writtentext)
            fdebug.close()
            self.maxDiff=None
            self.assertMultiLineEqual(goldtext,writtentext)
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
        finally:
            goldtext=fgold.read()
            writtentext=fwritten.read()
            fgold.close()
            fwritten.close()       
            os.chdir(savewd)     
            fdebug.write(writtentext)
            fdebug.close()
            self.maxDiff=None
            self.assertMultiLineEqual(goldtext,writtentext)
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
        finally:
            goldtext=fgold.read()
            writtentext=fwritten.read()
            fgold.close()
            fwritten.close()       
            os.chdir(savewd)     
            fdebug.write(writtentext)
            fdebug.close()
            self.maxDiff=None
            self.assertMultiLineEqual(goldtext,writtentext)
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
        finally:
            goldtext=fgold.read()
            writtentext=fwritten.read()
            fgold.close()
            fwritten.close()       
            os.chdir(savewd)     
            fdebug.write(writtentext)
            fdebug.close()
            self.maxDiff=None
            self.assertMultiLineEqual(goldtext,writtentext)
            os.chdir(savewd)     
            if fwritten is not None:
                fwritten.close()    
                
    #incorrect var desc
    def test_multiple_timestep_bad_var_desc(self):   
        badvar='"spf.sr [Shearr rate]"'
        expected = "Could not find data for variable {0}".format(re.sub('\"','',badvar))        
        output=popen(['tidysol', 'tidy', 'tests\\commands\\data\\good-single-timestep.txt','--cols={0}'.format(badvar)], stdout=PIPE).communicate()[0].decode("utf-8")
        assert(expected == output.rstrip())  
        
    #two time steps both times explicit, using LAST keyword  
    def test_multiple_timestep_both_times_last_keyword(self):   
        fgold = open("tests\\commands\\data\\goldfiles\\two_timestep_all_default.csv")     
        fdebug= open("tests\\debug-dump.txt","w")
        fwritten=None
        savewd = os.getcwd()
        shutil.copyfile('tests\\commands\\data\\good-two-timestep.txt',self.test_dir+"\\good-two-timestep.txt")
        os.chdir(self.test_dir)  
        try:
            popen(['tidysol', 'tidy', self.test_dir+"\\good-two-timestep.txt",'--times=0.1,LAST'], stdout=PIPE).communicate()[0].decode("utf-8")
            fwritten = open(self.test_dir+"\\good-two-timestep.csv") 
        finally:
            goldtext=fgold.read()
            writtentext=fwritten.read()
            fgold.close()
            fwritten.close()       
            os.chdir(savewd)     
            fdebug.write(writtentext)
            fdebug.close()
            self.maxDiff=None
            self.assertMultiLineEqual(goldtext,writtentext)
            os.chdir(savewd)     
            if fwritten is not None:
                fwritten.close()
    #two time steps default time,only inlcude shear rate var and reynolds #
    def test_multiple_timestep_two_var(self):   
        #TODO some odd gymnastics to handle test files and temp file writing. There's probably  a better way        
        fgold = open("tests\\commands\\data\\goldfiles\\two_timestep_two_var.csv")     
        fdebug= open("tests\\debug-dump.txt","w")
        fwritten=None
        savewd = os.getcwd()
        shutil.copyfile('tests\\commands\\data\\good-two-timestep.txt',self.test_dir+"\\good-two-timestep.txt")
        os.chdir(self.test_dir)  
        try:
            popen(['tidysol', 'tidy', self.test_dir+"\\good-two-timestep.txt",'--cols=spf2.sr,spf2.cellRe'], stdout=PIPE).communicate()[0].decode("utf-8")
            fwritten = open(self.test_dir+"\\good-two-timestep.csv") 
        finally:
            goldtext=fgold.read()
            writtentext=fwritten.read()
            fgold.close()
            fwritten.close()       
            os.chdir(savewd)     
            fdebug.write(writtentext)
            fdebug.close()
            self.maxDiff=None
            self.assertMultiLineEqual(goldtext,writtentext)
            os.chdir(savewd)     
            if fwritten is not None:
                fwritten.close()
    def test_multiple_timestep_two_var_wdesc(self):   
        #TODO some odd gymnastics to handle test files and temp file writing. There's probably  a better way        
        fgold = open("tests\\commands\\data\\goldfiles\\two_timestep_two_var.csv")     
        fdebug= open("tests\\debug-dump.txt","w")
        fwritten=None
        savewd = os.getcwd()
        shutil.copyfile('tests\\commands\\data\\good-two-timestep.txt',self.test_dir+"\\good-two-timestep.txt")
        os.chdir(self.test_dir)  
        try:
            popen(['tidysol', 'tidy', self.test_dir+"\\good-two-timestep.txt",'--cols="spf2.sr [Shear rate],spf2.cellRe [Cell Reynolds number]"'], stdout=PIPE).communicate()[0].decode("utf-8")       
            fwritten = open(self.test_dir+"\\good-two-timestep.csv") 
        finally:
            goldtext=fgold.read()
            writtentext=fwritten.read()
            fgold.close()
            fwritten.close()       
            os.chdir(savewd)     
            fdebug.write(writtentext)
            fdebug.close()
            self.maxDiff=None
            self.assertMultiLineEqual(goldtext,writtentext)
            os.chdir(savewd)     
            if fwritten is not None:
                fwritten.close()
    #two times steps only include sr,cellRe and Date meta
    def test_multiple_timestep_two_var_one_meta(self):   
        #TODO some odd gymnastics to handle test files and temp file writing. There's probably  a better way        
        fgold = open("tests\\commands\\data\\goldfiles\\two_timestep_two_var_one_meta.csv")     
        fdebug= open("tests\\debug-dump.txt","w")
        fwritten=None
        savewd = os.getcwd()
        shutil.copyfile('tests\\commands\\data\\good-two-timestep.txt',self.test_dir+"\\good-two-timestep.txt")
        os.chdir(self.test_dir)  
        try:
            popen(['tidysol', 'tidy', self.test_dir+"\\good-two-timestep.txt",'--cols=spf2.sr,spf2.cellRe,Date'], stdout=PIPE).communicate()[0].decode("utf-8")
            fwritten = open(self.test_dir+"\\good-two-timestep.csv") 
        finally:
            goldtext=fgold.read()
            writtentext=fwritten.read()
            fgold.close()
            fwritten.close()       
            os.chdir(savewd)     
            fdebug.write(writtentext)
            fdebug.close()
            self.maxDiff=None
            self.assertMultiLineEqual(goldtext,writtentext)
            os.chdir(savewd)     
            if fwritten is not None:
                fwritten.close()
        
    #two time steps LAST keyword ,defualt vars, output to non-default file & directory
    def test_multiple_timestep_specify_filename(self):   
        #TODO some odd gymnastics to handle test files and temp file writing. There's probably  a better way        
        fgold = open("tests\\commands\\data\\goldfiles\\two_timestep_all_default.csv")     
        fdebug= open("tests\\debug-dump.txt","w")
        fwritten=None
        savewd = os.getcwd()
        shutil.copyfile('tests\\commands\\data\\good-two-timestep.txt',self.test_dir+"\\good-two-timestep.txt")
        os.chdir(self.test_dir)  
        try:
            popen(['tidysol', 'tidy', self.test_dir+"\\good-two-timestep.txt",'--output=newname.csv'], stdout=PIPE).communicate()[0].decode("utf-8")
            fwritten = open(self.test_dir+"\\newname.csv") 
        finally:
            goldtext=fgold.read()
            writtentext=fwritten.read()
            fgold.close()
            fwritten.close()       
            os.chdir(savewd)     
            fdebug.write(writtentext)
            fdebug.close()
            self.maxDiff=None
            self.assertMultiLineEqual(goldtext,writtentext)
            os.chdir(savewd)     
            if fwritten is not None:
                fwritten.close()
                
    #output dir does not exist
    def test_multiple_timestep_specify_filename_w_newdir(self):   
        #TODO some odd gymnastics to handle test files and temp file writing. There's probably  a better way        
        fgold = open("tests\\commands\\data\\goldfiles\\two_timestep_all_default.csv")     
        fdebug= open("tests\\debug-dump.txt","w")
        fwritten=None
        savewd = os.getcwd()
        shutil.copyfile('tests\\commands\\data\\good-two-timestep.txt',self.test_dir+"\\good-two-timestep.txt")
        os.chdir(self.test_dir)  
        try:
            popen(['tidysol', 'tidy', self.test_dir+"\\good-two-timestep.txt",'--output=newdir\\newname.csv'], stdout=PIPE).communicate()[0].decode("utf-8")
            fwritten = open(self.test_dir+"\\newdir\\newname.csv") 
        finally:
            goldtext=fgold.read()
            writtentext=fwritten.read()
            fgold.close()
            fwritten.close()       
            os.chdir(savewd)     
            fdebug.write(writtentext)
            fdebug.close()
            self.maxDiff=None
            self.assertMultiLineEqual(goldtext,writtentext)
            os.chdir(savewd)     
            if fwritten is not None:
                fwritten.close()
    
    #specify times vars and output
    def test_multiple_timestep_all_args(self):   
        #TODO some odd gymnastics to handle test files and temp file writing. There's probably  a better way        
        fgold = open("tests\\commands\\data\\goldfiles\\two_timestep_all_args.csv")     
        fdebug= open("tests\\debug-dump.txt","w")
        fwritten=None
        savewd = os.getcwd()
        shutil.copyfile('tests\\commands\\data\\good-two-timestep.txt',self.test_dir+"\\good-two-timestep.txt")
        os.chdir(self.test_dir)  
        try:
            popen(['tidysol', 'tidy', self.test_dir+"\\good-two-timestep.txt",'--times=LAST','--cols=spf2.cellRe', '--output=newdir\\newname.csv'], stdout=PIPE).communicate()[0].decode("utf-8")
            fwritten = open(self.test_dir+"\\newdir\\newname.csv") 

        finally:
            goldtext=fgold.read()
            writtentext=fwritten.read()
            fgold.close()
            fwritten.close()       
            os.chdir(savewd)     
            fdebug.write(writtentext)
            fdebug.close()
            self.maxDiff=None
            self.assertMultiLineEqual(goldtext,writtentext)
            os.chdir(savewd)     
            if fwritten is not None:
                fwritten.close()   
                
    #test for duplicate specfied timesteps
    def test_multiple_timestep_first_timestep_repeated(self):   
        #TODO some odd gymnastics to handle test files and temp file writing. There's probably  a better way        
        fgold = open("tests\\commands\\data\\goldfiles\\two_timestep_first_only.csv")     
        fdebug= open("tests\\debug-dump.txt","w")
        fwritten=None
        savewd = os.getcwd()
        shutil.copyfile('tests\\commands\\data\\good-two-timestep.txt',self.test_dir+"\\good-two-timestep.txt")
        os.chdir(self.test_dir)  
        try:
            popen(['tidysol', 'tidy', self.test_dir+"\\good-two-timestep.txt",'--times=0.1,0.1'], stdout=PIPE).communicate()[0].decode("utf-8")
            fwritten = open(self.test_dir+"\\good-two-timestep.csv")  
        finally:
            goldtext=fgold.read()
            writtentext=fwritten.read()
            fgold.close()
            fwritten.close()       
            os.chdir(savewd)     
            fdebug.write(writtentext)
            fdebug.close()
            self.maxDiff=None
            self.assertMultiLineEqual(goldtext,writtentext)
            os.chdir(savewd)     
            if fwritten is not None:
                fwritten.close()
    
    #test for duplicate specified vars
                
    #what about handling a large file?  