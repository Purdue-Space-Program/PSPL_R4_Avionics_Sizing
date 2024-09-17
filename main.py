import math
import pandas as pd
import numpy as np
import battery as battery

inputs_path = "./inputs/inputs.xlsx"

motorData = pd.read_excel(inputs_path, "Neumotors 1545 Data", usecols='A, B, G, H')
cellData = pd.read_excel(inputs_path, "Cell Inputs")

batteryMass = battery.flight_mass_estimate(motorData, cellData)

