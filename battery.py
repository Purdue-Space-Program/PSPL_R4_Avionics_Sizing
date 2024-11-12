import math
import numpy as np
import pandas as pd
import pandasql as ps
from datetime import datetime
import os
import glob


# 8.265 inches outer diameter

def pack_mass(cellData, sysVoltage, sysPower):
    massResults = np.empty((len(cellData), 7), dtype=object)  # Update shape to match number of elements being stored
    volumeResults = np.zeros(len(cellData))
    for index, row in cellData.iterrows():
        cellVoltage = row['Voltage(V)']
        cellCurrent = row['Max Discharge Current(A)']
        cellMass = row['Weight(g)']
        cellLength = row['Length(mm)'] / 25.4  # Convert mm to inches
        cellWidth = row['Width(mm)'] / 25.4  # Convert mm to inches
        cellThickness = row['Thickness(mm)'] / 25.4  # Convert mm to inches
        cellName = row['Cell Name']
        
      
        # Calculate number of cells needed
        series = math.ceil(sysVoltage / cellVoltage)
        parallel = math.ceil(sysPower / (sysVoltage * cellCurrent))
        cells = series * parallel   
        mass = cells * cellMass

        cellCurrentDrawn = sysPower / (sysVoltage * parallel)
        # Calculate packing configuration
        square_side = 8.625 * math.sqrt(2) / 2  # Side length of the inscribed square
        if cellLength > 0 and cellWidth > 0:
            cells_per_square = max(1, math.floor(square_side / cellLength) * math.floor(square_side / cellWidth))
        else:
            cells_per_square = 1  # Ensure at least one cell is considered
        
        stacks_needed = math.ceil(cells / cells_per_square)
        stack_height = stacks_needed * cellThickness
        
        # Calculate total volume
        total_volume = square_side ** 2 * stack_height
        
        # Store results
        massResults[index] = (cellName, mass, cellWidth, cellLength, cellThickness, cells, cellCurrentDrawn / cellCurrent)
    
    minResult = min(massResults, key=lambda x: x[1])
    with open(f"./reports/{sysVoltage}V_{sysPower}W_Report", "w") as f:
        for i in range(len(massResults)):
            if(massResults[i][1] < (8 / 0.00220462)):
                f.write(f"{massResults[i][0]}, Mass : {massResults[i][1] * 0.00220462} lbs, Number of Cells: {massResults[i][5]}, % Max Current: {massResults[i][6]}\n, Volume: {massResults[i][2] * massResults[i][3] * massResults[i][4] * massResults[i][5]} in^3\n") 
     
    with open(f"./summaryreports/SummaryReport_{sysPower}", "a") as f:
        f.write(f"Voltage: {sysVoltage}, {minResult[0]}, Mass : {minResult[1] * 0.00220462} lbs, Number of Cells: {minResult[5]}, % Max Current: {minResult[6]}, Volume: {minResult[2] * minResult[3] * minResult[4] * minResult[5]} in^3\n") 
        
        
        
    return min(massResults, key=lambda x: x[1])
   
   
def main():
    inputs_path = "./inputs.xlsx"
    reports_path = "./reports"
    summary_reports_path = "./summaryreports"
    
    files = glob.glob(os.path.join(reports_path, '*'))
    
    for file in files:
        try:
            os.remove(file)
            print(f"Removed {file}")
        except Exception as e:
            print(f"Error deleting {file}: {e}")
    
    files = glob.glob(os.path.join(summary_reports_path, '*'))
    
    for file in files:
        try:
            os.remove(file)
            print(f"Removed {file}")
        except Exception as e:
            print(f"Error deleting {file}: {e}")
        
    
    for sysPower in range(10000, 25000, 1000):
        
        cellData = pd.read_excel(inputs_path, sheet_name='Cell Options')
        system_voltages = list(range(100, 250, 10))  # System voltages from 150V to 290V, in increments of 10V        

        for sysVoltage in system_voltages:
            massResults = pack_mass(cellData, sysVoltage, sysPower)

        
        
        

if __name__ == "__main__":
    main()
