"""Tests for our `tidysol tidy subcommand."""


from subprocess import PIPE, Popen as popen
from unittest import TestCase


class TestMeta(TestCase):
            
    #time not found
    def test_single_timestep_with_descriptions(self):
        time=12.3        
        expected = "Could not find data for time {0}".format(time)
        output = popen(['tidysol', 'tidy', 'tests\\commands\\data\\good-single-timestep.txt','--times={0}'.format(time)], stdout=PIPE,bufsize=16384).communicate()[0].decode("utf-8")
        assert(expected == output.rstrip())        
        
    #time is not correct format LAST or [\d|\.]+
    #base case for single time step, default time,defualt vars, output to terminal
        
    #two time steps default time,defualt vars, output to terminal
        
    #two time steps only first time,defualt vars, output to terminal
    
    #two time steps LAST kewword time,defualt vars, output to terminal
    
    #two time steps both times explicit kewword time,incorrect var name, output to terminal  
      
    #two time steps default time,do not inlcude pressure var, output to terminal 
        
    #two time steps default time,do not inlcude dat metadatar, output to terminal      
        
    #two time steps LAST kewword time,defualt vars, output to file
    