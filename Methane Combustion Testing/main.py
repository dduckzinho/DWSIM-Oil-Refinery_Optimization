import numpy as np
from dwsimopt.solve_sim_opt import OptimiSim

#path2dwsim=r"C:\Users\morit\AppData\Local\DWSIM7\\"
#path2sim=r"C:\Users\morit\Downloads\vscodeSTUFF"

path2dwsim=r"C:\Users\morit\AppData\Local\DWSIM7\\"
path2sim=r"G:\Other computers\My Laptop\vscodeSTUFF\MethaneCombustion.dwxmz"


sim=OptimiSim(
    path2sim=path2sim,
    path2dwsim=path2dwsim
)

"""
from DWSIM.Automation import Automation2
interf=Automation2()
sim.connect(interf)
"""


print(sim.flowsheet)
print(sim.interface)

error=sim.interface.CalculateFlowsheet2(sim.flowsheet)

print("Calculation result:", error)

"""
print(f"\n# obj in sim: {len(sim.flowsheet.SimulationObjects)}\n")
for obj in sim.flowsheet.SimulationObjects:
    print(f"{obj}\n")

"""

for obj in sim.flowsheet.SimulationObjects.Values:
    print(obj.GraphicObject.Tag)

stream=sim.flowsheet.GetFlowsheetSimulationObject("methane")

# stream info
print(type(stream))
print(stream)
print(dir(stream))

"""
# attribute exposed
print(stream.GetMolarFlow())


# testing changing stuff
stream.SetMolarFlow(3.0)

sim.interface.CalculateFlowsheet2(sim.flowsheet)

print(stream.GetMolarFlow())
"""


# dof

sim.add_dof(
    lambda x:(
        sim.flowsheet.GetFlowsheetSimulationObject("methane").SetMolarFlow(float(x)),        
        sim.flowsheet.GetFlowsheetSimulationObject("oxygen").SetMolarFlow(2.0*float(x))
    )
)


# objective

sim.add_fobj(
    lambda: np.array([
        -sim.flowsheet.GetFlowsheetSimulationObject("E3").EnergyFlow
    ])
)

# constraints

"""
contraint=function g(x)

g(x)<=0 => valid
g(x)>0 => invalid

"""

sim.add_constraint( # temp can't be more than 1000 kelvin
    lambda: np.array([
        sim.flowsheet.GetFlowsheetSimulationObject("9").GetTemperature()-
        1000.0
        ])) 

sim.add_constraint( # molar flow of methane must be at least 10 mol/s
    lambda: np.array([
        10.0-
        sim.flowsheet.GetFlowsheetSimulationObject("methane").GetMolarFlow()
        ])) 


x0=np.array([20.0]) # DE doesnt use x0
xlb=np.array([5.0])
xub=np.array([200.0])


# using differential evolution algorythm

if ("y"==input("run? ").lower().strip()):
    result=sim.DE(
        x0,
        xlb,
        xub,
        pop=10,
        max_ite=10,
        plotting=True
    )

    print(result)


""""
fobj = [8566.3149395]
g_0 = [-681.76263497]
g_1 = [0.31112303]

fobj = [-160597.09204101]
g_0 = [-681.76263497]
g_1 = [-171.6423372]

fobj = [-171960.26143793]
g_0 = [-681.76263497]
g_1 = [-184.49457892]
"""










