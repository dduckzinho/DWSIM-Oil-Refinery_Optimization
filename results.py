
from math import isfinite
import config as c
import re

class InvalidSimulationResult(ValueError):
    pass


def _number(value, label, nonnegative=False):
    
    if value is None:
        raise InvalidSimulationResult(
            f"Missing value: {label}"
        )

    value=float(value)

    if not isfinite(value):
        raise InvalidSimulationResult(
            f"Non-finite value for {label}: {value}"
        )

    if nonnegative and value < 0:
        raise InvalidSimulationResult(
            f"Negative value for {label}: {value}"
        )

    return value


def getResults(session):
    objects=session.flowsheetObjects

    massFlows={}

    for name in c.STREAM_NAMES:
        massFlows[name]=_number(
            objects[name].GetPropertyValue("PROP_MS_2"),
            label=f"{name} mass flow",
            nonnegative=True,
        )

    reboilerDuty=_number(
        objects["reboiler_estr"].GetPropertyValue("PROP_ES_0"),
        label="reboiler duty",
    )

    condenserDuty=_number(
        objects["condenser_estr"].GetPropertyValue("PROP_ES_0"),
        label="condenser duty",
    )

    return {
        "massFlows": massFlows,
        "reboilerDuty": reboilerDuty,
        "condenserDuty": condenserDuty,
    }

def getDistillationCurveInfo(session):

    distillationInfo={}

    for stream in c.STREAM_NAMES: # each stream
        object=session.flowsheetObjects[stream]

        for utility in object.AttachedUtilities: # each utility
            if match := re.search(r"^.*_curves$", utility.Name):
                distillationInfo[utility.Name]={}

                for prop in c.CHRACTERIZATION_PROP: # each prop
                    
                    value=utility.GetPropertyValue(prop)
                    unit=utility.GetPropertyUnits(prop)

                    distillationInfo[utility.Name][prop]=(value, unit)

    print(distillationInfo)
    return distillationInfo
