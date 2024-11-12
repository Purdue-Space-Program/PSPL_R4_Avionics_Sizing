### update battery selection excel sheet with volume data ###
# 8.265 inches outer diameter
from math import ceil
import pandas as pd

# read excel sheet with battery cell data
df = pd.read_excel("./inputs.xlsx", sheet_name = "Cell Options")

def selection(voltage, mass, theo_max_current, req_voltage, req_current, current_derating):
    # change voltage derating if necessary
    max_current = theo_max_current * current_derating
    cells_series = ceil(req_voltage / voltage)
    cells_parallel = ceil(req_current / max_current)

    total_cells = cells_parallel * cells_series
    total_mass = mass * total_cells

    return total_mass

def main():
    total_mass_list = []
    number_of_batteries = df.shape[0]

    # required values for power and voltage
    
    
    req_power = int(input("required power (kW): "))
    req_voltage = int(input("required voltage: "))
    req_current = int(req_power) * 1000 / int(req_voltage)

    # iterate through batteries to calculate mass
    for i in range(number_of_batteries - 1):
        voltage = df.iloc[i, 1]
        mass = df.iloc[i, 5]
        theo_max_current = df.iloc[i, 4]
        mass_result = selection(voltage, mass, theo_max_current, req_voltage, req_current, 0.85)
        total_mass_list.append(mass_result)

    # searches list for minimum mass and calculates volume
    best_mass = min(total_mass_list) / 1000
    index = total_mass_list.index(min(total_mass_list))
    battery_code = df.iloc[index, 0]
    battery_volume = df.iloc[0, 7] * df.iloc[0, 8] * df.iloc[0, 9]
    
    print(f"Best mass (kg): {best_mass}")
    print(f"Best battery: {battery_code}")
    print(f"Volume (cubic mm): {battery_volume}")

if __name__ == "__main__":
    main()
