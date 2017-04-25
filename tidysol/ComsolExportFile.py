"""Reads the actual comsol export file"""

from tidysol.Exceptions import TidysolException
import re
import csv
import collections

class ComsolExportFile(object):
    """An exported comsol file reader."""
    
    def __init__(self, filename):
        self.filename=filename
        self.timesteps=set() 
        self.columnVars=collections.OrderedDict()
        self.metaData=dict()
        self.dimVars=[]
        self.error_to_catch = getattr(__builtins__,'FileNotFoundError', IOError)
        self.foundVars=None
        #TODO this is an ad-hoc parse built up from unit tests and miht benefit from refactoring
        try:
            NOT_MATCHED=-1
            linecount = 0
            varsLine=NOT_MATCHED
            numExpressions=NOT_MATCHED
            numDimensions=NOT_MATCHED
            numNodesMeta=NOT_MATCHED
            numDesc=NOT_MATCHED
            nodeCount=0
            varDescs=[]
            for line in open(self.filename,"r"):
                linecount=linecount + 1
                matchComment= re.search('^%',line)
                if matchComment:
                    varReg='([\w|\.]+)\s*(\(*\S*\)*)\s*\@\s*t=(\d\.*\d*)\s*'
                    matchVar = re.findall(varReg,line) #using findall for easy len
                    if matchVar:
                        if(self.foundVars):
                            raise TidysolException("Found more than one line naming variables: "+str(varsLine) + " & " + str(linecount))
                        else:
                            varsLine=linecount
                            self.foundVars=matchVar
                            foundAt = re.search(varReg,line)
                            possibleDims=line[1:foundAt.start()-1]
                            self.dimVars = possibleDims.split()
                    else:
                        matchMeta=re.search('^%\s*([^\:]*):\s*(.*)',line)
                        if matchMeta:
                            self.metaData[matchMeta.group(1)]=matchMeta.group(2)
                else:
                    nodeCount=nodeCount+1
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
                        for r in row:
                            varDescs.append(re.sub('\s*,\s*',' - ',r.strip()))    
            if(numExpressions == NOT_MATCHED):
                raise TidysolException("Could not find an % Expressions line")
            if(numDimensions == NOT_MATCHED):
                raise TidysolException("Could not find a % Dimensions line")
            if(numNodesMeta == NOT_MATCHED):
                raise TidysolException("Could not find a % Nodes line")  
            if(numDesc==NOT_MATCHED):
                raise TidysolException("Could not find a % Description line")
                
            if(int(numNodesMeta) != nodeCount):
                raise TidysolException('Expected {0} nodes but read {1}'.format(numNodesMeta,nodeCount))
             
            
            if self.foundVars:
                expected=int(numExpressions)+int(numDimensions)
                if len(self.foundVars)+len(self.dimVars) == expected:
                    varnum=0
                    #if performance is an issue, we could get more clever about this    
                    for d in self.dimVars:
                        self.columnVars[d]=""
                    for (varn,units,timestep) in self.foundVars:
                       self.timesteps.add(float(timestep))

                       #slightly hacky - there is a varn for each repeated timestep. Once we get to the end of the descriptions, we're looping around, so exit the iteration
                       #there's a few hole in it, but the internal consistency checks should catch them first (famous last words)                    
                       if varnum<(numDesc):
                           self.columnVars[varn]="{0}".format(varDescs[varnum])     
                       varnum=varnum+1          
                else:
                    raise TidysolException('Expected {0} variables ({1} dimensions and {2} expressions) but found {3} ({4} dimensions and {5} expressions)'.format(expected,numDimensions,numExpressions,len(self.foundVars)+len(self.dimVars),len(self.dimVars),len(self.foundVars)))               
            else:
                raise TidysolException("Could not find a line defining variables") 
                
            expectedDesc=int(numExpressions)/len(self.timesteps)
            if(expectedDesc!=numDesc):
                raise TidysolException('Expected {0} descriptions of variables but read {1}'.format(int(expectedDesc),numDesc))
       
        except self.error_to_catch:
            raise(TidysolException("Could not find file: "+self.filename))
    def vars_w_descs(self):
        var_descs=[]   
        for v in self.columnVars:
            var_descs.append("{0} [{1}]".format(v,self.columnVars[v]))
        return(var_descs)
        
    def to_csv(self):
        metakeys=[]
        metaToWrite=[]
        #default, write all timesteps
        timesToWrite=self.timesteps
        
        for m in sorted(self.metaData.keys()):
            #by default, do not include metadata now made redundant. Particularly the variable description list
            if(m not in ['Expressions','Dimension','Nodes','Description']):
                metakeys.append("{0} []".format(m))
                metaToWrite.append(re.sub('\s*,\s*',' - ',self.metaData[m]))

        headers=["t []"]+self.vars_w_descs()+metakeys
        headerline=",".join(str(h) for h in headers)
        
        output=headerline
        #could probably get clever with itertools here
        colsToWrite=[]
        for c in range(0,len(self.dimVars)):
            colsToWrite.append(c+1)
            
        col=len(self.dimVars)+1

        for ts in self.timesteps:
            if(ts in timesToWrite):
                for (varn,units,timestep) in self.foundVars:
                    if(str(ts) == str(timestep)):
                        colsToWrite.append(col)
                        col=col+1
        
                try:
                    for line in open(self.filename,"r"):
                        matchComment= re.search('^%',line)
                        if not matchComment:
                            cols=re.split('\s\s+',line.strip())
                            writeMe=[ts]
                            for i in colsToWrite:
                                writeMe.append(cols[i-1])
                            writeMe=writeMe+metaToWrite
                            output=output+"\n"+",".join(str(c) for c in writeMe)
                except self.error_to_catch:
                    raise(TidysolException("Could not find file: "+self.filename))
             
        return (output+"\n")
        