import math
import numpy as np
import pandas as pd
import pandasql as ps
from datetime import datetime

# 8.265 inches outer diameter

def pack_mass(cellData, sysVoltage, sysPower):
    massResults = np.empty((len(cellData), 2), dtype=object)
    volumeResults = np.zeros(len(cellData))
    for index, row in cellData.iterrows():
        cellVoltage = row['Voltage(V)']
        cellCurrent = row['Max Discharge Current(A)']
        cellMass = row['Weight(g)']
        cellLength = row['Length(mm)']
        cellWidth = row['Width(mm)']
        cellThickness = row['Thickness(mm)']
        cellName = row['Cell Name']
        
        series = math.ceil(sysVoltage / cellVoltage)
        parallel = math.ceil(sysPower / (sysVoltage * cellCurrent))
        cells = series * parallel   
        mass = cells * cellMass

        massResults[index] = (cellName, mass)
        
    return min(massResults, key=lambda x: x[1])
   
   
def main():
    inputs_path = "./inputs.xlsx"

    cellData = pd.read_excel(inputs_path, "Cell Options")

    sysPower = 21000
    sysVoltage = np.arange(90, 400,  10)

    for voltage in sysVoltage:
        batteryMass = pack_mass(cellData, voltage, sysPower)
        print("System Voltage: ", voltage, "V Cell Name", batteryMass[0], " Battery Mass: ", batteryMass[1], "g")

if __name__ == "__main__":
    main()