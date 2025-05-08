import pytest
import matplotlib
matplotlib.use("Agg")  # Use non-GUI backend before importing pyplot
import numpy as np
import pandas as pd
from datetime import timedelta
from scipy import stats
from epydemix.calibration.abc import ABCSampler
from epydemix.model.predefined_models import create_sir
from epydemix.population import Population
from epydemix.model import simulate

@pytest.fixture
def mock_simulation_function():
    """Fixture providing a simple mock simulation function"""
    def simulate(params):
        beta = params.get("beta", 0.3)
        gamma = params.get("gamma", 0.1)
        # Simple deterministic SIR output
        return {
            "data": np.array([100 * np.exp(-beta * gamma * t) for t in range(10)])
        }
    return simulate

@pytest.fixture
def basic_abc_sampler(mock_simulation_function):
    """Fixture providing a basic ABC sampler setup"""
    # Define priors
    priors = {
        "beta": stats.uniform(0.1, 0.5),  # U(0.1, 0.6)
        "gamma": stats.uniform(0.05, 0.2)  # U(0.05, 0.25)
    }
    
    # Create sampler
    return ABCSampler(
        simulation_function=mock_simulation_function,
        priors=priors,
        parameters={"dt": 0.1},
        observed_data=np.array([90, 82, 75, 68, 62, 57, 52, 48, 44, 40]),
    )

def test_abc_initialization(basic_abc_sampler):
    """Test ABC sampler initialization"""
    assert len(basic_abc_sampler.param_names) == 2
    assert "beta" in basic_abc_sampler.continuous_params
    assert "gamma" in basic_abc_sampler.continuous_params
    assert len(basic_abc_sampler.discrete_params) == 0

def test_abc_rejection(basic_abc_sampler):
    """Test ABC rejection sampling"""
    results = basic_abc_sampler.calibrate(
        strategy="rejection",
        epsilon=100.0,
        num_particles=10,
        verbose=False
    )
    
    # Check results structure
    assert len(results.posterior_distributions) == 1
    posterior = results.posterior_distributions[0]
    assert "beta" in posterior.columns
    assert "gamma" in posterior.columns
    
    # Check parameter ranges
    assert np.all((0.1 <= posterior["beta"]) & (posterior["beta"] <= 0.6))
    assert np.all((0.05 <= posterior["gamma"]) & (posterior["gamma"] <= 0.25))

def test_abc_smc(basic_abc_sampler):
    """Test ABC Sequential Monte Carlo"""
    results = basic_abc_sampler.calibrate(
        strategy="smc",
        num_particles=10,
        num_generations=3,
        epsilon_quantile_level=0.5,
        verbose=False
    )
    
    # Check results structure
    assert len(results.posterior_distributions) == 3  # One per generation
    
    # Check parameter ranges in final generation
    final_posterior = results.get_posterior_distribution()
    assert np.all((0.1 <= final_posterior["beta"]) & (final_posterior["beta"] <= 0.6))
    assert np.all((0.05 <= final_posterior["gamma"]) & (final_posterior["gamma"] <= 0.25))


def test_abc_with_real_model():
    """Test ABC with a real SIR model"""
    # Create SIR model
    model = create_sir(transmission_rate=0.3, recovery_rate=0.1)
    
    # Set up population
    pop = Population()
    pop.add_population([10000])
    pop.add_contact_matrix(np.array([[1.0]]))
    model.set_population(pop)
    
    # Generate synthetic data
    true_params = {
        "beta": 0.3,
        "gamma": 0.1
    }
    model.add_parameter(parameters_dict=true_params)

    
    synthetic_data = simulate(
        epimodel=model,
        start_date="2023-01-01",
        end_date="2023-01-10",
        initial_conditions_dict={
            "Susceptible": np.array([9900]),
            "Infected": np.array([100]),
            "Recovered": np.array([0])
        }
    )

    def simulate_wrapper(parameters): 
        results = simulate(**parameters)
        return {"data": results.compartments["Infected_total"]}
    
    # Set up ABC sampler
    sampler = ABCSampler(
        simulation_function=simulate_wrapper,
        priors={
            "transmission_rate": stats.uniform(0.1, 0.5),
            "recovery_rate": stats.uniform(0.05, 0.2)
        },
        parameters=dict(epimodel=model,
                        start_date="2023-01-01",
                        end_date="2023-01-10",
                        initial_conditions_dict={
                            "Susceptible": np.array([9900]),
                            "Infected": np.array([100]),
                            "Recovered": np.array([0])
                            }),
        observed_data=synthetic_data.compartments["Infected_total"]
    )
    # Run calibration
    results = sampler.calibrate(
        strategy="rejection",
        epsilon=100,
        num_particles=10,
        verbose=False
    )
    
def test_abc_error_handling(basic_abc_sampler):
    """Test error handling in ABC"""
    # Test invalid strategy
    with pytest.raises(ValueError):
        basic_abc_sampler.calibrate(strategy="invalid_strategy")


def test_abc_runtime_limits(basic_abc_sampler):
    """Test ABC runtime limits"""
    # Test max time limit
    results = basic_abc_sampler.calibrate(
        strategy="rejection",
        epsilon=0.1,
        num_particles=1000,
        max_time=timedelta(seconds=1),
        verbose=False
    )
    assert len(results.posterior_distributions) > 0

    # Test simulation budget limit
    results = basic_abc_sampler.calibrate(
        strategy="rejection",
        epsilon=0.1,
        num_particles=1000,
        total_simulations_budget=100,
        verbose=False
    )
    assert len(results.posterior_distributions) > 0 