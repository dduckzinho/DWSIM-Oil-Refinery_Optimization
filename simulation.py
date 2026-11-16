import os
import sys
import pythonnet
import config as c
import numpy as np
import traceback



class DWSIMSession:

    def __init__(self):
        pythonnet.load("netfx")

        import clr

        if str(c.DWSIM_PATH) not in sys.path:
            sys.path.insert(0, str(c.DWSIM_PATH))

        os.chdir(c.DWSIM_PATH)

        clr.AddReference(
            str(c.DWSIM_PATH / "DWSIM.Automation.dll")
        )

        from DWSIM.Automation import Automation3 # pyright: ignore[reportMissingImports]

        self.interf=Automation3()
        self.flowsheet=self.interf.LoadFlowsheet(
            str(c.SIMULATION_PATH)
        )

        self.flowsheetObjects={}

        for obj in self.flowsheet.SimulationObjects.Values:
            name=str(obj.GraphicObject.Tag)

            self.flowsheetObjects[name]=(
                self.flowsheet.GetFlowsheetSimulationObject(name)
            )

    def setVariables(self, x):
        
        if len(x)!=len(c.OPERATING_VARIABLES):

            raise ValueError(
                f"expected {len(c.OPERATING_VARIABLES)} variables"
                f"received {len(x)}"
            )

        print("before")
        for objectName, propertyName, value, unit in self.getCurVarValues():
            print(f"{objectName}.{propertyName}: {value} ({unit})")

        for (objectName, propertyName), value in zip(c.OPERATING_VARIABLES, x):

            self.flowsheetObjects[objectName].SetPropertyValue(propertyName, float(value))

        print("\nafter")
        for objectName, propertyName, value, unit in self.getCurVarValues():
            print(f"{objectName}.{propertyName}: {value} ({unit})")

    def getCurVarValues(self):
        result=[]

        for objectName, propertyName in c.OPERATING_VARIABLES:

            value=self.flowsheetObjects[objectName].GetPropertyValue(propertyName)
            unit=self.flowsheetObjects[objectName].GetPropertyUnit(propertyName)

            result.append((objectName, propertyName, value, unit))

        return result


    def simulate(self, x=[50.0, 1.5, 5.0/1000, 2.0/1000, 2.5/1000, 2.8/1000, 3.8/1000, 2.6/1000]):
        try:
            self.setVariables(x)

            errors = self.interf.CalculateFlowsheet4(self.flowsheet)

            if errors.Count > 0:
                print("\nsomething is wrong")
                print(f"input: {x}")

                for i, error in enumerate(errors, start=1):
                    print(f"\nerror: {i}")

                    print("type:", error.GetType().FullName)
                    print("source:", error.Source)
                    print("message:", error.Message)

                    print("\nexception:")
                    print(error.ToString())

                print("\nobject errors")

                for name, obj in self.flowsheetObjects.items():
                    message = obj.ErrorMessage

                    if message:
                        print(f"{name}: {message}")

                return False

            return True

        except Exception as e:
            print("\npythonnet error?")
            print(f"variables: {x}")

            traceback.print_exc()

            if hasattr(e, "ToString"):
                print("\n.NET exception details:")
                print(e.ToString())

            raise

    def getComponents(self):
        return {
            name: {
                "molarWeight": float(compound.Molar_Weight),
                "NBP": self.getNBP(compound)
            }
            for name, compound in self.flowsheet.SelectedCompounds.items()
        }
    
    def getNBP(self, compound):
        try:
            value=compound.NBP

            if value is None:
                return None

            value=float(value)

            if not np.isfinite(value) or value <= 0:
                return None

            return value

        except (TypeError, ValueError, OverflowError):
            return None

    


