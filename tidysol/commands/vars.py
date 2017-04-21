"""The vars command."""

from .base import Base
from .. import ComsolExportFile
from ..Exceptions import TidysolException


class Vars(Base):
    """List the variables (with descriptions, and including metadata) for which data are recorded"""
    
    def run(self):
        try:
            c=ComsolExportFile(self.options["<name>"])    
            print(", ".join(str(step) for step in c.timesteps))
        
        #not much to do with unexpected exceptions other than print them out
        except Exception as e: 
            print(e)
            
        except TidysolException as e:
            print(e)