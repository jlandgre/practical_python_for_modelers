#Version 5/1/23
#python -m pytest test_roll.py -v -s
#2345678901234567890123456789012345678901234567890123456789012345678901234567890

import sys, os
import pandas as pd
import numpy as np
import pytest
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from roll import RollLength
from projfiles import Files

IsPrint = False

@pytest.fixture
def files_test():
    # Instantiate the Files class with the desired arguments
    return Files(proj_abbrev='roll', IsTest=True)

@pytest.fixture
def df_raw():
    return pd.DataFrame({'length': [0., 20.], 'diameter': [40, 120]})

@pytest.fixture()
def roll_raw_fit(df_raw):
    return RollLength(df_raw)

"""
=========================================================================
Length calculation given caliper, diam and diam_core inputs
=========================================================================
"""

@pytest.fixture()
def roll_LCalc():
    """
    A class instance with inputs for length calculation only
    """
    return RollLength(diam_roll=120.5, diam_core=43.2, caliper=0.47)

def test_CalculateLength(roll_LCalc):
    """
    Calculate roll length in meters
    JDL 5/1/23
    """
    roll_LCalc.CalculateLength()
    assert roll_LCalc.length == 21.1

def test_LCalc_fixture(roll_LCalc):
    """
    Check fixture's inputs
    JDL 5/1/23
    """
    assert roll_LCalc.diam_roll == 120.5
    assert roll_LCalc.diam_core == 43.2
    assert roll_LCalc.caliper == 0.47

"""
=========================================================================
Plotting raw data (no tests; just a way to show plots)
=========================================================================
"""

def x_test_PlottingMethods(roll_raw_fit):
    # Add calculated columns
    roll_raw_fit.AddCalculatedRawCols()

    # Plot length vs. diameter
    roll_raw_fit.PlotLengthVsDiameter()

    # Plot length vs. diam_m^2
    roll_raw_fit.PlotLengthVsDiamSquared()

"""
=========================================================================
CaliperFromRawData Procedure
=========================================================================
"""

def test_CalculateCaliper(roll_raw_fit):
    """
    Test the CalculateCaliper method to check the caliper calculation.
    """
    roll_raw_fit.AddCalculatedRawCols()
    roll_raw_fit.FitRawData()

    # Call the CalculateCaliper method
    roll_raw_fit.CalculateCaliper()

    # Check the caliper value
    assert roll_raw_fit.caliper == pytest.approx(0.5027, abs=1e-4)

def test_FitRawData(roll_raw_fit):
    """
    Calculate slope, intercept, and R-squared attributes for 
    raw data linear fit
    JDL 4/27/23
    """
    roll_raw_fit.AddCalculatedRawCols()
    roll_raw_fit.FitRawData()

    if IsPrint:
        lst_vars = [roll_raw_fit.slope, roll_raw_fit.intercept,roll_raw_fit.R_squared]
        PrintVars(lst_vars,['Slope', 'Intercept', 'R-squared'])

    # Perform checks on the fitted attributes
    x = roll_raw_fit.df_raw['diam_m^2'].values
    y = roll_raw_fit.df_raw['length'].values

    # Calculate the expected slope rise over run calculation (100000 from JMP check)
    delta_y = y[-1] - y[0]
    delta_x = x[-1] - x[0]
    expected_slope = delta_y / delta_x
    assert np.isclose(roll_raw_fit.slope, expected_slope)

    # Calculate the expected intercept (almost 0.000)
    expected_intercept = y[0] - expected_slope * x[0]
    assert np.isclose(roll_raw_fit.intercept, expected_intercept)

    # Calculate the R-squared value (1.0 exactly for fit through 2 points)
    expected_r_squared = 1.0
    assert np.isclose(roll_raw_fit.R_squared, expected_r_squared)

def test_AddCalculatedRawCols(roll_raw_fit, df_raw):
    """
    Add Calculated columns to length, diam raw measurement data
    """
    # Call the new method to add calculated columns
    roll_raw_fit.AddCalculatedRawCols()

    if IsPrint:
        PrintDF(roll_raw_fit.df_raw, 'df_raw')

    # Check if the calculated columns are added correctly
    assert 'diam_m' in roll_raw_fit.df_raw.columns
    assert 'diam_m^2' in roll_raw_fit.df_raw.columns

    # Check the values of the calculated columns
    assert roll_raw_fit.df_raw.loc[1, 'diam_m'] == 0.120
    assert roll_raw_fit.df_raw.loc[1, 'diam_m^2'] == 0.0144

"""
=========================================================================
Instancing RollLength Class
=========================================================================
"""
def test_RollLength_Init():
    # Test case 1: Check if the attributes are set properly when all parameters are provided
    df_raw = pd.DataFrame({'length': [10, 20, 30], 'diameter': [100, 150, 200]})
    diam_roll = None
    diam_core = 50
    caliper = 0.1
    IsTest=True

    roll = RollLength(df_raw, diam_roll, diam_core, caliper, IsTest)
    assert roll.df_raw.equals(df_raw)
    assert roll.diam_roll is None
    assert roll.diam_core == diam_core
    assert roll.caliper == caliper

    # Test case 2: Check if the attributes are set properly when no parameters are provided
    roll = RollLength()
    assert roll.df_raw is None
    assert roll.diam_core is None
    assert roll.caliper is None

    # Test case 3: Check if the attributes are set properly when only some parameters are provided
    df_raw = pd.DataFrame({'length': [10, 20, 30], 'diameter': [100, 150, 200]})

    roll = RollLength(df_raw)
    assert roll.df_raw.equals(df_raw)
    assert roll.diam_core is None
    assert roll.caliper is None

"""
=========================================================================
Utility functions for Print()
=========================================================================
"""

def PrintDF(df, text=''):
    print('\n', text, '\n')
    print(df)
    print('\n\n')

def PrintVars(vars, text):
    print('\n\n')
    if isinstance(vars, list):
        for v, s in zip(vars, text):
            print(f"{s}: {v}")
    else:
        print(f"{text}: {vars}")
    print('\n\n')
