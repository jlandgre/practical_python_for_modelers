#Version 4/28/23
"""
These commands are helpful for avoiding typing
1) Run all tests in *.py file: python -m pytest test_roll_exercise.py -v -s
2) Run a specific test: python -m pytest test_roll_exercise.py -v -s -k 'test_xxx'

Ruler helpful staying in PEP 8 line length guideline
#2345678901234567890123456789012345678901234567890123456789012345678901234567890

https://peps.python.org/pep-0008
"""
import sys, os
import pandas as pd
import numpy as np
import pytest

#Append the roll_scripts subdirectory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

#Import project-specific classes
from roll import RollLength
from projfiles import Files

#Toggle to activate various print statements within tests (if IsPrint:)
IsPrint = False



"""
Example "fixtures" 
* helpful for any attribute re-used in multiple tests
* return statement populates
* gets re-instanced whenever used in a test so ok to modify it within a test
* add fixture name as fixture or test function argument to make available there


Values are based on the actual, Excel raw data to keep the test results
realistic and more intuitive -- a 20 m long roll of toilet paper is 120 mm in
diamter and has a core diameter of 40 mm
"""
@pytest.fixture
def df_raw():
    return pd.DataFrame({'length': [0., 20.], 'diameter': [40, 120]})

@pytest.fixture()
def roll_raw_fit(df_raw):
    """
    Instance RollLength class with the df_raw two-row fixture data
    """
    return RollLength(df_raw)

@pytest.fixture()
def roll_LCalc(df_raw):
    return RollLength(df_raw=df_raw, diam_roll=120.5, diam_core=43.2, 
                      caliper=0.47)





"""
Exercise 1
"""
def test_RollLength_Init_CheckFixture(roll_raw_fit):
    """
    Test the df_raw fixture
    """
    #You can use isintance to check that roll_raw_fit is a RollLength object
    pass





"""
Exercise 2
"""
def test_AddCalculatedRawCols(roll_raw_fit, df_raw):
    """
    Add ‘diam_m’ and ‘diam_m^2’ calculated columns to .df_raw
    """
    # Call the new method to add calculated columns
    roll_raw_fit.AddCalculatedRawCols()

    if IsPrint:
        PrintDF(roll_raw_fit.df_raw, 'df_raw')

    # Check if the calculated columns are added correctly
    """
    Add a check that the columns got added
    Hint: can use xxx in df.columns with assert
    """

    # Check the values of the calculated columns
    """
    Add checks that values are correctly calculated
    (2nd df row, 120 mm --> 0.120 m and 0.0144 m^2)
    Can use .loc function
    Helpful to print out the df earlier to remind on index values for loc
    """




















def x_test_PlottingMethods(roll_raw_fit):
    # Add calculated columns
    roll_raw_fit.AddCalculatedRawCols()

    # Plot length vs. diameter
    roll_raw_fit.PlotLengthVsDiameter()

    # Plot length vs. diam_m^2
    roll_raw_fit.PlotLengthVsDiamSquared()

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
                                   
def test_RollLength_Init():
    """
    ChatGPT wrote this one...JDL debugged
    """
    # Test case 1: Check if the attributes are set properly when all parameters are provided
    df_raw = pd.DataFrame({'length': [10, 20, 30], 'diameter': [100, 150, 200]})
    diam_roll = None
    diam_core = 50
    caliper = 0.1
    IsTest=True

    roll = RollLength(df_raw, diam_roll, diam_core, caliper, IsTest)

    """
    Note different ways of doing comparison checks
    .equals() for df or series
    is None for unpopulated attributes
    x == y for variables and lists
    """
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
