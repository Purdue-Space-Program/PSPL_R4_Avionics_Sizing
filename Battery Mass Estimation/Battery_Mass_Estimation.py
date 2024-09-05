import math

class Cell:
    def __init__(self, name, weight, capacity, nominalVoltage, discharge, cost) -> None:
        self.name = name
        self.weight = weight
        self.capacity = capacity
        self.nominalVoltage = nominalVoltage
        self.discharge = discharge
        self.cost = cost


def createBattery(cell, motorPower, motorRuntime, motorVoltage):
    
    motorCurrent = motorPower / motorVoltage
    totalEnergyUsed = motorRuntime*motorPower
    s = math.ceil(motorVoltage/cell.nominalVoltage)
    p = math.ceil(motorCurrent / cell.discharge)
    numCells = s * p 
    batteryWeight = cell.weight * 0.0022 * numCells
    batteryTotalEnergy = (s*cell.nominalVoltage)*(p*cell.capacity)*(3600)
    
    print(cell.name, "Battery Weight", batteryWeight, "numCells", numCells, "Extra stored energy", batteryTotalEnergy - totalEnergyUsed)
    
    
    
    

cell1 = Cell("14500 Lithium Ion", 21, 1, 3.7, 2, 7.95)
cell2 = Cell("18650 Lithium Ion", 46, 2800, 3.6, 35, 5.95)

createBattery(cell1, 8000, 20, 239)