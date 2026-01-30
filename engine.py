import numpy as np
import pandas as pd

class CDCEngine:
    def __init__(self, N, r0, vax_rate, vax_efficacy):
        self.N = N
        self.gamma = 0.1  # Recovery rate
        self.beta = r0 * self.gamma
        self.vax_rate = vax_rate
        self.vax_eff = vax_efficacy

    def run_simulation(self, days, ss_prob, partial_prot):
        # Initializing compartments
        num_vax = int(self.N * self.vax_rate)
        S, V, P, I, R = [self.N - num_vax - 1], [num_vax], [0], [1], [0]
        
        for _ in range(days):
            s, v, p, i, r = S[-1], V[-1], P[-1], I[-1], R[-1]
            
            # Stochastic Logic
            curr_beta = self.beta * 3.0 if np.random.random() < ss_prob else self.beta
            
            # CDC transitions
            inf_s = np.random.poisson(curr_beta * s * i / self.N)
            inf_v = np.random.poisson(curr_beta * (1 - self.vax_eff) * v * i / self.N)
            inf_p = np.random.poisson(curr_beta * (1 - partial_prot) * p * i / self.N)
            new_rec = np.random.poisson(self.gamma * i)
            waning = np.random.poisson(0.01 * v)

            # State Updates
            S.append(s - inf_s)
            V.append(v - inf_v - waning)
            P.append(p - inf_p + waning)
            I.append(i + inf_s + inf_v + inf_p - new_rec)
            R.append(r + new_rec)
            
        return pd.DataFrame({"Day": range(days+1), "S": S, "V": V, "P": P, "I": I, "R": R})
