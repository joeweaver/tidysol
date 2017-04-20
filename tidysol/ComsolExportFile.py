"""Reads the actual comsol export file"""

from tidysol.Exceptions import TidysolException
    
class ComsolExportFile(object):
    """An exported comsol file reader."""
    
    def __init__(self, filename):
        self.filename=filename

        error_to_catch = getattr(__builtins__,'FileNotFoundError', IOError)
        
        linecount = 0
        try:
            for line in open(self.filename,"r"):
                linecount=linecount + 1
        except error_to_catch:
            raise(TidysolException("Could not find file: "+self.filename))