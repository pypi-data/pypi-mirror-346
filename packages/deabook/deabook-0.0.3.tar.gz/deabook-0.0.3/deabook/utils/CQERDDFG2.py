# import dependencies
from pyomo.environ import ConcreteModel, Set, Var, Objective, minimize, Constraint, log
from pyomo.core.expr.numvalue import NumericValue
import numpy as np
import pandas as pd
from ..constant import CET_ADDI, FUN_PROD, FUN_COST, RTS_CRS, RTS_VRS, OPT_DEFAULT, OPT_LOCAL
from .tools import optimize_model
from . import CQERDDFZG1,CQERDDFZG2,CQERDDFG1

class CQRDDFG2(CQERDDFZG2.CQRDDFZG2,CQERDDFG1.CQRDDFG1,CQERDDFZG1.CQRDDFZG1):
    """initial Group-VC-added weakCNLSDDFZ (weakCNLSDDFZ+G) model
    """

    def __init__(self, y, x, b, tau, cutactive,active, gy=[1], gx=[1], gb=[1], fun=FUN_PROD, rts=RTS_VRS):
        """CNLSDDFZ+G model

        Args:
            y (float): output variable.
            x (float): input variables.
            b (float, optional): undersiable variables.
            tau (float): quantile.
            cutactive (float, optional): active concavity constraint.
            gy (list, optional): output directional vector. Defaults to [1].
            gx (list, optional): input directional vector. Defaults to [1].
            gb (list, optional): undesirable output directional vector. Defaults to [1].
            fun (String, optional): FUN_PROD (production frontier) or FUN_COST (cost frontier). Defaults to FUN_PROD.
            rts (String, optional): RTS_VRS (variable returns to scale) or RTS_CRS (constant returns to scale). Defaults to RTS_VRS.
        """
        # TODO(error/warning handling): Check the configuration of the model exist
        self.x,self.y,self.b = x, y, b
        self.gy, self.gx, self.gb = gy,gx,gb
        self.tau = tau

        self.fun = fun
        self.rts = rts

        self.cutactive = cutactive
        self.active = active

        # Initialize the CNLS model
        self.__model__ = ConcreteModel()

        # Initialize the sets
        self.__model__.I = Set(initialize=range(len(self.y)))
        self.__model__.J = Set(initialize=range(len(self.x[0])))
        self.__model__.K = Set(initialize=range(len(self.y[0])))


        if type(self.b) != type(None):
            self.__model__.L = Set(initialize=range(len(self.b[0])))
            self.__model__.delta = Var(
                self.__model__.I, self.__model__.L, bounds=(0.0, None), doc='delta')

        # Initialize the variables
        self.__model__.alpha = Var(self.__model__.I, doc='alpha')
        self.__model__.beta = Var(self.__model__.I,
                                  self.__model__.J,
                                  bounds=(0.0, None),
                                  doc='beta')
        self.__model__.gamma = Var(self.__model__.I,
                                  self.__model__.K,
                                  bounds=(0.0, None),
                                  doc='gamma')


        self.__model__.epsilon_plus = Var(
            self.__model__.I, bounds=(0.0, None), doc='positive error term')
        self.__model__.epsilon_minus = Var(
            self.__model__.I, bounds=(0.0, None), doc='negative error term')

        self.__model__.frontier = Var(self.__model__.I,
                                      bounds=(0.0, None),
                                      doc='estimated frontier')

        # Setup the objective function and constraints
        self.__model__.objective = Objective(rule=self._CQRDDFZG1__objective_rule(),
                                             sense=minimize,
                                             doc='objective function')
        self.__model__.regression_rule = Constraint(self.__model__.I,
                                                    rule=self._CQRDDFG1__regression_rule(),
                                                    doc='regression equation')
        self.__model__.translation_rule = Constraint(self.__model__.I,
                                                     rule=self._CQRDDFZG1__translation_property(),
                                                     doc='translation property')

        self.__model__.afriat_rule = Constraint(self.__model__.I,
                                                rule=self._CQRDDFZG1__afriat_rule(),
                                                doc='elementary Afriat approach')
        self.__model__.disposability_rule = Constraint(self.__model__.I,
                                                        rule=self._CQRDDFZG1__disposability_rule(),
                                                        doc='elementary weak disposibility')
        self.__model__.sweet_rule = Constraint(self.__model__.I,
                                               self.__model__.I,
                                               rule=self._CQRDDFZG1__sweet_rule(),
                                               doc='sweet spot approach')
        self.__model__.sweet_rule2 = Constraint(self.__model__.I,
                                               self.__model__.I,
                                               rule=self._CQRDDFZG2__sweet_rule2(),
                                               doc='sweet spot-2 approach')

        # Optimize model
        self.optimization_status = 0
        self.problem_status = 0



class CERDDFG2(CQRDDFG2):
    """initial Group-VC-added CERZ (CERZ+G) model
    """

    def __init__(self, y, x, b, tau, cutactive, active, gy=[1], gx=[1], gb=[1], fun=FUN_PROD, rts=RTS_VRS):
        """CERZ+G model

        Args:
            y (float): output variable.
            x (float): input variables.
            b (float, optional): undersiable variables
            tau (float): expectile.
            cutactive (float): active concavity constraint.
            cet (String, optional): CET_ADDI (additive composite error term) or CET_MULT (multiplicative composite error term). Defaults to CET_ADDI.
            fun (String, optional): FUN_PROD (production frontier) or FUN_COST (cost frontier). Defaults to FUN_PROD.
            rts (String, optional): RTS_VRS (variable returns to scale) or RTS_CRS (constant returns to scale). Defaults to RTS_VRS.
        """
        super().__init__(y, x, b, tau, cutactive,active, gy, gx, gb, fun, rts)
        self.__model__.objective.deactivate()
        self.__model__.squared_objective = Objective(
            rule=self.__squared_objective_rule(), sense=minimize, doc='squared objective rule')

    def __squared_objective_rule(self):
        def squared_objective_rule(model):
            return (1 - self.tau) * sum(model.epsilon_plus[i] ** 2 for i in model.I) \
                + self.tau * sum(model.epsilon_minus[i] ** 2 for i in model.I)

        return squared_objective_rule

