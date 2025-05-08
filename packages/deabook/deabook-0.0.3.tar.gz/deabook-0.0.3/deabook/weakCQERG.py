# import dependencies
import numpy as np
import pandas as pd
from .utils import weakCQERG1, weakCQERG2, weakCQERZG1, weakCQERZG2, sweet, tools, interpolation
from .constant import CET_ADDI, CET_MULT, FUN_PROD, FUN_COST, RTS_CRS, RTS_VRS, OPT_LOCAL, OPT_DEFAULT
import time


class weakCQRG:
    """Convex quantile regression (CQR) with Genetic algorithm and weak
    """

    def __init__(self, y, x, b, tau, z=None, cet=CET_ADDI, fun=FUN_PROD, rts=RTS_VRS):
        """CQRG model

        Args:
            y (ndarray): output variable.
            x (ndarray): input variables.
            b (ndarray): undersiable variables.
            tau (float): quantile.
            z (float, optional): Contextual variable(s). Defaults to None.
            cet (String, optional): CET_ADDI (additive composite error term) or CET_MULT (multiplicative composite error term). Defaults to CET_ADDI.
            fun (String, optional): FUN_PROD (production frontier) or FUN_COST (cost frontier). Defaults to FUN_PROD.
            rts (String, optional): RTS_VRS (variable returns to scale) or RTS_CRS (constant returns to scale). Defaults to RTS_VRS.
        """
        # TODO(error/warning handling): Check the configuration of the model exist
        self.cutactive = sweet.sweet(np.column_stack((x,b)))
        self.y, self.x, self.b, self.z = tools.assert_valid_wp_data(y, x, b, z)

        self.tau = tau
        self.cet = cet
        self.fun = fun
        self.rts = rts

        # active (added) violated concavity constraint by iterative procedure
        self.active = np.zeros((len(x), len(x)))
        # violated concavity constraint
        self.active2 = np.zeros((len(x), len(x)))

        # active (added) violated concavity constraint for weak disposbility constrains by iterative procedure
        self.activeweak = np.zeros((len(x), len(x)))
        # violated concavity constraint for weak disposbility constrains
        self.activeweak2 = np.zeros((len(x), len(x)))

        # Optimize model
        self.optimization_status = 0
        self.problem_status = 0

    def optimize(self, email=OPT_LOCAL, solver=OPT_DEFAULT):
        """Optimize the function by requested method"""
        # TODO(error/warning handling): Check problem status after optimization
        self.t0 = time.time()
        if type(self.z) != type(None):
            model1 = weakCQERZG1.weakCQRZG1(
                self.y, self.x, self.b, self.z, self.tau, self.cutactive, self.cet, self.fun, self.rts)
        else:
            model1 = weakCQERG1.weakCQRG1(
                self.y, self.x, self.b, self.tau, self.cutactive, self.cet, self.fun, self.rts)
        model1.optimize(email, solver)
        self.alpha = model1.get_alpha()
        self.beta = model1.get_beta()
        self.delta = model1.get_delta()
        self.__model__ = model1.__model__

        self.count = 0
        while self.__convergence_test(self.alpha, self.beta, self.delta) > 0.0001 \
                or self.__convergence_test_weak(self.alpha, self.beta, self.delta) > 0.0001:
            if type(self.z) != type(None):
                model2 = weakCQERZG2.weakCQRZG2(
                    self.y, self.x, self.b, self.z, self.tau, self.cutactive,self.active,self.activeweak,
                                self.cet, self.fun, self.rts)
            else:
                model2 = weakCQERG2.weakCQRG2(
                    self.y, self.x, self.b, self.tau, self.cutactive, self.active, self.activeweak,
                                self.cet, self.fun, self.rts)
            model2.optimize(email, solver)
            self.alpha = model2.get_alpha()
            self.beta = model2.get_beta()
            self.delta = model2.get_delta()

            # TODO: Replace print with log system
            # print("Genetic Algorithm Convergence : %8f" %
            #       (self.__convergence_test(self.alpha, self.beta)))
            self.__model__ = model2.__model__
            self.count += 1
        self.optimization_status = 1
        self.tt = time.time() - self.t0

    def __convergence_test(self, alpha, beta,delta):
        x = np.asarray(self.x)
        b = np.asarray(self.b)
        activetmp1 = 0.0
        if self.rts == RTS_VRS and self.fun == FUN_PROD:
        # go into the loop
            for i in range(len(x)):
                activetmp = 0.0
                # go into the sub-loop and find the violated concavity constraints
                for j in range(len(x)):
                    self.active2[i, j] = alpha[i] \
                        + np.sum(beta[i, :] * x[i, :]) + np.sum(delta[i, :] * b[i, :]) - \
                        alpha[j] - np.sum(beta[j, :] * x[i, :]) - np.sum(delta[j, :] * b[i, :])

                    if self.active2[i, j] > activetmp:
                        activetmp = self.active2[i, j]

            # find the maximal violated constraint in sub-loop and added into the active matrix
                for j in range(len(x)):
                    if self.active2[i, j] >= activetmp and activetmp > 0:
                        self.active[i, j] = 1
                if activetmp > activetmp1:
                    activetmp1 = activetmp


        elif self.rts == RTS_VRS and self.fun == FUN_COST:
        # go into the loop
            for i in range(len(x)):
                activetmp = 0.0
                # go into the sub-loop and find the violated concavity constraints
                for j in range(len(x)):
                    self.active2[i, j] = - alpha[i] - np.sum(beta[i, :] * x[i, :]) \
                                         - np.sum(delta[i, :] * b[i, :])+ alpha[j] \
                                         + np.sum(beta[j, :] * x[i, :]) + np.sum(delta[j, :] * b[i, :])

                    if self.active2[i, j] > activetmp:
                        activetmp = self.active2[i, j]

            # find the maximal violated constraint in sub-loop and added into the active matrix
                for j in range(len(x)):
                    if self.active2[i, j] >= activetmp and activetmp > 0:
                        self.active[i, j] = 1
                if activetmp > activetmp1:
                    activetmp1 = activetmp


        elif self.rts == RTS_CRS and self.fun == FUN_PROD:
        # go into the loop
            for i in range(len(x)):
                activetmp = 0.0
                # go into the sub-loop and find the violated concavity constraints
                for j in range(len(x)):
                    self.active2[i, j] = np.sum(beta[i, :] * x[i, :]) + np.sum(delta[i, :] * b[i, :]) \
                            - np.sum(beta[j, :] * x[i, :]) - np.sum(delta[j, :] * b[i, :])

                    if self.active2[i, j] > activetmp:
                        activetmp = self.active2[i, j]

            # find the maximal violated constraint in sub-loop and added into the active matrix
                for j in range(len(x)):
                    if self.active2[i, j] >= activetmp and activetmp > 0:
                        self.active[i, j] = 1
                if activetmp > activetmp1:
                    activetmp1 = activetmp

        elif self.rts == RTS_CRS and self.fun == FUN_COST:
        # go into the loop
            for i in range(len(x)):
                activetmp = 0.0
                # go into the sub-loop and find the violated concavity constraints
                for j in range(len(x)):
                    self.active2[i, j] = - np.sum(beta[i, :] * x[i, :]) - np.sum(delta[i, :] * b[i, :]) \
                            + np.sum(beta[j, :] * x[i, :]) + np.sum(delta[j, :] * b[i, :])
                    if self.active2[i, j] > activetmp:
                        activetmp = self.active2[i, j]

            # find the maximal violated constraint in sub-loop and added into the active matrix
                for j in range(len(x)):
                    if self.active2[i, j] >= activetmp and activetmp > 0:
                        self.active[i, j] = 1
                if activetmp > activetmp1:
                    activetmp1 = activetmp
        return activetmp


    def __convergence_test_weak(self, alpha, beta,delta):
        x = np.asarray(self.x)
        b = np.asarray(self.b)
        activetmp1 = 0.0
        if self.rts == RTS_VRS and self.fun == FUN_PROD:
        # go into the loop
            for i in range(len(x)):
                activetmp = 0.0
                # go into the sub-loop and find the violated concavity constraints
                for j in range(len(x)):
                    self.activeweak2[i, j] = - alpha[j] - np.sum(beta[j, :] * x[i, :])

                    if self.activeweak2[i, j] > activetmp:
                        activetmp = self.activeweak2[i, j]

            # find the maximal violated constraint in sub-loop and added into the active matrix
                for j in range(len(x)):
                    if self.activeweak2[i, j] >= activetmp and activetmp > 0:
                        self.activeweak[i, j] = 1
                if activetmp > activetmp1:
                    activetmp1 = activetmp

        elif self.rts == RTS_VRS and self.fun == FUN_COST:
        # go into the loop
            for i in range(len(x)):
                activetmp = 0.0
                # go into the sub-loop and find the violated concavity constraints
                for j in range(len(x)):
                    self.activeweak2[i, j] = alpha[j] + np.sum(beta[j, :] * x[i, :])

                    if self.activeweak2[i, j] > activetmp:
                        activetmp = self.activeweak2[i, j]

            # find the maximal violated constraint in sub-loop and added into the active matrix
                for j in range(len(x)):
                    if self.activeweak2[i, j] >= activetmp and activetmp > 0:
                        self.activeweak[i, j] = 1
                if activetmp > activetmp1:
                    activetmp1 = activetmp

        elif self.rts == RTS_CRS and self.fun == FUN_PROD:
        # go into the loop
            for i in range(len(x)):
                activetmp = 0.0
                # go into the sub-loop and find the violated concavity constraints
                for j in range(len(x)):
                    self.activeweak2[i, j] = - np.sum(beta[j, :] * x[i, :])

                    if self.activeweak2[i, j] > activetmp:
                        activetmp = self.activeweak2[i, j]

            # find the maximal violated constraint in sub-loop and added into the active matrix
                for j in range(len(x)):
                    if self.activeweak2[i, j] >= activetmp and activetmp > 0:
                        self.activeweak[i, j] = 1
                if activetmp > activetmp1:
                    activetmp1 = activetmp

        elif self.rts == RTS_CRS and self.fun == FUN_COST:
        # go into the loop
            for i in range(len(x)):
                activetmp = 0.0
                # go into the sub-loop and find the violated concavity constraints
                for j in range(len(x)):
                    self.activeweak2[i, j] = np.sum(beta[j, :] * x[i, :])
                    if self.activeweak2[i, j] > activetmp:
                        activetmp = self.activeweak2[i, j]

            # find the maximal violated constraint in sub-loop and added into the active matrix
                for j in range(len(x)):
                    if self.activeweak2[i, j] >= activetmp and activetmp > 0:
                        self.activeweak[i, j] = 1
                if activetmp > activetmp1:
                    activetmp1 = activetmp
        return activetmp


    def display_status(self):
        """Display the status of problem"""
        print(self.optimization_status)

    def display_alpha(self):
        """Display alpha value"""
        tools.assert_optimized(self.optimization_status)
        tools.assert_various_return_to_scale(self.rts)
        self.__model__.alpha.display()

    def display_beta(self):
        """Display beta value"""
        tools.assert_optimized(self.optimization_status)
        self.__model__.beta.display()

    def display_delta(self):
        """Display beta value"""
        tools.assert_optimized(self.optimization_status)
        self.__model__.delta.display()

    def display_lamda(self):
        """Display lamda value"""
        tools.assert_optimized(self.optimization_status)
        tools.assert_contextual_variable(self.z)
        self.__model__.lamda.display()

    # def display_residual(self):
    #     """Dispaly residual value"""
    #     tools.assert_optimized(self.optimization_status)
    #     self.__model__.epsilon.display()

    def display_positive_residual(self):
        """Dispaly positive residual value"""
        tools.assert_optimized(self.optimization_status)
        self.__model__.epsilon_plus.display()

    def display_negative_residual(self):
        """Dispaly negative residual value"""
        tools.assert_optimized(self.optimization_status)
        self.__model__.epsilon_minus.display()

    def get_status(self):
        """Return status"""
        return self.optimization_status

    def get_alpha(self):
        """Return alpha value by array"""
        tools.assert_optimized(self.optimization_status)
        tools.assert_various_return_to_scale(self.rts)
        alpha = list(self.__model__.alpha[:].value)
        return np.asarray(alpha)

    def get_beta(self):
        """Return beta value by array"""
        tools.assert_optimized(self.optimization_status)
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

    def get_residual(self):
        """Return residual value by array"""
        tools.assert_optimized(self.optimization_status)
        residual = list(self.__model__.epsilon_minus[:].value-self.__model__.epsilon_plus[:].value)
        return np.asarray(residual)

    def get_positive_residual(self):
        """Return positive residual value by array"""
        tools.assert_optimized(self.optimization_status)
        residual_plus = list(self.__model__.epsilon_plus[:].value)
        return np.asarray(residual_plus)

    def get_negative_residual(self):
        """Return negative residual value by array"""
        tools.assert_optimized(self.optimization_status)
        residual_minus = list(self.__model__.epsilon_minus[:].value)
        return np.asarray(residual_minus)

    def get_lamda(self):
        """Return beta value by array"""
        tools.assert_optimized(self.optimization_status)
        tools.assert_contextual_variable(self.z)
        lamda = list(self.__model__.lamda[:].value)
        return np.asarray(lamda)

    def get_frontier(self):
        """Return estimated frontier value by array"""
        tools.assert_optimized(self.optimization_status)
        if self.cet == CET_MULT and type(self.z) == type(None):
            frontier = np.asarray(list(self.__model__.frontier[:].value))+1
        elif self.cet == CET_MULT and type(self.z) != type(None):
            frontier = list(np.divide(self.y, np.exp(
                - self.get_residual() - self.get_lamda()*np.asarray(self.z)[:, 0])) - 1)
        elif self.cet == CET_ADDI:
            frontier = np.asarray(self.y) + self.get_residual()
        return np.asarray(frontier)

    def get_totalconstr(self):
        """Return the number of total constraints"""
        tools.assert_optimized(self.optimization_status)
        activeconstr = np.sum(self.active) - np.trace(self.active)
        cutactiveconstr = np.sum(self.cutactive) - np.trace(self.cutactive)
        totalconstr = activeconstr + cutactiveconstr + 2 * len(self.active) + 1
        return totalconstr

    def get_runningtime(self):
        """Return the running time"""
        tools.assert_optimized(self.optimization_status)
        return self.tt

    def get_blocks(self):
        """Return the number of blocks"""
        tools.assert_optimized(self.optimization_status)
        return self.count

    def get_predict(self, x_test):
        """Return the estimated function in testing sample"""
        tools.assert_optimized(self.optimization_status)
        return interpolation.interpolation(self.get_alpha(), self.get_beta(), x_test, fun=self.fun)
    

class weakCERG(weakCQRG):
    """Convex expectile regression (CER) with Genetic algorithm
    """

    def __init__(self, y, x, b, tau, z=None, cet=CET_ADDI, fun=FUN_PROD, rts=RTS_VRS):
        """CERG model

        Args:
            y (float): output variable. 
            x (float): input variables.
            b (float): undersiable variables.
            tau (float): quantile.
            z (float, optional): Contextual variable(s). Defaults to None.
            cet (String, optional): CET_ADDI (additive composite error term) or CET_MULT (multiplicative composite error term). Defaults to CET_ADDI.
            fun (String, optional): FUN_PROD (production frontier) or FUN_COST (cost frontier). Defaults to FUN_PROD.
            rts (String, optional): RTS_VRS (variable returns to scale) or RTS_CRS (constant returns to scale). Defaults to RTS_VRS.
        """
        # TODO(error/warning handling): Check the configuration of the model exist
        self.cutactive = sweet.sweet(x)
        self.y, self.x, self.b, self.z = tools.assert_valid_wp_data(y, x, b, z)

        self.tau = tau
        self.cet = cet
        self.fun = fun
        self.rts = rts

        # active (added) violated concavity constraint by iterative procedure
        self.active = np.zeros((len(x), len(x)))
        # violated concavity constraint
        self.active2 = np.zeros((len(x), len(x)))

        # active (added) violated concavity constraint for weak disposbility constrains by iterative procedure
        self.activeweak = np.zeros((len(x), len(x)))
        # violated concavity constraint for weak disposbility constrains
        self.activeweak2 = np.zeros((len(x), len(x)))

        # Optimize model
        self.optimization_status = 0
        self.problem_status = 0

    def optimize(self, email=OPT_LOCAL, solver=OPT_DEFAULT):
        """Optimize the function by requested method"""
        # TODO(error/warning handling): Check problem status after optimization
        self.t0 = time.time()
        if type(self.z) != type(None):
            model1 = weakCQERZG1.weakCERZG1(
                self.y, self.x, self.b, self.z, self.tau, self.cutactive, self.cet, self.fun, self.rts)
        else:
            model1 = weakCQERG1.weakCERG1(
                self.y, self.x, self.b, self.tau, self.cutactive, self.cet, self.fun, self.rts)
        model1.optimize(email, solver)
        self.alpha = model1.get_alpha()
        self.beta = model1.get_beta()
        self.delta = model1.get_delta()
        self.__model__ = model1.__model__

        self.count = 0
        while self.__convergence_test(self.alpha, self.beta, self.delta) > 0.0001 \
                or self.__convergence_test_weak(self.alpha, self.beta, self.delta) > 0.0001:
            if type(self.z) != type(None):
                model2 = weakCQERZG2.weakCERZG2(
                    self.y, self.x, self.b, self.z, self.tau, self.cutactive,self.active,self.activeweak,
                                self.cet, self.fun, self.rts)
            else:
                model2 = weakCQERG2.weakCERG2(
                    self.y, self.x, self.b, self.tau, self.cutactive, self.active, self.activeweak,
                                self.cet, self.fun, self.rts)
            model2.optimize(email, solver)
            self.alpha = model2.get_alpha()
            self.beta = model2.get_beta()
            self.delta = model2.get_delta()

            # TODO: Replace print with log system
            # print("Genetic Algorithm Convergence : %8f" %
            #       (self.__convergence_test(self.alpha, self.beta)))
            self.__model__ = model2.__model__
            self.count += 1
        self.optimization_status = 1
        self.tt = time.time() - self.t0

    def __convergence_test(self, alpha, beta,delta):
        x = np.asarray(self.x)
        b = np.asarray(self.b)
        activetmp1 = 0.0
        if self.rts == RTS_VRS and self.fun == FUN_PROD:
        # go into the loop
            for i in range(len(x)):
                activetmp = 0.0
                # go into the sub-loop and find the violated concavity constraints
                for j in range(len(x)):
                    self.active2[i, j] = alpha[i] \
                        + np.sum(beta[i, :] * x[i, :]) + np.sum(delta[i, :] * b[i, :]) - \
                        alpha[j] - np.sum(beta[j, :] * x[i, :]) - np.sum(delta[j, :] * b[i, :])

                    if self.active2[i, j] > activetmp:
                        activetmp = self.active2[i, j]

            # find the maximal violated constraint in sub-loop and added into the active matrix
                for j in range(len(x)):
                    if self.active2[i, j] >= activetmp and activetmp > 0:
                        self.active[i, j] = 1
                if activetmp > activetmp1:
                    activetmp1 = activetmp


        elif self.rts == RTS_VRS and self.fun == FUN_COST:
        # go into the loop
            for i in range(len(x)):
                activetmp = 0.0
                # go into the sub-loop and find the violated concavity constraints
                for j in range(len(x)):
                    self.active2[i, j] = - alpha[i] - np.sum(beta[i, :] * x[i, :]) \
                                         - np.sum(delta[i, :] * b[i, :])+ alpha[j] \
                                         + np.sum(beta[j, :] * x[i, :]) + np.sum(delta[j, :] * b[i, :])

                    if self.active2[i, j] > activetmp:
                        activetmp = self.active2[i, j]

            # find the maximal violated constraint in sub-loop and added into the active matrix
                for j in range(len(x)):
                    if self.active2[i, j] >= activetmp and activetmp > 0:
                        self.active[i, j] = 1
                if activetmp > activetmp1:
                    activetmp1 = activetmp


        elif self.rts == RTS_CRS and self.fun == FUN_PROD:
        # go into the loop
            for i in range(len(x)):
                activetmp = 0.0
                # go into the sub-loop and find the violated concavity constraints
                for j in range(len(x)):
                    self.active2[i, j] = np.sum(beta[i, :] * x[i, :]) + np.sum(delta[i, :] * b[i, :]) \
                            - np.sum(beta[j, :] * x[i, :]) - np.sum(delta[j, :] * b[i, :])

                    if self.active2[i, j] > activetmp:
                        activetmp = self.active2[i, j]

            # find the maximal violated constraint in sub-loop and added into the active matrix
                for j in range(len(x)):
                    if self.active2[i, j] >= activetmp and activetmp > 0:
                        self.active[i, j] = 1
                if activetmp > activetmp1:
                    activetmp1 = activetmp

        elif self.rts == RTS_CRS and self.fun == FUN_COST:
        # go into the loop
            for i in range(len(x)):
                activetmp = 0.0
                # go into the sub-loop and find the violated concavity constraints
                for j in range(len(x)):
                    self.active2[i, j] = - np.sum(beta[i, :] * x[i, :]) - np.sum(delta[i, :] * b[i, :]) \
                            + np.sum(beta[j, :] * x[i, :]) + np.sum(delta[j, :] * b[i, :])
                    if self.active2[i, j] > activetmp:
                        activetmp = self.active2[i, j]

            # find the maximal violated constraint in sub-loop and added into the active matrix
                for j in range(len(x)):
                    if self.active2[i, j] >= activetmp and activetmp > 0:
                        self.active[i, j] = 1
                if activetmp > activetmp1:
                    activetmp1 = activetmp
        return activetmp


    def __convergence_test_weak(self, alpha, beta,delta):
        x = np.asarray(self.x)
        b = np.asarray(self.b)
        activetmp1 = 0.0
        if self.rts == RTS_VRS and self.fun == FUN_PROD:
        # go into the loop
            for i in range(len(x)):
                activetmp = 0.0
                # go into the sub-loop and find the violated concavity constraints
                for j in range(len(x)):
                    self.activeweak2[i, j] = - alpha[j] - np.sum(beta[j, :] * x[i, :])

                    if self.activeweak2[i, j] > activetmp:
                        activetmp = self.activeweak2[i, j]

            # find the maximal violated constraint in sub-loop and added into the active matrix
                for j in range(len(x)):
                    if self.activeweak2[i, j] >= activetmp and activetmp > 0:
                        self.activeweak[i, j] = 1
                if activetmp > activetmp1:
                    activetmp1 = activetmp

        elif self.rts == RTS_VRS and self.fun == FUN_COST:
        # go into the loop
            for i in range(len(x)):
                activetmp = 0.0
                # go into the sub-loop and find the violated concavity constraints
                for j in range(len(x)):
                    self.activeweak2[i, j] = alpha[j] + np.sum(beta[j, :] * x[i, :])

                    if self.activeweak2[i, j] > activetmp:
                        activetmp = self.activeweak2[i, j]

            # find the maximal violated constraint in sub-loop and added into the active matrix
                for j in range(len(x)):
                    if self.activeweak2[i, j] >= activetmp and activetmp > 0:
                        self.activeweak[i, j] = 1
                if activetmp > activetmp1:
                    activetmp1 = activetmp

        elif self.rts == RTS_CRS and self.fun == FUN_PROD:
        # go into the loop
            for i in range(len(x)):
                activetmp = 0.0
                # go into the sub-loop and find the violated concavity constraints
                for j in range(len(x)):
                    self.activeweak2[i, j] = - np.sum(beta[j, :] * x[i, :])

                    if self.activeweak2[i, j] > activetmp:
                        activetmp = self.activeweak2[i, j]

            # find the maximal violated constraint in sub-loop and added into the active matrix
                for j in range(len(x)):
                    if self.activeweak2[i, j] >= activetmp and activetmp > 0:
                        self.activeweak[i, j] = 1
                if activetmp > activetmp1:
                    activetmp1 = activetmp

        elif self.rts == RTS_CRS and self.fun == FUN_COST:
        # go into the loop
            for i in range(len(x)):
                activetmp = 0.0
                # go into the sub-loop and find the violated concavity constraints
                for j in range(len(x)):
                    self.activeweak2[i, j] = np.sum(beta[j, :] * x[i, :])
                    if self.activeweak2[i, j] > activetmp:
                        activetmp = self.activeweak2[i, j]

            # find the maximal violated constraint in sub-loop and added into the active matrix
                for j in range(len(x)):
                    if self.activeweak2[i, j] >= activetmp and activetmp > 0:
                        self.activeweak[i, j] = 1
                if activetmp > activetmp1:
                    activetmp1 = activetmp
        return activetmp

