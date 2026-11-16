import numpy as np
import config as c
from pymoo.core.problem import ElementwiseProblem

from constraints import calculatePreConstraints, calculatePostConstraints, calculateContamScore
from objectives import calculateObjs
from results import getResults

class DistillationProblem(ElementwiseProblem):

    def __init__(self, session):

        self.session=session

        feed=session.flowsheetObjects["bacalhau3"]
        print(feed)
        print(dir(feed))
        self.feedMolarWeight=float(feed.GetPropertyValue("PROP_MS_6"))

        components=session.getComponents()

        self.minComponentMolarWeight=min(
            component["molarWeight"]
            for component in components.values()
        )

        maxMassFlow=(
            c.MAX_FEED_MOLAR_FLOW * self.feedMolarWeight / 1000
        )

        super().__init__(
            n_var=8,
            n_obj=c.N_OBJECTIVES,
            n_ieq_constr=1,

            # feedMolarFlow, refluxRatio, bottomProductMolarFlow, hNaphthaLF, keroseneLF, lDieselLF, hDieselLF, agoLF
            xl=np.array([
                1, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
            ]),

            xu=np.array([
                c.MAX_FEED_MOLAR_FLOW,
                10.0,
                c.MAX_FEED_MOLAR_FLOW,
                *([maxMassFlow]*5)
            ])
        )

    def _evaluate(self, x, out, *args, **kwargs):

        preG=calculatePreConstraints(
            x,
            self.feedMolarWeight,
            self.minComponentMolarWeight,
        )

        if any(g > 0 for g in preG):
            out["F"]=[c.PENALTY]*c.N_OBJECTIVES
            out["G"]=preG+[0.0]*c.N_POST_CONSTRAINTS
            return

        self.session.setVariables(x)

        if not self.session.simulate():
            out["F"]=[c.PENALTY]*c.N_OBJECTIVES
            out["G"]=preG+[1.0]*c.N_POST_CONSTRAINTS
            return

        results=getResults(self.session)

        out["F"]=calculateObjs(results)
        out["G"]=preG+calculatePostConstraints(results)