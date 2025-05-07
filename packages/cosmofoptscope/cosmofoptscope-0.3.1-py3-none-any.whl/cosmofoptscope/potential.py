from cosmoTransitions import generic_potential
import numpy as np
from scipy import optimize


class PotentialWrapper(generic_potential.generic_potential):
    def init(self):
        pass

    def energyDensity2(self, X, T, include_radiation=True):
        T_eps = self.T_eps
        if self.deriv_order == 2:
            dVdT = self.DVtot(X, T + T_eps)
            dVdT -= self.DVtot(X, T - T_eps)
            dVdT *= 1.0 / (2 * T_eps)
        else:
            dVdT = self.DVtot(X, T - 2 * T_eps)
            dVdT -= 8 * (self.DVtot(X, T - T_eps))
            dVdT += 8 * (self.DVtot(X, T + T_eps))
            dVdT -= self.DVtot(X, T + 2 * T_eps)
            dVdT *= 1.0 / (12 * T_eps)
        V = self.DVtot(X, T)
        #return V - T * dVdT
        return V - T * dVdT / 4

    def findTrueMin(self, T=0.0):
        def objective(x, T):
            if x <= 0:
                return 1e50
            return self.DVtot([x], T)

        bound_max = 10*self.approxZeroTMin()[0]
        result_approx = optimize.minimize_scalar(
            lambda x: objective(x, T), method='bounded', bounds=(0, bound_max), options={'xatol': 1e-6}
        )

        return result_approx.x

    def alpha(self, temp, g_star):
        fM = np.array([self.findTrueMin(T=temp)])
        energy_density = self.energyDensity2(fM, T=temp)
        inv_rho_rad = 30 / (np.pi**2 * g_star * temp**4)
        return inv_rho_rad * (-energy_density)
