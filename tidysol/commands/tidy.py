"""The tidy command."""

from .base import Base
from .. import ComsolExportFile
from ..Exceptions import TidysolException
import re
import os

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
            base = os.path.basename(self.options["<name>"])
            fname = os.path.splitext(base)[0]
            o = open("{0}.csv".format(fname),"w")
            o.write(c.to_csv())
            o.close()
        #not much to do with unexpected exceptions other than print them out
        except Exception as e: 
            print(e)
            
        except TidysolException as e:
            print(e)