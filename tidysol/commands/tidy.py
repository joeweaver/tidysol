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
            writeTimes=[]
            writeCols=[]
            if(self.options["--times"]):
                writeTimes = re.split(",",self.options["--times"][0])

            for t in writeTimes:
                if t.casefold()!="last".casefold():                   
                    if (not re.match('^\d*\.?\d$',t)):
                           raise (TidysolException("{0} is not a valid timestep".format(t))) 
                    if float(t) not in c.timesteps:
                        raise TidysolException("Could not find data for time {0}".format(t))
            
            if(self.options["--cols"]):
                writeCols=re.split(",",re.sub('\"','',self.options["--cols"][0]))

            for col in writeCols:
                if c.columnVars.get(col) == None and c.metaData.get(col)==None:
                    if not col in c.vars_w_descs():
                        raise TidysolException("Could not find data for variable {0}".format(col))
            #ensure unique cols
            writeCols=list(set(writeCols))
            
            base = os.path.basename(self.options["<name>"])
            fname = os.path.splitext(base)[0]
            o=None
            if not(self.options["--output"]):
                o = open("{0}.csv".format(fname),"w")
            else:
                outfilename=self.options["--output"]
                if os.path.dirname(outfilename) :
                    os.makedirs(os.path.dirname(outfilename), exist_ok=True)
                o=open(outfilename,"w")
            try:
                o.write(c.to_csv(writeTimes,writeCols))
            finally:
                o.close()
        #not much to do with unexpected exceptions other than print them out
        except Exception as e: 
            print(e)
            
        except TidysolException as e:
            print(e)