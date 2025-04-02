import math
import numpy as np
import pandas as pd

# CONSTRAINTS
OUTER_TANK_DIAMETER_INCHES  = 8.265 # inches
TANK_WALL_THICKNESS_INCHES  = 0.148 # inches
MID_AIRFRAME_HEIGHT_INCHES  = 8 # inches, approximately
LOX_TXTUBE_VOLUME_REDUCTION = 0.2 # constant
TARGET_POWER = 20000 # Watts
TARGET_VOLTAGE = 100 # Volts
TARGET_TIME  = 15 # seconds
CURRENT_SAFETY_FACTOR = 1.25

# DERIVED CONSTRAINTS
# 1 inch = 2.54 cm
OUTER_TANK_DIAMETER_CM = OUTER_TANK_DIAMETER_INCHES * 2.54
MID_AIRFRAME_HEIGHT_CM = MID_AIRFRAME_HEIGHT_INCHES * 2.54
TANK_WALL_THICKNESS_CM = TANK_WALL_THICKNESS_INCHES * 2.54
# square percent area of circle * pi * (outer_diameter-(tank_thickness*2))^2 * h * volume reduction
USEABLE_MID_AIRFRAME_VOLUME_CM = 2/np.pi * np.pi * math.pow((OUTER_TANK_DIAMETER_CM - (2 * TANK_WALL_THICKNESS_CM)) / 2, 2) * MID_AIRFRAME_HEIGHT_CM * (1 - LOX_TXTUBE_VOLUME_REDUCTION)

def main() -> None:
    # contains battery options
    batteries = pd.read_excel('inputs.xlsx', sheet_name='Cylindrical').drop_duplicates()
    battery_filter(batteries, TARGET_VOLTAGE).sort_values(by='Capacity(mAh)', ascending=False).to_excel('battery_options.xlsx')

def battery_filter(battery_options: pd.DataFrame, target_voltage: int) -> pd.DataFrame:
    target_current = (TARGET_POWER / target_voltage) * CURRENT_SAFETY_FACTOR

    good_batteries = pd.DataFrame()
    for _index, cell in battery_options.iterrows(): 
        num_series = math.ceil(target_voltage / cell['Voltage(V)'])
        num_parallel = math.floor(target_current / cell['Max Discharge Current(A)'])
        num_batteries_required = num_series * num_parallel

        # cell must be able to support required power
        # if max_current <= target_current:
            # continue

        # volume of required cells must fit
        # 2 mm of cotton between every 2 cells
        # convert mm^3 to cm^3
        total_volume_cm = ((cell['Diameter(mm)'] * cell['Diameter(mm)'] * cell['Height(mm)'] / 1000) * num_batteries_required) + ((math.ceil(num_batteries_required / 2) - 1) * 0.2) 
        if total_volume_cm >= USEABLE_MID_AIRFRAME_VOLUME_CM:
            continue

        # batteries must be able to run at 50A for at least TARGET_TIME seconds
        # mAh to seconds conversion
        max_time = cell['Capacity(mAh)'] * num_parallel / 1000 * 60 * 60 / target_current
        if max_time < TARGET_TIME:
            continue
        
        #total_thickness = num_batteries_required * cell['Thickness(mm)'] / 25.4 + ((math.ceil(num_batteries_required / 2) - 1) * 0.2)
        #num_stacks = math.ceil((total_thickness / MID_AIRFRAME_HEIGHT_INCHES))
        
        cell['Num Batteries']       = num_batteries_required
        # g to lbm conversion
        cell['Total Weight(lbm)']   = num_batteries_required * cell['Weight(g)'] / 1000 * 2.205
        # cm^3 to in^3 conversion
        cell['Total Volume(in^3)']  = total_volume_cm / 16.387
        # mm to inches conversion
        #cell['Total Thickness(in)'] = total_thickness
        #cell['Num Stacks']          = num_stacks
        cell['Maximum Time(s)']     = max_time

        good_batteries = pd.concat([good_batteries, cell.to_frame().T])

    return good_batteries

if __name__ == '__main__':
    main()