"""The times command."""


from json import dumps

from .base import Base
import re
   
class Times(Base):
    """List the timesteps for which data are recorded"""


    def run(self):
        error_to_catch = getattr(__builtins__,'FileNotFoundError', IOError)
        try:
            varsLine=0
            linecount = 0
            for line in open(self.options["<name>"],"r"):
                linecount=linecount + 1
                if re.search('^%',line):
                    match = re.search('([\w|\.]+)\s*(\([^\)]+\))\s*\@\s*t=(\d\.*\d*)\s*',line)
                    if match:
                        if(varsLine==0):
                            varsLine=linecount
                        else:
                            raise Exception("Found more than one line naming variables: "+str(varsLine) + " & " + str(linecount))
            if varsLine != 1:
                raise Exception("Could not find a line defining variables")                    
                
        except error_to_catch:
              print("Could not find file: "+self.options["<name>"])
        except Exception as e: #TODO may want to spend time making a custom exception class work
            print(e)
