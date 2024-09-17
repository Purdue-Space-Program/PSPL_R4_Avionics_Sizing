import math
import numpy as np
import pandas as pd
import pandasql as ps
from datetime import datetime

def flight_mass_estimate(motorData, cellData):
    
    voltage = motorData['Max Volts']
    current = motorData['Max Amps']
    power = voltage * current
    motorName = motorData['Motor']
    cellVoltage = cellData['Nominal Voltage']
    cellCurrent = cellData['Maximum Discharge Current']
    cellWeight = cellData['Weight'] * 0.00220462
    cellName = cellData['Name']
    
    batteryOptions = pd.DataFrame(columns=["Motor Model", "Cell Model", "Voltage", "Discharge Current Max", "Weight" ])
    
    
    for i in range(len(motorData)):

        for j in range(len(cellData)):
            if(cellData['Use'][j] == 'Flight'):
                s = math.ceil(voltage[i] / cellVoltage[j] )
                p = math.ceil(current[i] / cellCurrent[j])
                numCells = s * p
                weight = cellWeight[j] * numCells
                batteryVoltage = s * cellVoltage[j]
                batteryMaxDischarge = p *  cellCurrent[j]
                new_data = [motorName[i], cellName[j], batteryVoltage, batteryMaxDischarge, weight]
                batteryOptions.loc[len(batteryOptions)] = np.array(new_data)

