
import numpy as np
import config as c

from simulation import DWSIMSession
from problem import DistillationProblem

from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize

import matplotlib as plt

import results

def main():

    session=DWSIMSession()

    if input("yes to run: ")=="yes":
        if  session.simulate():
            from results import getResults
            print("pluh")
            print(getResults(session))
        else:
            print("smth went wrong gng")

    problem=DistillationProblem(session)
    algorithm=NSGA2(
        pop_size=20,
        eliminate_duplicates=True
    )

    print(results.getDistillationCurveInfo(session))

def runOptimization(problem, algorithm):

    result=minimize(
        problem,
        algorithm,
        termination=("n_gen", 10),
        seed=1,
        verbose=True
    )
    return result

if (__name__=="__main__"):
    main()


#------------------------------------------------------------------------------------------------------------#

"""
# testing.....
properties=flowsheetObjects["atm_cdu"].GetProperties(PropertyType.ALL)

print("Available properties:")
for prop in properties:
    print(repr(str(prop)))

print("\nTotal properties:", len(properties))

rRatio=flowsheetObjects["atm_cdu"].GetPropertyValue("Reflux ratio")
print("rratio", rRatio)

print("ss1", flowsheetObjects["atm_cdu"].GetPropertyValue("Sidestream1 liquid flow"))

print("ss3", flowsheetObjects["atm_cdu"].GetPropertyValue("Sidestream3 liquid flowratio"))
for name, compound in flowsheet.SelectedCompounds.items():
    print(name, compound.Molar_Weight)

"""
#------------------------------------------------------------------------------------------------------------#












