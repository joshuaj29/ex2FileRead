"""
Created on Thur March 16, 2023

@author: JoshuaJ
"""


import re
import sys
import copy
import pandas as pd
import matplotlib.pyplot as plt
import time


#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s -  %(levelname)s -  %(message)s')




class ReTools:
    '''
    Covers tool definitions 
    if TXX starts a line, then looks for tool parameters defined thereafter.
    Group 1 is Tool, group 2 is diameter, group 3 is feed down, group 4
    is spindle speed, group 5 is feed up, group 6 is hit count, group 7 is z offset,
    group 8 is slot designation
    '''
    def __init__(self, line):
        self.toolHeadRe = re.compile('^(?:(T\d+)|(C(?:\d|)\.\d+|\d\.\d+)|(F\d+)|(S\d+(?:\.?))|(B\d+)|(H\d+)|(Z(?:-|)\d?(?:\.|)\d+)|(w\d)){1,8}').search(line)
        
        
    def tGroups(self):
        self.toolGroups = self.toolHeadRe.groups()
        return self.toolGroups

    def toolPresent(self):
        if self.toolHeadRe == None:
            return False
        else:
            return True
    
    def toolNum(self):
        '''Returns the tool number in string TXX'''
        return self.tGroups()[0]
    
    def toolDiam(self):
        '''Returns the tool diameter in string CX.XXXX'''
        return self.tGroups()[1]
    
    def toolFeedDown(self):
        '''Returns the feed down in string FXXX'''
        return self.tGroups()[2]
    
    def toolSpeed(self):
        '''Returns the spindle speed in string SXX'''
        return self.tGroups()[3]
    
    def toolUpFeed(self):
        '''Returns the up feed in string FXX'''
        return self.tGroups()[4]
    
    def toolHitCount(self):
        '''Returns the hit count in string HXXX'''
        return self.tGroups()[5]
    
    def toolZOff(self):
        '''Returns the z offset in string ZX.XXXX or Z-X.XXXX'''
        return self.tGroups()[6]
    
    def toolSlot(self):
        '''Returns the slot designation in string XX. example w1'''
        return self.tGroups()[7]





class ReXY:
    '''Covers X and Y coordinates in the body
    Group 1 is X, group 2 is Y'''
    def __init__(self, line):
        self.XY_val_re = re.compile('^(?:(X(?:-|)\d+)|(Y(?:-|)\d+)){1,2}$').search(line)
        
    def xyGroups(self):    
        return self.XY_val_re.groups()

    def xyPresent(self):
        if self.XY_val_re == None:
            return False
        else:
            return True

    def reX(self):
        return self.xyGroups()[0]
    
    def reY(self):
        return self.xyGroups()[1]





class ReSNR:
    '''Covers all step and repeat commands and coordinates
    If M02 starts the line, group 1 is X, group 2 is Y,
    group 3 is M70, group 4 is M80, group 5 is M90'''
    def __init__(self, line):
        self.XY_snr_re = re.compile('^M02(?:(X(?:-|)\d+)|(Y(?:-|)\d+)){1,2}(?:(M70)|(M80)|(M90)?){1,2}').search(line)
        
        
    def snrGroups(self):    
        return self.XY_snr_re.groups()
        

    def snrPresent(self):
        if self.XY_snr_re == None:
            return False
        else:
            return True
        
    def M70Present(self):
        if self.snrGroups()[2] != None:
            return True
        else:
            return False
        
    def M80Present(self):
        if self.snrGroups()[3] != None:
            return True
        else:
            return False
        
    def M90Present(self):
        if self.snrGroups()[4] != None:
            return True
        else:
            return False
        
    def M70M80Present(self):
        sG = self.snrGroups()
        if (sG[2] != None) and (sG[3] != None):
            return True
        else:
            return False
        
    def M70M90Present(self):
        sG = self.snrGroups()
        if (sG[2] != None) and (sG[4] != None):
            return True
        else:
            return False
        
    def M80M90Present(self):
        sG = self.snrGroups()
        if (sG[3] != None) and (sG[4] != None):
            return True
        else:
            return False
        
    def M02Present(self):
        sG = self.snrGroups()
        if (sG[2] == None) and (sG[3] == None) and (sG[4] == None):
            return True
        else:
            return False
        
        
    def reM02(self):
        '''line is only M02XXYY. No other step and repeat commands'''
        x = ex2DecConvert(self.snrGroups()[0])
        y = ex2DecConvert(self.snrGroups()[1])
        return x, y


    def reM70(self):
        '''step and repeat line contains only a M70 command'''
        x = self.snrGroups()[0]
        y = self.snrGroups()[1]
        return x, y


    def reM80(self):
        '''step and repeat line contains only a M80 command'''
        x = self.snrGroups()[0]
        y = self.snrGroups()[1]
        return x, y


    def reM90(self):
        '''step and repeat line contains only a M90 command'''
        x = self.snrGroups()[0]
        y = self.snrGroups()[1]
        return x, y


    def reM70M80(self):
        '''step and repeat line contains only a M70M80 command'''
        x = self.snrGroups()[0]
        y = self.snrGroups()[1]
        return x, y


    def reM70M90(self):
        '''step and repeat line contains only a M70M90 command'''
        x = self.snrGroups()[0]
        y = self.snrGroups()[1]
        return x, y


    def reM80M90(self):
        '''step and repeat line contains only a M80M90 command'''
        x = self.snrGroups()[0]
        y = self.snrGroups()[1]
        return x, y




class ReM25:
    '''Covers M25 lines - start of a step and repeat block'''
    def __init__(self, line):
        self.M25_re = re.compile('^M25$').search(line)

    def m25Present(self):
        if self.M25_re == None:
            return False
        else:
            return True
        
    def m25Group(self):
        return self.M25_re.group()



def reM01(line):
    '''Covers M01 lines - end of a step and repeat coordinate block
    start of step and repeat commands'''
    M01_re = re.compile('^M01$')
    return M01_re.search(line).group()



def reCamera(line):
    pass


def ex2DecConvert(coord):
    if coord[1] == '-':
        numCoord = float('-' + coord[2:4] + '.' + coord[4:])
    else:
        numCoord = float(coord[1:3] + '.' + coord[3:])
    return numCoord





class StepAndRepeat:
    def __init__(self, pivot, original, writeTo, m02OffsetX, m02OffsetY, xIndex, yIndex, modifierX=2, modifierY=2):
        self.lastOffset = {'X': [], 'Y': []}
        self.pivot = pivot
        self.original = original
        self.writeTo = writeTo
        self.m02OffsetX = m02OffsetX
        self.m02OffsetY = m02OffsetY
        self.xIndex = xIndex
        self.yIndex = yIndex
        self.modifierX = modifierX
        self.modifierY = modifierY
        
        
        self.newCoordinates('X', m02OffsetX, xIndex, modifierX)
        self.newCoordinates('Y', m02OffsetY, yIndex, modifierY)
        
        
        self.writeTo['X'].extend(self.pivot['X'])
        self.writeTo['Y'].extend(self.pivot['Y'])
        self.writeTo['T'].extend(self.original['T'])
    
        
    def newCoordinates(self, axis, m02Off, cIndex, modifier):
        for value in self.pivot[axis]:
            newValue = m02Off + value - (self.original[axis][cIndex]*modifier)
            self.pivot[axis][cIndex] = newValue
            self.lastOffset[axis].append(value + m02Off)
            cIndex += 1

        
    def addingOn(self):
        return copy.deepcopy(self.lastOffset)     # pivot dict
    
    
    
    
    
# swap last step x and y coordinates (even if M02), then add M02 offset
def m70(pivot, original, m02OffX, m02OffY, modX=2, modY=2):
    pivot70 = {'X': copy.deepcopy(pivot['Y']), 'Y': copy.deepcopy(pivot['X'])}
    offsetX = m02OffX
    offsetY = m02OffY
    i = 0
    for value in pivot70['X']:
        pivot['X'][i] = value + offsetX - (original['Y'][i]*modY)
        i+=1
    j = 0
    for value in pivot70['Y']:
        pivot['Y'][j] = value + offsetY - (original['X'][j]*modX)
        j+=1
    return copy.deepcopy(pivot)





def main():

    st = time.time()
    
    
    try:
        with open(r'path to file', 'r') as file:
            fileContent = file.readlines()
            
    except:
        print('File not Found')
        sys.exit()
        
    else:
        currentT = ''
        currentX = 0
        currentY = 0
        tools = {}
        toolDiameters = []
        allCoords = {'X': [], 'Y': [], 'T': []}
        snrCount = 0
        
        # can delete these, using so errors do not show in IDE
        pivotSNR = ''
        originalSNR = ''
        currentSNR = ''
    
        for line in fileContent:
            rt = ReTools(line)
            snr = ReSNR(line)
            xy = ReXY(line)
            m25 = ReM25(line)
    
    
            if xy.xyPresent() == True:
                if xy.reX() != None:
                    currentX = ex2DecConvert(xy.reX())
                if xy.reY() != None:
                    currentY = ex2DecConvert(xy.reY())
                currentSNR['X'].append(currentX)
                currentSNR['Y'].append(currentY)
                currentSNR['T'].append(currentT)
                
    
    
            elif snr.snrPresent() == True:
                snrCount += 1
                snrOffsetX, snrOffsetY = snr.reM02()
                xCount = 0
                yCount = 0
                
                if snr.M02Present():
                    stepandrepeat = StepAndRepeat(pivotSNR, originalSNR, allCoords, snrOffsetX, snrOffsetY, xCount, yCount, modifierX=0, modifierY=0)
                    pivotSNR = stepandrepeat.addingOn()
                    
                    
                elif snr.M70M80Present():
                    pivotSNR = m70(pivotSNR, originalSNR, snrOffsetX, snrOffsetY, modX=2, modY=0)
                    allCoords['X'].extend(pivotSNR['X'])
                    allCoords['Y'].extend(pivotSNR['Y'])
                    allCoords['T'].extend(originalSNR['T'])
                    
                    
                elif snr.M70M90Present():
                    pivotSNR = m70(pivotSNR, originalSNR, snrOffsetX, snrOffsetY, modX=0, modY=2)
                    allCoords['X'].extend(pivotSNR['X'])
                    allCoords['Y'].extend(pivotSNR['Y'])
                    allCoords['T'].extend(originalSNR['T'])
                    
                    
                    
                elif snr.M80M90Present():
                    stepandrepeat = StepAndRepeat(pivotSNR, originalSNR, allCoords, snrOffsetX, snrOffsetY, xCount, yCount)
                    pivotSNR = stepandrepeat.addingOn()
              
                    
                elif snr.M70Present():
                    pivotSNR = m70(pivotSNR, originalSNR, snrOffsetX, snrOffsetY, modX=0, modY=0)
                    allCoords['X'].extend(pivotSNR['X'])
                    allCoords['Y'].extend(pivotSNR['Y'])
                    allCoords['T'].extend(originalSNR['T'])
                    
                    
                elif snr.M80Present():
                    stepandrepeat = StepAndRepeat(pivotSNR, originalSNR, allCoords, snrOffsetX, snrOffsetY, xCount, yCount, modifierY=0)
                    pivotSNR = stepandrepeat.addingOn()
                    
                    
                elif snr.M90Present():
                    stepandrepeat = StepAndRepeat(pivotSNR, originalSNR, allCoords, snrOffsetX, snrOffsetY, xCount, yCount, modifierX=0)
                    pivotSNR = stepandrepeat.addingOn()
                 
    
    
            elif rt.toolPresent() == True:
                if rt.toolDiam() == None:
                    currentT = round(float(tools[rt.toolNum()]), 4)
                    toolDiameters.append(currentT)
                else:
                    tools.update({rt.toolNum(): rt.toolDiam()[1:]})
                    
    
    
    
            elif m25.m25Present() == True:
                currentSNR = {'X': [], 'Y': [], 'T': []}
    
    
    
            elif line == 'M01\n':
                originalSNR = copy.deepcopy(currentSNR)
                pivotSNR = copy.deepcopy(currentSNR)
                allCoords['X'].extend(currentSNR['X'])
                allCoords['Y'].extend(currentSNR['Y'])
                allCoords['T'].extend(currentSNR['T'])
                
                
                
                
    df = pd.DataFrame(allCoords)
        
    
    
    
    fig = plt.figure(figsize=(7,7), dpi = 150)
    ax = fig.add_axes([0,0,1,1])
    
    
    m=0
    for key, group in df.groupby(['T'], sort=False):
        ax.scatter(group['X'], group['Y'], s=toolDiameters[m]*150, label=toolDiameters[m])
        m+=1
        
    ax.legend(loc=(1.02,0.14))
    
        
    
    et = time.time()
    print('Execution time:', et-st)
    
    
    plt.show()
    
    
    
    
    
if __name__ == "__main__":
    main()







