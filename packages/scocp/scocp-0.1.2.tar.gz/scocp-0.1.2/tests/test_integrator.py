"""Test integrator class"""

import numpy as np

import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import scocp

def test_scipy_integrator_cr3bp_impulsive():
    """Test `ScipyIntegrator` class for impulsive CR3BP dynamics"""
    mu = 1.215058560962404e-02
    integrator = scocp.ScipyIntegrator(nx=6, nu=3, rhs=scocp.rhs_cr3bp, rhs_stm=scocp.rhs_cr3bp_stm, args=(mu,),
                                       method='DOP853', reltol=1e-12, abstol=1e-12)

    # propagate uncontrolled and controlled dynamics
    x0 = np.array([
        1.0809931218390707E+00,
        0.0,
        -2.0235953267405354E-01,
        0.0,
        -1.9895001215078018E-01,
        0.0])
    period_0 = 2.3538670417546639E+00
    sol_lpo0 = integrator.solve([0.0, period_0], x0, stm=True, get_ODESolution=True)

    assert sol_lpo0.y[0:6,-1].shape == (6,)
    assert np.max(np.abs((sol_lpo0.y[0:6,-1] - x0))) < 1e-11
    return


def test_scipy_integrator_cr3bp_continuous():
    """Test `ScipyIntegrator` class for continuous CR3BP dynamics"""
    mu = 1.215058560962404e-02
    integrator = scocp.ScipyIntegrator(nx=6, nu=3, rhs=scocp.control_rhs_cr3bp, rhs_stm=scocp.control_rhs_cr3bp_stm,
                                       impulsive=False, args=(mu,[0.0,0.0,0.0]),
                                       method='DOP853', reltol=1e-12, abstol=1e-12)

    # propagate uncontrolled and controlled dynamics
    x0 = np.array([
        1.0809931218390707E+00,
        0.0,
        -2.0235953267405354E-01,
        0.0,
        -1.9895001215078018E-01,
        0.0])
    period_0 = 2.3538670417546639E+00
    sol_lpo0 = integrator.solve([0.0, period_0], x0, stm=False, get_ODESolution=True)

    assert sol_lpo0.y[0:6,-1].shape == (6,)
    assert np.max(np.abs((sol_lpo0.y[0:6,-1] - x0))) < 1e-11
    return



if __name__ == "__main__":
    test_scipy_integrator_cr3bp_continuous()
