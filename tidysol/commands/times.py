"""The times command."""

from .base import Base
from .. import ComsolExportFile
from ..Exceptions import TidysolException
    
import re
import csv 

class Times(Base):
    """List the timesteps for which data are recorded"""


    def run(self):
        try:
            NOT_MATCHED=-1
            #TODO this is an ad-hoc parse built up from unit tests could refactor it to definitely its own class probably make it as a better parser too.
        
            #find one and only one line defining variable names
            varsLine=0
            linecount = 0
            foundVars = None
            numExpressions=NOT_MATCHED
            numDimensions=NOT_MATCHED
            numNodesMeta=NOT_MATCHED
            dimVars = None
            nodeCount=0
            descriptions=None
            numDesc=NOT_MATCHED
            c=ComsolExportFile(self.options["<name>"])
            for line in open(self.options["<name>"],"r"):
                linecount=linecount + 1
                matchHead= re.search('^%',line)
                if matchHead:
                    varReg='([\w|\.]+)\s*(\(*\S*\)*)\s*\@\s*t=(\d\.*\d*)\s*'
                    matchVar = re.findall(varReg,line) #using findall for easy len
                    if matchVar:
                        if(foundVars):
                            raise Exception("Found more than one line naming variables: "+str(varsLine) + " & " + str(linecount))
                        else:
                            varsLine=linecount
                            foundVars=matchVar
                            foundAt = re.search(varReg,line)
                            possibleDims=line[1:foundAt.start()-1]
                            dimVars = possibleDims.split()
                else:
                    nodeCount=nodeCount+1
                #TODO this will become a generic match headers at some point
                matchExpressionCount = re.search('^% Expressions:\s+(\d+)',line)
                if matchExpressionCount:
                    numExpressions = matchExpressionCount.group(1)
                matchDimensions=re.search('^% Dimension:\s+(\d+)',line)
                if matchDimensions:                
                    numDimensions = matchDimensions.group(1)
                matchNodesMeta=re.search('^% Nodes:\s+(\d+)',line)
                if matchNodesMeta:                
                    numNodesMeta = matchNodesMeta.group(1)
                matchDescriptions=re.search('^% Description:\s+(.+)',line)
                if matchDescriptions:
                    rawDesc=matchDescriptions.group(1)
                    #have to quote things like 'Velocity, z component'
                    quotedDesc=re.sub('([^,]*,\s+\S+\s+component[^,]*)', lambda x: "\"{0}\"".format(x.group(1)),rawDesc)
                    #letting the csv package deal with splitting by only unenclosed commas
                    descriptions = csv.reader([quotedDesc], delimiter=',') 
                    for row in descriptions: 
                        numDesc=len(row)
            if(numExpressions == NOT_MATCHED):
                raise Exception("Could not find an % Expressions line")
            if(numDimensions == NOT_MATCHED):
                raise Exception("Could not find a % Dimensions line")
            if(numNodesMeta == NOT_MATCHED):
                raise Exception("Could not find a % Nodes line")  
            if(numDesc==NOT_MATCHED):
                raise Exception("Could not find a % Description line")
            
            if(int(numNodesMeta) != nodeCount):
                raise Exception('Expected {0} nodes but read {1}'.format(numNodesMeta,nodeCount))

            #examine the variable names found      
            timesteps=set()           
            if foundVars:
                expected=int(numExpressions)+int(numDimensions)
                if len(foundVars)+len(dimVars) == expected:
                    #if performance is an issue, we could get more clever about this                    
                    for (varn,units,timestep) in foundVars:
                        timesteps.add(float(timestep))
                else:
                    raise Exception('Expected {0} variables ({1} dimensions and {2} expressions) but found {3} ({4} dimensions and {5} expressions)'.format(expected,numDimensions,numExpressions,len(foundVars)+len(dimVars),len(dimVars),len(foundVars)))               
            else:
                raise Exception("Could not find a line defining variables") 
            
            expectedDesc=int(numExpressions)/len(timesteps)
            if(expectedDesc!=numDesc):
                raise Exception('Expected {0} descriptions of variables but read {1}'.format(int(expectedDesc),numDesc))
            print(", ".join(str(step) for step in timesteps))
        
        except Exception as e: #TODO may want to spend time making a custom exception class work
            print(e)
        except TidysolException as e:
            print(e)
