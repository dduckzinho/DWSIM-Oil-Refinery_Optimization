
def calculatePreConstraints(x, feedMolarWeight, minComponentMolarWeight):

    feedMass=x[0]*feedMolarWeight/1000

    sideMass=sum(x[3:8])
    bottomMinMass=x[2]*minComponentMolarWeight/1000

    g1=(sideMass+bottomMinMass-feedMass)/feedMass
    g2=(x[2]-x[0])/x[0]

    return [g1, g2]

def calculatePostConstraints(results):
    ...

def calculateContamScore():
    ...