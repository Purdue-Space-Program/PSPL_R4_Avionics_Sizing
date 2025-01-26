from math import pi
import matplotlib.pyplot as plt

####################################################################
# Wire Sizing Script
#
# Author: Jeremy Shinn
# Contact me on slack or via email Shinn3@purdue.edu
#
# Descritpion: This code sizes wires for given current requirements
# visit the wire sizing confluence page for more information
#
####################################################################

def CalcTemp(Length, Resistivity, Density, Radius, ConvectiveCoefficient, TimeStep, HeatCapacity, Current, AirTemp, PreviousWireTemp):
    Area = 3.14 * Radius ** 2 #Cross sectional area of the wire
    SurfaceArea = 2 * 3.14 * Radius * Length #Total surface area of the wire
    Mass = Area * Length * Density 
    Resistance = ((Resistivity * Length) / Area) * (1 + TempResistCoeff * (PreviousWireTemp - AirTemp))
    
    
    PreviousEnergy = Mass * HeatCapacity * (PreviousWireTemp - AirTemp)
    EnergyIn = (Current ** 2) * Resistance * TimeStep
    EnergyOut = ConvectiveCoefficient * SurfaceArea * (PreviousWireTemp - AirTemp) * TimeStep
    EnergyStored = EnergyIn - EnergyOut
    WireTemp = (EnergyStored / (Mass * HeatCapacity)) + PreviousWireTemp
    return WireTemp


###########################################################################
# Define parameters
WireLength = 3 # [M] Length of the wire
Resistivity = 1.724 * 10**(-8) # [ohm Meters] Resistivity of the conductor
Density = 8850 # [kg/m^3] Density of conductor
HeatCapacity = 390 # [J/(kgK)] Specific heat capacity of conductor
ConvectiveCoefficient = 9 # [W/(m^2C)]  Convective heat transfer coefficient
RedlineTemperature = 250 # [C] maximum safe temperature for wires
TimeStep = .1 # [Seconds] Dark Templar!
AirTemp = 293 # [K] temperature of the air surrounding the wire
InitialWireTemp = 298 # [K] Initial wire temperature
TempResistCoeff = .00393 # [1/C] Temperature coefficient of resistance for conductor material
WireRadius = 0.003 # [M] Radius of the wire conductor
PreviousWireTemp = 20 # [K]
############################################################################


Temparray = []
TimeArray = []
####################
# Get inputs
Current = int(input("Please enter current requirements\ in amps: "))
####################



count = 0
while True:
    Temperature = CalcTemp(WireLength, Resistivity, Density, WireRadius, ConvectiveCoefficient, TimeStep, HeatCapacity, Current, AirTemp, PreviousWireTemp)
    Temparray.append(Temperature)
    TimeArray.append(count)
    if (Temperature - PreviousWireTemp) < .000000001:
        break
    PreviousWireTemp = Temperature
    count += 1
print(f"\nSteady state temperature: {str(round(Temperature - 273.15,2))} C")   
print("\nAmount of time to reach steady state: " + str(round((count * TimeStep)/60,2)) + " Minutes")

plt.plot(TimeArray, Temparray, color = "red")
plt.title("Wire Temperature", fontsize = 16, fontweight = "bold")
plt.xlabel("Time (seconds)")
plt.ylabel("Temperature (Kelvin)")
plt.grid(color='gray', linestyle='-', linewidth=0.5, alpha=0.7)
plt.show()