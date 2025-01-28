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

def CalcTemp(PreviousConTemp, PreviousInTemp):

    Resistance = ((Resistivity * WireLength) / ConCrossArea) * (1 + ConTempResistCoeff * (PreviousConTemp - AirTemp))
    
    
    PreviousConEnergy = ConMass * ConHeatCapacity * (PreviousConTemp - AirTemp)
    PreviousInEnergy = InMass * InHeatCapacity * (PreviousInTemp - AirTemp)
    ConEnergyIn = (Current ** 2) * Resistance * TimeStep
    
    InEnergyIn = TimeStep * InConductiveCoefficient * ConSurfaceArea * (PreviousConTemp - PreviousInTemp) / InThickness 
    InEnergyOut = AirConvectiveCoefficient * InSurfaceArea * (PreviousInTemp - AirTemp) * TimeStep
    
    InEnergyStored = InEnergyIn - InEnergyOut + PreviousInEnergy
    ConEnergyStored = ConEnergyIn - InEnergyIn + PreviousConEnergy
    ConTemp = (ConEnergyStored / (ConMass * ConHeatCapacity)) + AirTemp
    InTemp = (InEnergyStored / (InMass * ConHeatCapacity)) + AirTemp
    return ConTemp, InTemp


###########################################################################
# Define parameters
WireLength = 3 # [M] Length of the wire
Resistivity = 1.724 * 10**(-8) # [ohm Meters] Resistivity of the conductor

ConDensity = 8850 # [kg/m^3] Density of conductor
ConHeatCapacity = 390 # [J/(kgK)] Specific heat capacity of conductor
InitialConTemp = 293.15 # [K] Initial temperature of the conductor
ConTempResistCoeff = .00393 # [1/C] Temperature coefficient of resistance for conductor material
ConRadius = 0.0015 # [m] Radius of the wire conductor
ConCrossArea = 3.14 * ConRadius ** 2 # [m^2] Cross sectional area of the condcutor
ConSurfaceArea = 2 * 3.14 *ConRadius * WireLength # [m^2] Total surface area of the conductor
ConMass = ConCrossArea * WireLength * ConDensity # [kg] Mass of the conductor
PreviousConTemp = 0
TimeStep = 1 # [Seconds] Dark Templar!
AirTemp = 293 # [K] temperature of the air surrounding the wire

InThickness = .0015 # [m] Outer radius minus inner radius
InConductiveCoefficient = .304 # [W/mK] Thermal conductivity of the insulative material
InDensity = 2200 # [kg/m^3] Density of the insulative material
InCrossArea = 3.14 * (ConRadius + InThickness) ** 2 - ConCrossArea # [m^2] Cross-sectional area of the insulative material
InMass = InDensity * InCrossArea # [kg] Mass of the insulative material
InHeatCapacity = 390 # [J/kgK] Specific heat capacity of the insulative material
InSurfaceArea = 2 * 3.14 * (ConRadius + InThickness) * WireLength # [m^2] Outer surface area of the insulator
InitialInTemp = InitialConTemp # [K] Initial temperature of the insulation

AirConvectiveCoefficient = 9 # [W/(m^2C)] Convective heat transfer coefficient
ConTempArray = []
InTempArray = []
TimeArray = []
############################################################################



####################
# Get inputs
Current = int(input("Please enter current requirements\ in amps: "))
####################



count = 0
PreviousTemps = CalcTemp(InitialConTemp, InitialInTemp)
print(f'Previous conductor: {PreviousTemps[0]}\n Previous insulation temp: {PreviousTemps[1]}')
while True:
    Temperatures = CalcTemp(PreviousTemps[0],PreviousTemps[1])
    
    ConTempArray.append(Temperatures[0] - 273.15)
    InTempArray.append(Temperatures[1] - 273.15)
    TimeArray.append(count)
    if (Temperatures[0] - PreviousTemps[0]) < .0000000001:
        break
    PreviousTemps = Temperatures
    count += 1

print(f"\nSteady state conductor temperature: {str(round(Temperatures[0]))} C")
print(f"\nSteady state insulation temperature: {str(round(Temperatures[1]))} C")      



plt.plot(TimeArray, ConTempArray, color = "red", label = 'Conductor')
plt.title("Wire Temperature", fontsize = 16, fontweight = "bold")
plt.xlabel("Time (seconds)")
plt.ylabel("Temperature (Celsius)")
plt.grid(color='gray', linestyle='-', linewidth=0.5, alpha=0.7)
plt.plot(TimeArray, InTempArray, color = "blue", label = 'Insulation')
plt.legend()

plt.show()