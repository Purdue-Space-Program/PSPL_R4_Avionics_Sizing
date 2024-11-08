import math
import numpy as np
import pandas as pd
import pandasql as ps
from datetime import datetime

# 8.265 inches outer diameter

def pack_mass(cellData, sysVoltage, sysPower):
    massResults = np.empty((len(cellData), 6), dtype=object)  # Update shape to match number of elements being stored
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

        # Calculate packing configuration
        square_side = 8.265 * math.sqrt(2) / 2  # Side length of the inscribed square
        if cellLength > 0 and cellWidth > 0:
            cells_per_square = max(1, math.floor(square_side / cellLength) * math.floor(square_side / cellWidth))
        else:
            cells_per_square = 1  # Ensure at least one cell is considered
        
        stacks_needed = math.ceil(cells / cells_per_square)
        stack_height = stacks_needed * cellThickness
        
        # Calculate total volume
        total_volume = square_side ** 2 * stack_height
        
        # Store results
        massResults[index] = (cellName, mass, cells_per_square, stacks_needed, stack_height, total_volume)
        
    return min(massResults, key=lambda x: x[1])
   
   
def main():
    inputs_path = "./inputs.xlsx"

    cellData = pd.read_excel(inputs_path, sheet_name='Cell Options')
    system_voltages = list(range(150, 291, 10))  # System voltages from 150V to 290V, in increments of 10V
    sysPower = 20000   # Example system power in Watts

    for sysVoltage in system_voltages:
        best_option = pack_mass(cellData, sysVoltage, sysPower)
        
        print(f"\nSystem Voltage: {sysVoltage}V")
        print(f"Best Cell Option: {best_option[0]}")
        print(f"Mass of Pack: {best_option[1]} grams")
        print(f"Cells Per Square: {best_option[2]}")
        print(f"Stacks Needed: {best_option[3]}")
        print(f"Total Stack Height: {best_option[4]} inches")
        print(f"Total Volume: {best_option[5]} cubic inches")

if __name__ == "__main__":
    main()
