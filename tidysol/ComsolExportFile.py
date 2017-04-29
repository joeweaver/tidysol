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
                #TODO this repetivie code can be handled better now that we're matching all meta
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
        
    def to_csv(self,timesToWrite=[],specifiedCols=[]):       
        metakeys=[]
        metaToWrite=[]
        #default, write all timesteps
        if not timesToWrite:
            timesToWrite=self.timesteps
        else:
            for i in range(0,len(timesToWrite)):
                if timesToWrite[i].casefold()=="last".casefold():
                    timesToWrite[i]=max(self.timesteps)
  
        #enforce unique
        timesToWrite=list(set(timesToWrite))  
        #if(len(timesToWrite)==1) and (timesToWrite[0].casefold()=="last".casefold()):
        #    timesToWrite[0]=max(self.timesteps)

        for m in sorted(self.metaData.keys()):
            #by default, do not include metadata now made redundant. Particularly the variable description list
            if not specifiedCols:            
                if(m not in ['Expressions','Dimension','Nodes','Description']):
                    metakeys.append("{0} []".format(m))
                    metaToWrite.append(re.sub('\s*,\s*',' - ',self.metaData[m]))
            else:
                if(m.strip() in specifiedCols):
                    metakeys.append("{0} []".format(m))
                    metaToWrite.append(re.sub('\s*,\s*',' - ',self.metaData[m])) 

        headerline=""        
        if not specifiedCols:        
            headers=["t []"]+self.vars_w_descs()+metakeys
            headerline=",".join(str(h) for h in headers)
        else:
            headers=["t []"]+self.vars_w_descs()[0:len(self.dimVars)]
            for v in self.vars_w_descs():
                vardesc =re.match('\s*([^\[]*)(\s*\[(.*)\])*',v)
                if vardesc:
                    vname=vardesc.group(1)
                    vdesc=vardesc.group(3)
                    for sc in specifiedCols:
                        scmatch=re.match('\s*([^\[]*)(\s*\[(.*)\])*',sc)
                        scname=scmatch.group(1)
                        scdesc=scmatch.group(3)
                        matchDesc = (not scdesc) or (not vdesc) or (scdesc.strip() == vdesc.strip())
                        matchName=vname.strip()==scname.strip()
                        if matchName and matchDesc:
                            headers.append(v)
            headers=headers+metakeys
            headerline=",".join(str(h) for h in headers)  
        output=headerline

        for ts in self.timesteps:
            #could probably get clever with itertools here
            colsToWrite=[]
            for c in range(0,len(self.dimVars)):
                colsToWrite.append(c+1)
            col=len(self.dimVars)+1
            #having string/float issues all over depending on how stuff
            #arrives here. Arbitralily casting evering to float at this chokepoint
            if(float(ts) in [float(i) for i in timesToWrite]):
                for (varn,units,timestep) in self.foundVars:                    
                    if(str(ts) == str(timestep)):
                        if(not specifiedCols):
                            colsToWrite.append(col)
                        else:                     
                            #TODO refactor. This is repeate code from above and messy
                            for sc in specifiedCols:
                                scmatch=re.match('\s*([^\[]*)(\s*\[(.*)\])*',sc)
                                scname=scmatch.group(1)
                                matchName=varn.strip()==scname.strip()
                                if matchName:
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
        