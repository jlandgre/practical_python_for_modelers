from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import math
import pandas as pd

class RollLength:
    def __init__(self, df_raw=None, diam_roll=None, diam_core=None, caliper=None, IsTest=False):
        """
        Initializes a RollLength object
        JDL 4/27/23

        Args:
            df_raw (pandas.DataFrame, optional): DataFrame of experimental length (meters) by diameter (millimeters)
                raw data for the roll. Each row represents a measurement as an actual roll of material is unwound.
            diam_core (float, optional): Diameter in millimeters of the core that the material is wound onto.
            caliper (float, optional): Thickness of the substrate measured in millimeters.
            IsTest (bool, optional): Flag indicating whether it is a test scenario.
        """
        self.diam_core = diam_core
        self.diam_roll = diam_roll
        self.caliper = caliper

        #Raw fit attributes
        self.df_raw = df_raw        
        self.slope = None
        self.intercept = None
        self.R_squared = None

    """
    =========================================================================
    CaliperFromRawData Procedure
    =========================================================================
    """
    @property
    def CaliperFromRawData(self):
        """
        Add ‘diam_m’ and ‘diam_m^2’ calculated columns to .df_raw
        Usage:
            Instance RollLength with df_raw populated with diam (mm) by
            length aka roll length (m). Property returns a  
        """
        self.AddCalculatedRawCols()
        self.FitRawData()
        self.CalculateCaliper()
        return self.caliper
    
    def CalculateCaliper(self):
        """
        Calculate the caliper attribute from the slope and convert to millimeters.
        Round the caliper to 4 decimal places.
        """
        
        # Calculate caliper using the formula: caliper = pi / (4 * slope)
        self.caliper = math.pi / (4 * self.slope)

        # Convert caliper to millimeters and round
        self.caliper *= 1000
        self.caliper = round(self.caliper, 4)

    def FitRawData(self):
        """
        Calculate slope, intercept, and R-squared attributes for 
        raw data linear fit
        JDL 4/27/23
        """

        if self.df_raw is None:
            raise ValueError("No raw data available to fit.")

        X = self.df_raw['diam_m^2'].values.reshape(-1, 1)
        y = self.df_raw['length'].values

        # Fit the data using scikit-learn LinearRegression
        reg = LinearRegression()
        reg.fit(X, y)

        # Set the attributes
        self.slope = reg.coef_[0]
        self.intercept = reg.intercept_
        self.R_squared = reg.score(X, y)

    def AddCalculatedRawCols(self):
        """
        Add Calculated columns to length, diam raw measurement data
        """
        self.df_raw['diam_m'] = self.df_raw['diameter'] / 1000
        self.df_raw['diam_m^2'] = self.df_raw['diam_m'] ** 2

    def PlotLengthVsDiameter(self):
        plt.scatter(self.df_raw['diameter'], self.df_raw['length'])
        plt.xlabel('Diameter (mm)')
        plt.ylabel('Length (m)')
        plt.title('Length vs. Diameter')
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.show()

    def PlotLengthVsDiamSquared(self):
        plt.scatter(self.df_raw['diam_m^2'], self.df_raw['length'])
        plt.xlabel('Diameter Squared (m^2)')
        plt.ylabel('Length (m)')
        plt.title('Length vs. Diameter Squared')
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.show()

    """
    =========================================================================
    Length calculation given caliper, diam and diam_core inputs
    =========================================================================
    """
    @property
    def CalculateLength(self):
        """
        Calculate roll length in meters
        JDL 4/27/23
        """
        mm_m = 1000.
        numerator = math.pi * ((self.diam_roll / mm_m) ** 2 - 
                               (self.diam_core / mm_m) ** 2)
        denom = (4 * (self.caliper / mm_m))
        self.length = numerator / denom
        return round(self.length, 1)

