import numpy as np
import matplotlib.pyplot as plt

class StochasticSEIR:
    def __init__(self, S0, E0, I0, R0, beta, sigma, gamma, population, time_steps):
        """
        Initializes the stochastic SEIR model.

        Args:
            S0 (int): Initial number of susceptible individuals.
            E0 (int): Initial number of exposed individuals.
            I0 (int): Initial number of infected individuals.
            R0 (int): Initial number of recovered individuals.
            beta (float): Transmission rate.
            sigma (float): Incubation rate (1/incubation period).
            gamma (float): Recovery rate.
            population (int): Total population (N = S + E + I + R).
            time_steps (int): Number of time steps for the simulation.
        """
        self.S0 = S0
        self.E0 = E0
        self.I0 = I0
        self.R0 = R0
        self.beta = beta
        self.sigma = sigma
        self.gamma = gamma
        self.N = population
        self.time_steps = time_steps

    def simulate(self):
        """
        Runs a single simulation of the SEIR model for the defined number of time steps.

        Returns:
            results (dict): A dictionary with keys 'S', 'E', 'I', 'R' containing lists of population sizes
                            at each time step for susceptible, exposed, infected, and recovered compartments.
        """
        # Initialize the compartments
        S = self.S0
        E = self.E0
        I = self.I0
        R = self.R0

        results = {'S': [], 'E': [], 'I': [], 'R': []}

        for t in range(self.time_steps):
            results['S'].append(S)
            results['E'].append(E)
            results['I'].append(I)
            results['R'].append(R)

            if I == 0 and E == 0:  # Stop if no more infected or exposed individuals
                break

            # Probabilities for new infections, new exposures, and recoveries
            infection_prob = 1 - np.exp(-self.beta * I / self.N)
            incubation_prob = 1 - np.exp(-self.sigma)
            recovery_prob = 1 - np.exp(-self.gamma)

            # New exposures, new infections, and recoveries based on binomial distributions
            new_exposures = np.random.binomial(S, infection_prob)
            new_infections = np.random.binomial(E, incubation_prob)
            new_recoveries = np.random.binomial(I, recovery_prob)

            # Update compartments
            S -= new_exposures
            E += new_exposures - new_infections
            I += new_infections - new_recoveries
            R += new_recoveries

        return results

    def run_simulations(self, Nsim, quantiles=[0.25, 0.5, 0.75]):
        """
        Runs the SEIR model simulation Nsim times and computes the specified quantiles.

        Args:
            Nsim (int): The number of simulations to run.
            quantiles (list of float): A list of quantiles to compute (e.g., [0.25, 0.5, 0.75]).

        Returns:
            quantile_results (dict of dict): A dictionary of dictionaries where the outer key is the compartment ('S', 'E', 'I', 'R')
                                             and the inner key is the quantile, each containing an array of shape (time_steps).
        """
        # Initialize lists to store all simulation results
        all_S = []
        all_E = []
        all_I = []
        all_R = []

        # Run Nsim simulations and collect results
        for _ in range(Nsim):
            results = self.simulate()
            all_S.append(results['S'])
            all_E.append(results['E'])
            all_I.append(results['I'])
            all_R.append(results['R'])

        # Find the longest simulation
        max_len = max(len(traj) for traj in all_S)

        # Pad the trajectories with the last value to make them all the same length
        for i in range(Nsim):
            if len(all_S[i]) < max_len:
                all_S[i].extend([all_S[i][-1]] * (max_len - len(all_S[i])))
                all_E[i].extend([all_E[i][-1]] * (max_len - len(all_E[i])))
                all_I[i].extend([all_I[i][-1]] * (max_len - len(all_I[i])))
                all_R[i].extend([all_R[i][-1]] * (max_len - len(all_R[i])))

        # Convert lists to arrays to compute the quantiles
        all_S = np.array(all_S)
        all_E = np.array(all_E)
        all_I = np.array(all_I)
        all_R = np.array(all_R)

        # Compute the quantiles across the simulations and store them in a dict of dicts
        quantile_results = {
            'S': {q: np.quantile(all_S, q, axis=0) for q in quantiles},
            'E': {q: np.quantile(all_E, q, axis=0) for q in quantiles},
            'I': {q: np.quantile(all_I, q, axis=0) for q in quantiles},
            'R': {q: np.quantile(all_R, q, axis=0) for q in quantiles}
        }

        return quantile_results

    def plot(self, quantile_results, quantiles=[0.25, 0.5, 0.75]):
        """
        Plots the quantile trajectories of the SEIR model.

        Args:
            quantile_results (dict of dict): The quantile results of the simulations with keys 'S', 'E', 'I', 'R',
                                             and inner keys as the quantiles (e.g., 0.25, 0.5, 0.75).
            quantiles (list of float): The quantiles to plot (e.g., [0.25, 0.5, 0.75]).
        """
        time_range = range(len(quantile_results['S'][quantiles[0]]))
        
        for q in quantiles:
            plt.plot(time_range, quantile_results['S'][q], label=f'Susceptible ({q*100:.0f}%)')
            plt.plot(time_range, quantile_results['E'][q], label=f'Exposed ({q*100:.0f}%)')
            plt.plot(time_range, quantile_results['I'][q], label=f'Infected ({q*100:.0f}%)')
            plt.plot(time_range, quantile_results['R'][q], label=f'Recovered ({q*100:.0f}%)')

        plt.xlabel('Time Steps')
        plt.ylabel('Population')
        plt.legend()
        plt.title('Stochastic SEIR Model - Quantiles over Multiple Simulations')
        plt.show()


