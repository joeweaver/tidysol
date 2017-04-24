"""The meta command."""

from .base import Base
from .. import ComsolExportFile
from ..Exceptions import TidysolException


class Meta(Base):
    """List the metadata in the header"""
    
    def run(self):
        try:
            c=ComsolExportFile(self.options["<name>"])    
            if(self.options['--values']):        
                print(c.metaData)
            else:
                print(", ".join(str(meta) for meta in sorted(c.metaData.keys())))
            #print(self.options)
        #not much to do with unexpected exceptions other than print them out
        except Exception as e: 
            print(e)
            
        except TidysolException as e:
            print(e)