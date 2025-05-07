from scipy import optimize
from scipy.integrate import quad
from scipy.interpolate import PchipInterpolator
from scipy.signal import savgol_filter
import numpy as np
import ray
from cosmoTransitions import transitionFinder, tunneling1D, pathDeformation

from potential import PotentialWrapper


def linde(S, T):
    if np.isinf(S):
        return 0
    return np.exp(-S / T) * T**4 * (S / (T * 2 * np.pi)) ** 1.5

def linde_vec(S, T):
    return np.exp(-S / T) * T**4 * (S / (T * 2 * np.pi)) ** 1.5

def calc_hubble_temp(T, g_star, Mp):
    return np.pi / (3 * Mp) * np.sqrt(g_star / 10) * T**2

def calc_decay_rate(S, T):
    return linde(S, T)

def calc_decay_rate_vec(S, T):
    return linde_vec(S, T)

def calc_dPdT(S, T, hubble_temp, g_star, Mp):
    decay_rate = calc_decay_rate_vec(S, T)
    return decay_rate / (T * hubble_temp ** 4)

class FOPTFinder:
    def __init__(
        self,
        potential: PotentialWrapper,
        Tmax,
        g_star,
        Mp,
        initialized=False,
<<<<<<< HEAD
=======
        parallel=False,
        findP_option='Linde',
        criterion_value=None,
>>>>>>> origin/main
        Tnuc=None,
        num_points=200,
        window_length=19,
    ):
        self.potential = potential
        self.Tmax = Tmax
        self.Tnuc = Tnuc
        self.num_points = num_points
        self.g_star = g_star
<<<<<<< HEAD
        self.Mp = Mp
        self.window_length = window_length
        self.cache = None
=======
        self.Mp = Mp 
        self.findP_option = findP_option
>>>>>>> origin/main

        # Initialization
        self.dST_dT_vec = None
        self.dST_dT_Tn = None
<<<<<<< HEAD
        self.T_finite = None
        self.dPdT_finite = None
=======
        self.action = None
>>>>>>> origin/main

        # - Find all transitions
        if not initialized:
            self.potential.getPhases()
            self.potential.findAllTransitions()

        # - Find the critical temperature
        tc_trans_result = self.potential.calcTcTrans()
        if tc_trans_result and len(tc_trans_result) > 0:
            self.Tcrit = tc_trans_result[0].get("Tcrit")
            print(f"Tcrit = {self.Tcrit}")
        else:
            self.Tcrit = None
            raise ValueError("No Tc found")

        # - Find T0
        self.T0 = self.potential.findT0()

        # Define start phase
        start_idx = transitionFinder.getStartPhase(
            self.potential.phases, self.potential.Vtot
        )
        self.start_phase = self.potential.phases[start_idx]

        # Find T_finite_0 (First T where S > 0) via binary search
        action_finder = ActionFinder(self.potential, self.start_phase)
        T1 = self.T0
        T2 = self.Tcrit
        T_finite_0 = None
        S1 = action_finder.findAction(T1)
        if S1 > 0 and np.isfinite(S1):
            T_finite_0 = T1
        else:
            S2 = action_finder.findAction(T2)
            if np.isinf(S2):
                find_finite = False
            else:
                find_finite = True
            while (np.isfinite(S2) and S2 > 0) or not find_finite:
                T_finite_0 = T2
                T2 = 0.5 * (T1 + T2)
                S2 = action_finder.findAction(T2)
                print(f"T1 = {T1}, T2 = {T2}")
                print(f"S1 = {S1}, S2 = {S2}")
                if not find_finite and np.isfinite(S2):
                    find_finite = True
        self.T_finite_0 = T_finite_0
        print(f"T_finite_0 = {self.T_finite_0}")

        # Find T_finite_1 (Last T where linde > 0) via binary search
        T1 = T_finite_0
        T2 = self.Tcrit
        S1 = action_finder.findAction(T1)
        S2 = action_finder.findAction(T2)
        D1 = calc_decay_rate(S1, T1)
        D2 = calc_decay_rate(S2, T2)
        print(f"S1 = {S1}, S2 = {S2}")
        print(f"D1 = {D1}, D2 = {D2}")
        if D2 > 0:
            T_finite_1 = T2
        else:
            find_finite = False
            while D1 > 0:
                T_finite_1 = T1
                T = 0.5 * (T1 + T2)
                S = action_finder.findAction(T)
                D = calc_decay_rate(S, T)
                if not find_finite and D <= 0:
                    T2 = T
                    D2 = D
                else:
                    if not find_finite:
                        find_finite = True
                    T1 = T
                    D1 = D
        self.T_finite_1 = T_finite_1
        print(f"T_finite_1 = {self.T_finite_1}")

        # Declare T_domain
        self.T_domain = np.logspace(
            np.log10(self.T_finite_0), np.log10(self.T_finite_1), self.num_points
        )
<<<<<<< HEAD
        self.S_vec = np.array([action_finder.findAction(T) for T in self.T_domain])
=======
        self.S_vec = self.findActions(self.T_domain, parallel)
        print("S: ", self.S_vec)
>>>>>>> origin/main
        self.S_fn = PchipInterpolator(self.T_domain, self.S_vec)
        self.S_over_T_fn = PchipInterpolator(self.T_domain, self.S_vec / self.T_domain)

        self.decay_rate = calc_decay_rate_vec(self.S_vec, self.T_domain)
        self.Hubble_vec = calc_hubble_temp(self.T_domain, self.g_star, self.Mp)
        self.dPdT_vec = calc_dPdT(self.S_vec, self.T_domain, self.Hubble_vec, self.g_star, self.Mp)
        
        log_dPdT_vec = np.log10(self.dPdT_vec)
        log_dPdT_fn = PchipInterpolator(self.T_domain, log_dPdT_vec)

<<<<<<< HEAD
        def integral(t):
            if t >= self.T_domain[-1]:
                return 0
            elif t <= self.T_domain[0]:
                if self.cache is None:
                    self.cache = quad(lambda t: np.exp(log_dPdT_fn(t)), self.T_domain[0], self.T_domain[-1])[0]
                return self.cache
            else:
                return quad(lambda t: np.exp(log_dPdT_fn(t)), t, self.T_domain[-1])[0]

        self.P_fn = integral
        self.P_vec = np.array([integral(T) for T in self.T_domain])
        print("P_vec:", self.P_vec)
=======
    def findTnuc(self, g_star=None, Mp=None):
        if self.Tnuc is not None:
            self.gradST()
            self.dST_dT_Tn = self.dST_dT(self.Tnuc)
            print("dST_dT_Tn value:", self.dST_dT_Tn)
            return self.Tnuc
        if self.criterion_value is not None:
            try:
                PT_result = transitionFinder.tunnelFromPhase(
                    self.potential.phases,
                    self.start_phase,
                    self.potential.Vtot,
                    self.potential.gradV,
                    Tmax=self.Tmax,
                    nuclCriterion=lambda S, T: S / (T + 1e-100) - self.criterion_value,
                )
                self.Tnuc = PT_result.get("Tnuc")
                if self.Tnuc is None or not np.isfinite(self.Tnuc):
                    raise ValueError("No Tnuc found")
            except Exception as e:
                print(e)
                self.Tnuc = None
        else:
            Tmin = self.T0
            
            def is_P_one(T):
                f = np.log10(self.P_fn(self.Tcrit - T))
                self.iterations.append({                    
                    'iteration': len(self.iterations),
                    'T': self.Tcrit-T,
                    'f': 10**f,
                })
                return f

            params = dict(
                xtol=1e-10,
                rtol=1e-10,
                maxiter=1000,
            )
            self.iterations=[]
            sol = optimize.root_scalar(
                is_P_one, bracket=[0, self.Tcrit - Tmin], method="brentq", **params
            )
            T_root = sol.root
            self.Tnuc_err = np.abs(self.P_fn(self.Tcrit - T_root) - 1)
            self.Tnuc = self.Tcrit - T_root
        
            self.dST_dT_Tn = self.dST_dT(self.Tnuc)

    def create_action_finder(self):
        return ActionFinder(
            potential=self.potential, start_phase=self.start_phase
        )

    def findActions(self, T_vec, parallel=False):
        finders = [self.create_action_finder() for _ in range(len(T_vec))]
        if parallel:
            actions = ray.get(
                [finder.findAction.remote(T) for finder, T in zip(finders, T_vec)]
            )
        else:
            actions = [finder.findAction(T) for finder, T in zip(finders, T_vec)]
        return np.array(actions)
>>>>>>> origin/main

    def gradST(self):
        if self.dST_dT_vec and self.dST_dT_Tn:
            pass
        else:
            dST_dT = self.S_over_T_fn.derivative()
            dST_dT_vec = dST_dT(self.T_domain)

            self.dST_dT = dST_dT
            self.dST_dT_vec = dST_dT_vec

            # For smoothing
            smoothed_data = savgol_filter(
                dST_dT_vec, self.window_length, 2, mode="mirror"
            )
            smoothed_data[-self.window_length :] = dST_dT_vec[-self.window_length :]
            self.smoothed_dST_dT_vec = smoothed_data

    def findBetas(self, smoothing=True):
        if self.dST_dT_vec is None:
            self.gradST()
        if smoothing:
            return self.smoothed_dST_dT_vec * self.T_domain
        else:
            return self.dST_dT_vec * self.T_domain

    def findTnuc(self, g_star=None, Mp=None):
        if self.Tnuc is not None:
            self.gradST()
            self.dST_dT_Tn = self.dST_dT(self.Tnuc)
            print("dST_dT_Tn value:", self.dST_dT_Tn)
            return self.Tnuc
        else:
            Tmin = self.T_domain[0]
            def is_P_one(T):
                f = self.P_fn(self.T_domain[-1] - T)
                return f - 1.0

            params = dict(
                xtol = 1e-10,
                rtol = 1e-10,
                maxiter = 100,
            )
            sol = optimize.root_scalar(
                is_P_one, bracket=[0, self.T_domain[-1] - Tmin], method="brentq", **params
            )
            T_root = sol.root
            self.Tnuc = self.T_domain[-1] - T_root
            self.Tnuc_err = np.abs(is_P_one(T_root))
            self.dST_dT_Tn = self.dST_dT(self.Tnuc)

    def report(self):
        if self.Tnuc is None:
            raise ValueError("Tnuc not found")
        if self.Tcrit is None:
            raise ValueError("Tcrit not found")
        if self.dST_dT_Tn is None:
            raise ValueError("dST_dT_Tn not found")
        self.action = self.S_fn(self.Tnuc)
<<<<<<< HEAD
        self.S_over_Tnuc = self.action / self.Tnuc
=======
        self.S_over_Tnuc = self.S_over_T_fn(self.Tnuc)
>>>>>>> origin/main
        return {
            "T0": self.T0,
            "Tnuc": self.Tnuc,
            "Tcrit": self.Tcrit,
            "S/Tnuc": self.action / self.Tnuc,
            "alpha": self.potential.alpha(self.Tnuc, self.g_star),
            "beta": self.dST_dT_Tn * self.Tnuc,
            "vev": self.potential.findTrueMin(self.Tnuc)
        }

<<<<<<< HEAD
=======
    def findDR(self, option=None):
        if option is None:
            option = self.findP_option

        if len(self.S_vec) < 3:
            raise ValueError("Not enough actions to spline")
        result = np.zeros(len(self.T_domain))

        for i, (S, T) in enumerate(zip(self.S_vec, self.T_domain)):
            if option == 'Linde':
                result[i] = np.exp(-S / T) * T**4 * (S / (T * 2 * np.pi)) ** 1.5
            elif option == 'Anderson':
                result[i] = np.exp(-S / T) * T**4 

        self.DR_vec = result
>>>>>>> origin/main

        


# ┌──────────────────────────────────────────────────────────┐
#  Action Finder
# └──────────────────────────────────────────────────────────┘
class ActionFinder:
    def __init__(self, potential, start_phase):
        self.potential = potential
        self.start_phase = start_phase
        self.outdict = {}

    def findAction(self, T: float, phitol=1e-8, overlap_angle=45.0):
        print(f"Finding action at T = {T}")
        if T in self.outdict:
            return self.outdict[T]["action"]

        try:
            def fmin(x):
                return optimize.fmin(
                    self.potential.Vtot, x, args=(T,), xtol=phitol, ftol=np.inf, disp=False
                )

            x0 = fmin(self.start_phase.valAt(T))
            V0 = self.potential.Vtot(x0, T)

            tunnel_list = []
            for key, p in self.potential.phases.items():
                if key == self.start_phase.key:
                    continue
                if p.T[0] > T or p.T[-1] < T:
                    continue
                x1 = fmin(p.valAt(T))
                V1 = self.potential.Vtot(x1, T)
                if V1 >= V0:
                    continue
                tdict = dict(
                    low_vev=x1,
                    high_vev=x0,
                    Tnuc=T,
                    low_phase=key,
                    high_phase=self.start_phase.key,
                )
                tunnel_list.append(tdict)

            # Check for overlap
            if overlap_angle > 0.0:
                excluded = []
                cos_overlap = np.cos(np.deg2rad(overlap_angle))
                for i in range(1, len(tunnel_list)):
                    for j in range(i):
                        xi = tunnel_list[i]["low_vev"]
                        xj = tunnel_list[j]["low_vev"]
                        xi2 = np.sum((xi - x0) ** 2)
                        xj2 = np.sum((xj - x0) ** 2)
                        dotij = np.sum((xj - x0) * (xi - x0))
                        if dotij >= np.sqrt(xi2 * xj2) * cos_overlap:
                            excluded.append(i if xi2 > xj2 else j)
                for i in sorted(excluded)[::-1]:
                    del tunnel_list[i]

            def V_(x, T=T):
                return self.potential.Vtot(x, T)

            def dV_(x, T=T):
                return self.potential.gradV(x, T)

            lowest_action = np.inf
            for tdict in tunnel_list:
                x1 = tdict["low_vev"]
                try:
                    tobj = pathDeformation.fullTunneling([x1, x0], V_, dV_, callback_data=T)
                    tdict["instanton"] = tobj
                    tdict["action"] = tobj.action
                    tdict["trantype"] = 1
                except tunneling1D.PotentialError as err:
                    if err.args[1] == "no barrier":
                        tdict["trantype"] = 0
                        tdict["action"] = 0.0
                    elif err.args[1] == "stable, not metastable":
                        tdict["trantype"] = 0
                        tdict["action"] = 0.0
                    else:
                        print("Unexpected error message.")
                        raise
                if tdict["action"] <= lowest_action:
                    lowest_action = tdict["action"]
            #if lowest_action == np.inf:
            #    lowest_action = 0.0
            return lowest_action
        except Exception as e:
            return 0
