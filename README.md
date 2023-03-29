# ex2FileRead
## Summary

Opens Excellon EX2 files, plots it on a graph. Supports step-and-repeats, tool diameters. Estimation of drill time to come in a future update.

See below in section, "Display of Results," for images of results displaying the properties of various step and repeat commands.



## Detailed Analysis

### Step-and-Repeat Commands
* M02
  * Offset value command. Uses the previous offset's coordinates to calculate the next step and repeat values.
* M70
  * Swap the axes. X=Y and Y=X. The swap uses the previous step and repeat coordinates.
* M80
  * Mirror image X axis. Uses the original coordinates, not the previous step and repeat's. Mirror is solved for by subtracting 2x the original coordinate (1x to origin, 2x to mirror).
* M90
  * Mirror image Y axis. Uses the original coordinates, not the previous step and repeat's. Mirror is solved for by subtracting 2x the original coordinate (1x to origin, 2x to mirror).
* M70M80
  * Swap axes and mirror image X axis. Swaps the previous step and repeat's coordinates, adds the M02 offsets, then subtracts 2x the original X value to mirror in the X axis.
* M70M90
  * Swap axes and mirror image Y axis. Swaps the previous step and repeat's coordinates, adds the M02 offsets, then subtracts 2x the original Y value to mirror in the Y axis.
* M80M90
  * Mirror image X and Y axis. Adds the M02 offsets, then subtracts 2x the original X and Y values to mirror in both axes.
  
### Miscellaneous Commands
* M01
  * Command for the end of a step and repeat coordinate block and the start of any step and repeat commands. Using this to make copies of the coordinate block for use in step and repeat calculations as well as extending the full coordinate dictionary with this block's values.
* M25
  * Command for the start of a step and repeat block. Using this to clear out and set default any values inside of the current step and repeat dictionary.
  
### Regexing
Regex compiles were created to search and match for tool line definitions, X and Y coordinates, step and repeat commands and X / Y coordinates, M25 and M01 commands.
* The regex for tool line definitions finds and returns groups for the tool number, tool diameter, feed down, spindle speed, up feed, hit count, z-offset, and slot designation.
* The regex for X and Y coordinates finds and returns groups for one X and one Y coordinate.
* The step and repeat rexex finds and returns groups for X and Y coordinates and whether there are any M70, M80, M90, or any combination of them appended to the end of the line
* The M25 and M01 regexs search a line and returns True if that command is in a line by itself.


## Display of Results

Figure 1: M70 Step-and-Repeat Command. Abbreviated Tool 1 Only (Left), All Tools (Right)

![M70](https://user-images.githubusercontent.com/124814751/225461518-6f8d827c-aad6-4acf-916d-41ee5887b614.png)


Figure 2: M80 Step-and-Repeat Command. Abbreviated Tool 1 Only (Left), All Tools (Right)

![M80](https://user-images.githubusercontent.com/124814751/225461897-81f90965-c50b-4719-9a48-d56ef588d94d.png)


Figure 3: M90 Step-and-Repeat Command. Abbreviated Tool 1 Only (Left), All Tools (Right)

![M90](https://user-images.githubusercontent.com/124814751/225461908-35f216a2-fa1e-4b45-ada2-d15da276ae13.png)


Figure 4: M70M80 Step-and-Repeat Command. Abbreviated Tool 1 Only (Left), All Tools (Right)

![M70M80](https://user-images.githubusercontent.com/124814751/225461921-5ca2906e-e522-4e0c-826d-63fc78d30c4e.png)


Figure 5: M70M90 Step-and-Repeat Command. Abbreviated Tool 1 Only (Left), All Tools (Right)

![M70M90](https://user-images.githubusercontent.com/124814751/225461937-4a30eda5-ac88-4380-a0e7-17c154406d73.png)


Figure 6: M80M90 Step-and-Repeat Command. Abbreviated Tool 1 Only (Left), All Tools (Right)

![M80M90](https://user-images.githubusercontent.com/124814751/225461943-7742201b-4a23-48b2-af09-31cd791ada2d.png)



