"""The tidy command."""

from .base import Base
from .. import ComsolExportFile
from ..Exceptions import TidysolException


class Tidy(Base):
    """Create a tidy version of the data in the Comsol export"""
    
    def run(self):
        try:
            print(self.options)
            c=ComsolExportFile(self.options["<name>"])    

        #not much to do with unexpected exceptions other than print them out
        except Exception as e: 
            print(e)
            
        except TidysolException as e:
            print(e)