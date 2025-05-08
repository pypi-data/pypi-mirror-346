# import dependencies
from pyomo.environ import ConcreteModel, Set, Var, Objective, minimize, Constraint, log
from pyomo.core.expr.numvalue import NumericValue
import numpy as np
import pandas as pd
from ..constant import CET_ADDI, FUN_PROD, FUN_COST, RTS_CRS, RTS_VRS, OPT_DEFAULT, OPT_LOCAL
from .tools import optimize_model


class weakCQRDDFZG1:
    """initial Group-VC-added weakCNLSDDFZ (weakCNLSDDFZ+G) model
    """

    def __init__(self, y, x, b, z, tau, cutactive,gy=[1], gx=[1], gb=[1], fun=FUN_PROD, rts=RTS_VRS):
        """CNLSDDFZ+G model

        Args:
            y (float): output variable.
            x (float): input variables.
            b (float): undersiable variables.
            z (float): Contextual variable(s). Defaults to None.
            tau (float): quantile.
            cutactive (float, optional): active concavity constraint.
            gy (list, optional): output directional vector. Defaults to [1].
            gx (list, optional): input directional vector. Defaults to [1].
            gb (list, optional): undesirable output directional vector. Defaults to [1].
            fun (String, optional): FUN_PROD (production frontier) or FUN_COST (cost frontier). Defaults to FUN_PROD.
            rts (String, optional): RTS_VRS (variable returns to scale) or RTS_CRS (constant returns to scale). Defaults to RTS_VRS.
        """
        # TODO(error/warning handling): Check the configuration of the model exist
        self.x,self.y,self.b,self.z = x, y, b, z
        self.gy, self.gx, self.gb = gy,gx,gb
        self.tau = tau

        self.fun = fun
        self.rts = rts

        self.cutactive = cutactive

        # Initialize the CNLS model
        self.__model__ = ConcreteModel()

        # Initialize the sets
        self.__model__.I = Set(initialize=range(len(self.y)))
        self.__model__.J = Set(initialize=range(len(self.x[0])))
        self.__model__.K = Set(initialize=range(len(self.y[0])))
        self.__model__.L = Set(initialize=range(len(self.b[0])))

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
        self.__model__.delta = Var(self.__model__.I,
                                   self.__model__.L,
                                   bounds=(0.0, None),
                                   doc='delta')

        # Initialize the set of z
        self.__model__.M = Set(initialize=range(len(self.z[0])))
        # Initialize the variables for z variable
        self.__model__.lamda = Var(self.__model__.M, doc='z coefficient')

        self.__model__.epsilon_plus = Var(
            self.__model__.I, bounds=(0.0, None), doc='positive error term')
        self.__model__.epsilon_minus = Var(
            self.__model__.I, bounds=(0.0, None), doc='negative error term')

        self.__model__.frontier = Var(self.__model__.I,
                                      bounds=(0.0, None),
                                      doc='estimated frontier')

        # Setup the objective function and constraints
        self.__model__.objective = Objective(rule=self.__objective_rule(),
                                             sense=minimize,
                                             doc='objective function')
        self.__model__.regression_rule = Constraint(self.__model__.I,
                                                    rule=self.__regression_rule(),
                                                    doc='regression equation')
        self.__model__.translation_rule = Constraint(self.__model__.I,
                                                     rule=self.__translation_property(),
                                                     doc='translation property')

        self.__model__.afriat_rule = Constraint(self.__model__.I,
                                                rule=self.__afriat_rule(),
                                                doc='elementary Afriat approach')
        self.__model__.disposability_rule = Constraint(self.__model__.I,
                                                        rule=self.__disposability_rule(),
                                                        doc='elementary weak disposibility')
        self.__model__.sweet_rule = Constraint(self.__model__.I,
                                               self.__model__.I,
                                               rule=self.__sweet_rule(),
                                               doc='sweet spot approach')

        # Optimize model
        self.optimization_status = 0
        self.problem_status = 0

    def optimize(self, email=OPT_LOCAL, solver=OPT_DEFAULT):
        """Optimize the function by requested method

        Args:
            email (string): The email address for remote optimization. It will optimize locally if OPT_LOCAL is given.
            solver (string): The solver chosen for optimization. It will optimize with default solver if OPT_DEFAULT is given.
        """
        # TODO(error/warning handling): Check problem status after optimization
        self.problem_status, self.optimization_status = optimize_model(
            self.__model__, email, CET_ADDI, solver)

    def __objective_rule(self):
        """Return the proper objective function"""

        def objective_rule(model):
            return (1 - self.tau) * sum(model.epsilon_plus[i] for i in model.I) \
                + self.tau * sum(model.epsilon_minus[i] for i in model.I)
        return objective_rule

    def __regression_rule(self):
        """Return the proper regression constraint"""
        if self.rts == RTS_VRS:
            def regression_rule(model, i):
                return sum(model.gamma[i, k] * self.y[i][k] for k in model.K) \
                    == model.alpha[i] \
                    + sum(model.beta[i, j] * self.x[i][j] for j in model.J) \
                    + sum(model.delta[i, l] * self.b[i][l] for l in model.L) \
                    - sum(model.lamda[m] * self.z[i][m] for m in model.M) \
                    - model.epsilon_minus[i] + model.epsilon_plus[i]

            return regression_rule


        elif self.rts == RTS_CRS:
            def regression_rule(model, i):
                return sum(model.gamma[i, k] * self.y[i][k] for k in model.K) \
                    == sum(model.beta[i, j] * self.x[i][j] for j in model.J) \
                    + sum(model.delta[i, l] * self.b[i][l] for l in model.L) \
                    - sum(model.lamda[m] * self.z[i][m] for m in model.M) \
                    - model.epsilon_minus[i] + model.epsilon_plus[i]

            return regression_rule

        raise ValueError("Undefined model parameters.")

    def __translation_property(self):
        """Return the proper translation property"""
        def translation_rule(model, i):
            return sum(model.beta[i, j] * self.gx[j] for j in model.J) \
                + sum(model.gamma[i, k] * self.gy[k] for k in model.K) \
                + sum(model.delta[i, l] * self.gb[l] for l in model.L) == 1

        return translation_rule

    def __afriat_rule(self):
        """Return the proper elementary Afriat approach constraint"""
        if self.fun == FUN_PROD:
            __operator = NumericValue.__le__
        elif self.fun == FUN_COST:
            __operator = NumericValue.__ge__

        if self.rts == RTS_VRS:

            def afriat_rule(model, i):
                return __operator(
                    model.alpha[i] + sum(model.beta[i, j] * self.x[i][j]for j in model.J) \
                                   + sum(model.delta[i, l] * self.b[i][l] for l in model.L) \
                                    - sum(model.gamma[i, k] * self.y[i][k] for k in model.K),
                    model.alpha[self.__model__.I.nextw(i)] \
                           + sum(model.beta[self.__model__.I.nextw(i), j] * self.x[i][j]for j in model.J) \
                             + sum(model.delta[self.__model__.I.nextw(i), l] * self.b[i][l] for l in model.L)\
                             - sum(model.gamma[self.__model__.I.nextw(i), k] * self.y[i][k] for k in model.K))

            return afriat_rule

        elif self.rts == RTS_CRS:
            def afriat_rule(model, i):
                return __operator(sum(model.beta[i, j] * self.x[i][j]for j in model.J) \
                                   + sum(model.delta[i, l] * self.b[i][l] for l in model.L) \
                                    - sum(model.gamma[i, k] * self.y[i][k] for k in model.K),
                    sum(model.beta[self.__model__.I.nextw(i), j] * self.x[i][j]for j in model.J) \
                             + sum(model.delta[self.__model__.I.nextw(i), l] * self.b[i][l] for l in model.L)\
                             - sum(model.gamma[self.__model__.I.nextw(i), k] * self.y[i][k] for k in model.K))

            return afriat_rule
        raise ValueError("Undefined model parameters.")

    def __disposability_rule(self):
        """Return the proper elementary weak disposability constraint"""
        if self.rts == RTS_VRS:
            def disposability_rule(model, i):
                return model.alpha[self.__model__.I.nextw(i)] \
                    + sum(model.beta[self.__model__.I.nextw(i), j] * self.x[i][j] for j in model.J) >= 0
            return disposability_rule

        elif self.rts == RTS_CRS:
            def disposability_rule(model, i):
                return sum(model.beta[self.__model__.I.nextw(i), j] * self.x[i][j] for j in model.J) >= 0
            return disposability_rule
        raise ValueError("Undefined model parameters.")


    def __sweet_rule(self ):
        """Return the proper sweet spot approach constraint"""
        if self.fun == FUN_PROD:
            __operator = NumericValue.__le__
        elif self.fun == FUN_COST:
            __operator = NumericValue.__ge__

        if self.rts == RTS_VRS:

            def sweet_rule(model, i, h):
                if self.cutactive[i][h]:
                    if i == h:
                        return Constraint.Skip
                    return __operator(model.alpha[i] \
                                      + sum(model.beta[i, j] * self.x[i][j] for j in model.J) \
                                      + sum(model.delta[i, l] * self.b[i][l] for l in model.L) \
                                      - sum(model.gamma[i, k] * self.y[i][k] for k in model.K),
                                      model.alpha[h] \
                                      + sum(model.beta[h, j] * self.x[i][j] for j in model.J) \
                                      + sum(model.delta[h, l] * self.b[i][l] for l in model.L) \
                                      - sum(model.gamma[i, k] * self.y[i][k] for k in model.K) )
                return Constraint.Skip

            return sweet_rule
        elif self.rts == RTS_CRS:

            def sweet_rule(model, i, h):
                if self.cutactive[i][h]:
                    if i == h:
                        return Constraint.Skip
                    return __operator(sum(model.beta[i, j] * self.x[i][j] for j in model.J) \
                                      + sum(model.delta[i, l] * self.b[i][l] for l in model.L) \
                                      - sum(model.gamma[i, k] * self.y[i][k] for k in model.K),
                                       sum(model.beta[h, j] * self.x[i][j] for j in model.J) \
                                      + sum(model.delta[h, l] * self.b[i][l] for l in model.L) \
                                      - sum(model.gamma[i, k] * self.y[i][k] for k in model.K) )
                return Constraint.Skip

            return sweet_rule

        raise ValueError("Undefined model parameters.")

    def get_alpha(self):
        """Return alpha value by array"""
        if self.optimization_status == 0:
            self.optimize()
        alpha = list(self.__model__.alpha[:].value)
        return np.asarray(alpha)

    def get_beta(self):
        """Return beta value by array"""
        if self.optimization_status == 0:
            self.optimize()
        beta = np.asarray([i + tuple([j]) for i, j in zip(list(self.__model__.beta),
                                                          list(self.__model__.beta[:, :].value))])
        beta = pd.DataFrame(beta, columns=['Name', 'Key', 'Value'])
        beta = beta.pivot(index='Name', columns='Key', values='Value')
        return beta.to_numpy()

    def get_delta(self):
        """Return delta value by array"""
        if self.optimization_status == 0:
            self.optimize()
        delta = np.asarray([i + tuple([j]) for i, j in zip(list(self.__model__.delta),
                                                           list(self.__model__.delta[:, :].value))])
        delta = pd.DataFrame(delta, columns=['Name', 'Key', 'Value'])
        delta = delta.pivot(index='Name', columns='Key', values='Value')
        return delta.to_numpy()

    def get_gamma(self):
        """Return delta value by array"""
        if self.optimization_status == 0:
            self.optimize()
        gamma = np.asarray([i + tuple([j]) for i, j in zip(list(self.__model__.gamma),
                                                           list(self.__model__.gamma[:, :].value))])
        gamma = pd.DataFrame(gamma, columns=['Name', 'Key', 'Value'])
        gamma = gamma.pivot(index='Name', columns='Key', values='Value')
        return gamma.to_numpy()


class weakCERDDFZG1(weakCQRDDFZG1):
    """initial Group-VC-added CERZ (CERZ+G) model
    """

    def __init__(self, y, x, b, z, tau, cutactive, gy=[1], gx=[1], gb=[1], fun=FUN_PROD, rts=RTS_VRS):
        """CERZ+G model

        Args:
            y (float): output variable.
            x (float): input variables.
            b (float): undersiable variables
            z (float, optional): Contextual variable(s). Defaults to None.
            tau (float): expectile.
            cutactive (float): active concavity constraint.
            cet (String, optional): CET_ADDI (additive composite error term) or CET_MULT (multiplicative composite error term). Defaults to CET_ADDI.
            fun (String, optional): FUN_PROD (production frontier) or FUN_COST (cost frontier). Defaults to FUN_PROD.
            rts (String, optional): RTS_VRS (variable returns to scale) or RTS_CRS (constant returns to scale). Defaults to RTS_VRS.
        """
        super().__init__(y, x, b, z, tau, cutactive, gy, gx, gb, fun, rts)
        self.__model__.objective.deactivate()
        self.__model__.squared_objective = Objective(
            rule=self.__squared_objective_rule(), sense=minimize, doc='squared objective rule')

    def __squared_objective_rule(self):
        def squared_objective_rule(model):
            return (1 - self.tau) * sum(model.epsilon_plus[i] ** 2 for i in model.I) \
                + self.tau * sum(model.epsilon_minus[i] ** 2 for i in model.I)

        return squared_objective_rule

