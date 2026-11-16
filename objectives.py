
def calculateObjs(results):
    massFlows=results["massFlows"]

    sumDesiredProduct=(
        massFlows["top"]
        + massFlows["h_naphtha"]
        + massFlows["kerosene"]
        + massFlows["l_diesel"]
        + massFlows["h_diesel"]
        + massFlows["ago"]
    )

    totalThermalDuty=(
        abs(results["reboilerDuty"])
        + abs(results["condenserDuty"])
    )

    return [-sumDesiredProduct, totalThermalDuty]