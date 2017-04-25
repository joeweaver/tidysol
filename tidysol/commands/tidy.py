"""The tidy command."""

from .base import Base
from .. import ComsolExportFile
from ..Exceptions import TidysolException
import re

class Tidy(Base):
    """Create a tidy version of the data in the Comsol export"""
    
    def run(self):
        try:
            c=ComsolExportFile(self.options["<name>"])    
            for t in self.options["--times"]:
                if not re.match('^\d*\.?\d$',t):
                   raise (TidysolException("{0} is not a valid timestep. Only digits and a single decimal point allowed".format(t))) 
                if t not in c.timesteps:
                    raise TidysolException("Could not find data for time {0}".format(t))
                    
        #not much to do with unexpected exceptions other than print them out
        except Exception as e: 
            print(e)
            
        except TidysolException as e:
            print(e)