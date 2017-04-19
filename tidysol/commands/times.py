"""The times command."""

from .base import Base
import re
   
class Times(Base):
    """List the timesteps for which data are recorded"""


    def run(self):
        error_to_catch = getattr(__builtins__,'FileNotFoundError', IOError)
        try:
            #TODO this is an ad-hoc parse built up from unit tests could refactor it to definitely its own class probably make it as a better parser too.
        
            #find one and only one line defining variable names
            varsLine=0
            linecount = 0
            foundVars = None
            numExpressions=-1
            numDimensions=-1
            numNodesMeta=-1
            dimVars = None
            nodeCount=0
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

            if(numExpressions == -1):
                raise Exception("Could not find an % Expressions line")
            if(numDimensions == -1):
                raise Exception("Could not find a % Dimensions line")
            if(numNodesMeta == -1):
                raise Exception("Could not find a % Nodes line")            
            
            if(int(numNodesMeta) != nodeCount):
                raise Exception('Expected {0} nodes but read {1}'.format(numNodesMeta,nodeCount))

            #examine the variable names found                
            if foundVars:
                expected=int(numExpressions)+int(numDimensions)
                if len(foundVars)+len(dimVars) != numExpressions+numDimensions:
                    raise Exception('Expected {0} variables ({1} dimensions and {2} epressions) but found {3} ({4} dimensions and {5} expressions)'.format(expected,numDimensions,numExpressions,len(foundVars)+len(dimVars),len(dimVars),len(foundVars)))               
            else:
                raise Exception("Could not find a line defining variables") 

                
        except error_to_catch:
              print("Could not find file: "+self.options["<name>"])
        except Exception as e: #TODO may want to spend time making a custom exception class work
            print(e)
