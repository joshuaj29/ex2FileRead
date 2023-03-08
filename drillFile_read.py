# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 15:19:39 2022

@author: JoshuaJ
"""


import re
import matplotlib.pyplot as plt
import pandas as pd
import copy
import sys
import logging
import math
import datetime


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s -  %(levelname)s -  %(message)s')



drillFile = '34114dr'

try:
    file = open(r'\\server' + '\\' + drillFile, 'r')
except:
    print('FILE NOT FOUND')
    sys.exit()
        

xValue = re.compile('^X(-|)\d+')                 # x value regex
yValue = re.compile('Y(-|)\d+$')                 # y value regex
rxCoord = re.compile('X(-|)\d+')                 # x coordinate value for step and repeat commands
ryCoord = re.compile('Y(-|)\d+')                 # y coordinate value for step and repeat commands
cameraCoords = re.compile(r'(/|G93|M46)(|G93|M46)(X\d+Y\d+|X\d+|Y\d+)')
toolValue = re.compile('T\d\d')                      # tool number regex (in body)
toolHeader = re.compile('T\d+(C|F|H|S)(\d+|.\d+)'
                        '(C|F|H|S)(\d+|.\d+)'
                        '(C|F|H|S)(\d+|.\d+)'
                        '(C|F|H|S)(\d+|.\d+)')       # tool number regex (in header)
toolBody = re.compile('T\d+((C|F|H|S)(\d+|.\d+)|'
                        '(C|F|H|S)(\d+|.\d+)|'
                        '(C|F|H|S)(\d+|.\d+)|'
                        '(C|F|H|S)(\d+|.\d+))')         # same as toolHeader but accounts for "-all" programs
r_m02 = re.compile('M02X(-|)\d+Y(-|)\d+$')               # step and repeat regex
r_m02m70 = re.compile('M02X(-|)\d+Y(-|)\d+M70$')         # swap the axes regex
r_m02m80 = re.compile('M02X(-|)\d+Y(-|)\d+M80$')         # mirror image X Axis regex
r_m02m90 = re.compile('M02X(-|)\d+Y(-|)\d+M90$')         # mirror image Y axis regex
r_m02m70m90 = re.compile('M02X(-|)\d+Y(-|)\d+M70M90$')   # swap axis & mirror Y regex
r_m02m80m90 = re.compile('M02X(-|)\d+Y(-|)\d+M80M90$')   # mirror image X & Y Axis regex
r_m02m70m80 = re.compile('M02X(-|)\d+Y(-|)\d+M70M80$')   # swap axis and mirror X regex
r_m25 = re.compile('M25')                           # start of start and repeat regex
r_m01 = re.compile('^M01')                           # end of step and repeat regex
r_g92 = re.compile('^G92')



# Create DataFrame dictionary
d1 = {'line':[],
      'tool':[],
      'x':[],
      'y':[],
      'block':[]}


# Create tool Dictionary
toolDict = []
toolSize = []
sizeOtool = []

# Create step and repeat dictionary
sNr_dict = {'blk' : [],
            'x_coord' : [],
            'y_coord' : [],
            'command' : [],
            'number' : []}
x_coord = 0
y_coord = 0
command = 0
number = 0


# initialize append values
line = 0
tool = 0
x = 0
y = 0
block = 0

for i in file:
    # search regex
    xline = xValue.search(i)
    yline = yValue.search(i)
    toolline = toolValue.search(i)
    toolhline = toolHeader.search(i)
    toolbline = toolBody.search(i)
    l_m02 = r_m02.search(i)
    l_m02m70 = r_m02m70.search(i)
    l_m02m80 = r_m02m80.search(i)
    l_m02m90 = r_m02m90.search(i)
    l_m02m70m90 = r_m02m70m90.search(i)
    l_m02m80m90 = r_m02m80m90.search(i)
    l_m02m70m80 = r_m02m70m80.search(i)
    l_m25 = r_m25.search(i)
    l_m01 = r_m01.search(i)
    l_g92 = r_g92.search(i)
    lxCoord = rxCoord.search(i)
    lyCoord = ryCoord.search(i)
    lcameraCoords = cameraCoords.search(i)
       

    # line has no x, y, tool, or step and repeat
    if (
            xline == None and 
            yline == None and 
            toolline == None and
            l_m02 == None and
            l_m02m70 == None and
            l_m02m80 == None and
            l_m02m90 == None and
            l_m02m70m80 == None and
            l_m02m70m90 == None and
            l_m02m80m90 == None and
            l_m25 == None
            ):
        
        continue
        
    
    # line contains zero point G92 command
    elif l_g92 != None:
        
        continue
    
    # line is in the header - adds tool size to list, to be used in graphing
    elif toolhline != None:
        
        toolSize.append(float(toolhline.group()[-5:])*200)
        sizeOtool.append(toolhline.group()[-5:])
    
    
    
    # line is not header but has diameter in it - used for -all programs
    elif toolbline != None and toolhline == None:
        
        toolSize.append(float(toolbline.group()[-5:])*200)
        
        
    
    # line has tool number but is not header
    elif toolline != None and toolbline == None:
        
        tool = int(toolline.group()[1:])    
    
        toolDict.append({i:line})
        
        
        
    # line has M25 command (start of step and repeat block)
    elif l_m25 != None:
        
        block +=1    
        

        
    # line has x and y value
    elif (xline != None and
          yline != None and
          lcameraCoords == None
          ):
        
        if xline.group()[1] == '-':
            x = float(xline.group()[1:4] + '.' + xline.group()[4:])
        else:
            x = float(xline.group()[1:3] + '.' + xline.group()[3:])
            
        if yline.group()[1] == '-':
            y = float(yline.group()[1:4] + '.' + yline.group()[4:])
        else:
            y = float(yline.group()[1:3] + '.' + yline.group()[3:])
           

        d1['line'].append(line)
        d1['tool'].append(tool)
        d1['x'].append(x)
        d1['y'].append(y)
        d1['block'].append(block)  
        
        line += 1
        
        
    # line has x but no y value
    elif (
            xline != None and
            yline == None and
            lcameraCoords == None
            ):
        
        if xline.group()[1] == '-':
            x = float(xline.group()[1:4] + '.' + xline.group()[4:])
        else:
            x = float(xline.group()[1:3] + '.' + xline.group()[3:])
    
        d1['line'].append(line)
        d1['tool'].append(tool)
        d1['x'].append(x)
        d1['y'].append(y)
        d1['block'].append(block)   
        
        line += 1

    
    # line has y but no x value
    elif (
            yline != None and
            xline == None and
            l_m02 == None and
            lcameraCoords == None
            ):

        if yline.group()[1] == '-':
            y = float(yline.group()[1:4] + '.' + yline.group()[4:])
        else:
            y = float(yline.group()[1:3] + '.' + yline.group()[3:])
        #logging.info([x, yline.group()])
        d1['line'].append(line)
        d1['tool'].append(tool)
        d1['x'].append(x)
        d1['y'].append(y)
        d1['block'].append(block)   
        
        line += 1
        
            
    # line contains any M02 command
    elif (
            l_m02 != None or
            l_m02m70 != None or
            l_m02m80 != None or
            l_m02m90 != None or
            l_m02m70m80 != None or
            l_m02m70m90 != None or
            l_m02m80m90 != None
            ):
        
        if lxCoord.group()[1] == '-':
            x_coord = float(lxCoord.group()[1:4] + '.' + lxCoord.group()[4:])
        else:
            x_coord = float(lxCoord.group()[1:3] + '.' + lxCoord.group()[3:]) 
        
        if lyCoord.group()[1] == '-':
            y_coord = float(lyCoord.group()[1:4] + '.' + lyCoord.group()[4:])
        else:
            y_coord = float(lyCoord.group()[1:3] + '.' + lyCoord.group()[3:]) 
            
    
            
        if l_m02m70 != None:
            command = 'm02m70'
            
        elif l_m02m80 != None:
            command = 'm02m80'
            
        elif l_m02m90 != None:
            command = 'm02m90'
            
        elif l_m02m70m80 != None:
            command = 'm02m70m80'
            
        elif l_m02m70m90 != None:
            command = 'm02m70m90'
            
        elif l_m02m80m90 != None:
            command = 'm02m80m90'
            
        elif l_m02 != None:
            command = 'm02'
        
        sNr_dict['blk'].append(block)
        sNr_dict['x_coord'].append(x_coord)
        sNr_dict['y_coord'].append(y_coord)
        sNr_dict['command'].append(command)
        sNr_dict['number'].append(number)
        
        number += 1
        
        
        
    else:
        continue




# close the file
file.close()



    
    
def sNr_append(dict1, dict2, axis1='x', axis2='y', modifier1 = 2, modifier2 = 2):
    '''

    Parameters
    ----------
    dict1 : dictionary
        Dictionary 1. This should be d1 and its values will be overwritten.
    dict2 : dictionary
        Dictionary 2. This should be d2 and its values will be appended to and graphed.
    axis1 : string
        x or y axis to be used in transX. Default is x
    axis2 : string
        x or y axis to be used in transY. default is y
    modifier1 : integer, optional
        0 or 2. Determines if we are using the "*-1 Axis" modifing command. The default is 2.
        Used in transX
    modifier2 : integer, optional
        0 or 2. Determines if we are using the "*-1 Axis" modifing command. The default is 2.
        Used in transY

    Returns
    -------
    None.

    '''
    
    step_x = copy.deepcopy(dict1['x'][items])
    step_y = copy.deepcopy(dict1['y'][items])
    offset_x = sNr_dict['x_coord'][i]
    offset_y = sNr_dict['y_coord'][i]
    
    
    dict1['x'][items] = step_x + offset_x
    dict1['y'][items] = step_y + offset_y
    
    transX = copy.deepcopy(step_x + offset_x - (dict2[axis1][items])*modifier1)
    transY = copy.deepcopy(step_y + offset_y - (dict2[axis2][items])*modifier2)
    
    dict2['x'].append(transX)
    dict2['y'].append(transY)
    dict2['tool'].append(copy.deepcopy(dict1['tool'][items]))
    dict2['block'].append(copy.deepcopy(dict1['block'][items]))
    
    






# define all functions for M02 commands and what is done to the dataframe
# M70, M80, M90 commands do not affect other step and repeats, only the M02
d2 = {'tool': copy.deepcopy(d1['tool']),
      'x': copy.deepcopy(d1['x']),
      'y': copy.deepcopy(d1['y']),
      'block': copy.deepcopy(d1['block'])}




# M70 true offset - used in conjunction with m70_sNr
def m70_true(sNr_dict = sNr_dict):
    '''
    Parameters
    ----------
    sNr_dict : DICT, optional
        Dictionary sNr_dict used to get true offsets. The default is sNr_dict.

    Returns
    -------
    m70_xoffset : FLOAT
        true x offset for M70 command.
    m70_yoffset : FLOAT
        true y offset for M70 command.

    '''
    p = copy.deepcopy(i)
    m70_xoffset = 0
    m70_yoffset = 0
    while p > 0:
        if sNr_dict['blk'][p] == sNr_dict['blk'][p-1]:
            m70_xoffset += sNr_dict['x_coord'][p-1]
            m70_yoffset += sNr_dict['y_coord'][p-1]
            p-=1
        else:
            break
        
    return m70_xoffset, m70_yoffset



# modified version of sNr_append to account for m70 commands. Uses defined function m70_true
# addition of original coordinates, all step and repeat offset changes before current group,
# current group offset, minus original coordinates times a 0 or 2 modifier for M80 or M90
def m70_sNr(dict1 = d1, dict2 = d2, sNr_dict = sNr_dict, modifier1 = 0, modifier2 = 0):
    '''
    Parameters
    ----------
    dict1 : Dict, optional
        d1 dictionary. The default is d1.
    dict2 : Dict, optional
        d2 dictionary. The default is d2.
    sNr_dict : Dict, optional
        step and repeat dictionary sNr_dict. The default is sNr_dict.
    modifier1 : Int, optional
        Used to turn M90 function on or off. On position = 2. The default is 0.
    modifier2 : Int, optional
        Used to turn M80 function on or off. On position = 2. The default is 0.

    Returns
    -------
    None.

    '''
    step_x = copy.deepcopy(dict1['x'][items])
    step_y = copy.deepcopy(dict1['y'][items])
    offset_x = sNr_dict['x_coord'][i]
    offset_y = sNr_dict['y_coord'][i]
    
    
    dict1['x'][items] = step_x + offset_x
    dict1['y'][items] = step_y + offset_y
    
    m70_xoffset, m70_yoffset = m70_true()
    
    transX = copy.deepcopy((dict2['y'][items]) + m70_xoffset + offset_x - (dict2['y'][items])*modifier1 )
    transY = copy.deepcopy((dict2['x'][items]) + m70_yoffset + offset_y - (dict2['x'][items])*modifier2 )
    
    dict2['x'].append(transX)
    dict2['y'].append(transY)
    dict2['tool'].append(copy.deepcopy(dict1['tool'][items]))
    dict2['block'].append(copy.deepcopy(dict1['block'][items]))






for i in range(len(sNr_dict['blk'])):
    #logging.debug(sNr_dict['command'][i])
    for items in range(len(d1['block'])):
        
        if d1['block'][items] == sNr_dict['blk'][i]:
            
            # step and repeat command is M02 - add offset
            if sNr_dict['command'][i] == 'm02':

                sNr_append(d1, d2, modifier1 = 0, modifier2 = 0)                
                
            
            # step and repeat command is M02M70 - add offset and flip axis (rotate 90 degrees)
            # M70 - need to add all previous offsets to original coordinates (then flip will work)
            elif sNr_dict['command'][i] == 'm02m70':
                
                m70_sNr()
                

            # step and repeat command is M02M80 - add offset and *-1 X axis            
            elif sNr_dict['command'][i] == 'm02m80':
                
                sNr_append(d1, d2, modifier2 = 0)
                
            
            # step and repeat command is M02M90 - add offset and *-1 Y axis
            elif sNr_dict['command'][i] == 'm02m90':
                
                sNr_append(d1, d2, modifier1 = 0)
                
 
            # step and repeat command is M02M70M80 - add offset, flip axes (rotate), *-1 X axis
            elif sNr_dict['command'][i] == 'm02m70m80':
                
                
                m70_sNr(modifier2 = 2)
                
                
            # step and repeat command is M02M70M90 - add offset, flip axes, *-1 Y axis
            elif sNr_dict['command'][i] == 'm02m70m90':
                
                m70_sNr(modifier1 = 2)
                
                
            # step and repeat command is M02M80M90 - add offset, *-1 X and Y axis
            elif sNr_dict['command'][i] == 'm02m80m90':
                
                sNr_append(d1, d2)
                




# Create new, final dataframe containing all step and repeat points
df2 = pd.DataFrame(data = d2)

df2.rename_axis('myIdx').sort_values(by = ['block','myIdx'], ascending = [True,True])




# Graph Results
# change plot size based on diameter size (tIndex and s=toolSize)

fig = plt.figure(figsize=(8,8), dpi=160)
ax = fig.add_axes([0,0,1,1])

tIndex=0
for key, group in df2.groupby(['tool']):
    ax.scatter(group['x'], group['y'], s=toolSize[tIndex], label=round(toolSize[tIndex]/200,4))
    tIndex+=1
    
ax.legend(loc=(1.02,0.14))
    
plt.show()




#%%    


# Time to Drill! - calculate drilling time based on distance between holes,
# drill changes, hit count, down feeds




def kinematics(accel,distArray,vmax):
    totTime = []
    for i in distArray:
        
        timeini = vmax / accel
        
        dx2vmax = (vmax/2)*timeini
        
        if dx2vmax > i:
            #vfinal = math.sqrt(2 * (accel) * (i))
            time2i = math.sqrt( (i*2) / accel)
            time2vmax = 0
            
            time = time2i
        else:     #dx2vmax <0 i
            time2vmax = timeini
            time2i = (i - dx2vmax) / vmax
            
            time = time2i + time2vmax
        
        '''
        vfinal = math.sqrt(2*accel*i)
        
        if vfinal > vmax:
            vfinal = vmax
        
        timeToVmax = vfinal/accel
        dx = 0.5*accel*(timeToVmax**2)
        
        if dx > i:
            timeToVmax = 0
            time = i*2/(vfinal)
        else:
            time = (i-dx)*2/(vfinal)
        '''
            
            
        
        
        totTime.append(time)
        
    return sum(totTime)






def hitKin(vmax,zob,accel):     #hit kinematics
    
    timeToVmax = vmax/accel
    
    dx = .5*accel*(timeToVmax**2)
    
    if dx > zob:
        timeToVmax = 0
        time = (zob)*2/(vmax)
    else:
        time = (zob-dx)*2/(vmax)
        
    return time + timeToVmax





# get distance between all holes (in order)
def distPoints(distArray, pDict):

    
    for i in range(len(pDict)-1):
        p = [pDict['x'][i], pDict['y'][i]]
        q = [pDict['x'][i+1], pDict['y'][i+1]]
        distArray.append(math.dist(p,q))
    
    return distArray




# open diameter pages    
dpageName = ['HT500','HT750','HT1000 (FR4)','HT1000 (FR4MC)',
             'HT1000 (FR4HC)','HT1500','POLY300','POLY500',
             'POLY1000','TEFLON300 (TEFLON)','TEFLON300 (ROGERSHC)','TEFLON750']



def totDrillTime(zob, dPage, dist, s_tdTime, mxy_tdTime, sizeOtool=sizeOtool):

    
    # read diameter pages and get their down feed, up feed, hit count for tools in graph
    r_diam = re.compile('C0.\d+')
    r_upF = re.compile('B\d+')
    r_downF = re.compile('F\d+')
    r_hit = re.compile('H\d+')
    
    
    toolPage = {'Diameter':[],
                'UpFeed':[],
                'DownFeed':[],
                'HitCount':[],
                'Hits':[],
                'DChanges':[]}
    
    
    dPage_path = r'C:/Users/joshuaj/Documents/Drilling/Engineering/Kyo-TCT Diam Pages' + '/'
    
    
    # parses all diameter pages
    for i1 in sizeOtool:
        with open(dPage_path + dPage + '.txt','r') as diameterPage:
            for j1 in diameterPage:

                if i1 == r_diam.search(j1).group()[2:] and j1[-3:-1]!='w1' and j1 != '':
                    toolPage['Diameter'].append(float(r_diam.search(j1).group()[1:]))        
                    toolPage['UpFeed'].append(float(r_upF.search(j1).group()[1:]))       # inches per min second
                    toolPage['DownFeed'].append(float(r_downF.search(j1).group()[1:]))   # inches per min second
                    toolPage['HitCount'].append(float(r_hit.search(j1).group()[1:]))
            
    
    
    
    
    # get amount of up and down time by using down feed, up feed
    
    
    # get amount of hits per drill
    for key,group in df2.groupby(['tool']):
        toolPage['Hits'].append(len(group['tool']))
    
    
    
    
    downTime_s = []
    downTime_mxy = []
    for j in range(len(toolPage['Diameter'])):
        downTime_s.append(hitKin(toolPage['DownFeed'][j], zob, s_accel) * toolPage['Hits'][j])
        downTime_mxy.append(hitKin(toolPage['DownFeed'][j], zob, mxy_accel) * toolPage['Hits'][j])
    
        
        
    upTime_s = []
    upTime_mxy = []
    for j in range(len(toolPage['Diameter'])):
        upTime_s.append(hitKin(toolPage['UpFeed'][j], zob, s_accel) * toolPage['Hits'][j])
        upTime_mxy.append(hitKin(toolPage['UpFeed'][j], zob, mxy_accel) * toolPage['Hits'][j])
        
    
    downTime_s = sum(downTime_s)
    downTime_mxy = sum(downTime_mxy)
    upTime_s = sum(upTime_s)
    upTime_mxy = sum(upTime_mxy)
    
    
    
    # get number of drill changes by using hit count and number of hits per drill
    for j in range(len(toolPage['HitCount'])):
        toolPage['DChanges'].append( math.ceil(toolPage['Hits'][j] / toolPage['HitCount'][j]))
        
        
    tChanges = sum(toolPage['DChanges'])
    
    tChange_s = tChanges * (35/60)
    tChange_mxy = tChanges * (27/60)
    

    
    
    # calculate time to reach all holes based on distance
    
    
    s_tdTime = kinematics(s_accel,dist,s_velo)
    mxy_tdTime = kinematics(mxy_accel,dist,mxy_velo)
    
    
     
    # add all times together and display runtime for each diameter page in hours
    
    totalTime_s = datetime.timedelta(hours = ((tChange_s + upTime_s + downTime_s + s_tdTime) / 60) )
    totalTime_mxy = datetime.timedelta(hours = ((tChange_mxy + upTime_mxy + downTime_mxy + mxy_tdTime) / 60))
    
    
    print(totalTime_s, totalTime_mxy, dPage)
    #print(tChange_s, upTime_s, downTime_s, s_tdTime, dPage)
    
    
    
    return toolPage, downTime_s, upTime_s






# zob is quickdrill height - set on machine

machineHeight = 0.02

zob = .062 + machineHeight   # TODO: check if correct - may be stack height + little extra



dist = []
distPoints(dist,df2)




# Speedmasters - Vmax = 100m/min, Amax = 9 m/sec^2
    # Vmax = 65.6168 in/s, Amax = 354.3307 in/sec^2
# MXY - Vmax = 80 m/min, Amax = 12 m/sec^2
    # Vmax = 52.4934 in/s, Amax = 472.4409 in/sec^2

s_accel = 1275590.55 # in / minute squared
s_velo = 3937.01     # in per minute
mxy_accel = 1700787  # in/minute squared
mxy_velo = 3149.61   # in per minute


s_tdTime = kinematics(s_accel,dist,s_velo)
mxy_tdTime = kinematics(mxy_accel,dist,mxy_velo)



 
for i in dpageName:
    dPage, dtime, utime = totDrillTime(zob,i,dist, s_tdTime, mxy_tdTime)

















