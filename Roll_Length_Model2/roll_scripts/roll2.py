#Version 5/1/23
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import math
import pandas as pd
#2345678901234567890123456789012345678901234567890123456789012345678901234567890


class RollLength:
    def __init__(self, file_raw='', diam_roll=None, diam_core=None, caliper=None):
        """
        Initializes a RollLength object
        JDL 4/27/23

        Args:
        file_raw (string, optional): Directory path + filename for raw, length 
            versus diam data where rows represent measurements on a roll as 
            material is unwound.
        diam_core (float, optional): Diameter in mm of the core that the 
            material is wound onto.
        diam_roll (float, optional): Roll diameter [mm] for the substrate roll
        caliper (float, optional): Thickness of the substrate measured in mm.
        """

        #CalculateRollLength procedure
        self.diam_core = diam_core
        self.diam_roll = diam_roll
        self.caliper = caliper
        self.length = None #Substrate roll length [m]

        #CaliperFromRawData procedure attributes 
        self.file_raw = file_raw 
        self.df_raw = None #Df with raw length [m] vs. diam [mm] exptl. data
        self.slope = None #Calculated slope from linear fit
        self.intercept = None #Calculated y-intercept from linear fit
        self.R_squared = None #Calculated R-Squared from linear fit

    """
    =========================================================================
    CaliperFromRawData Procedure
    =========================================================================
    """
    @property
    def CaliperFromRawData(self):
        """
        Example of Class Property -- returns just the caliper after running
        the procedure to open raw data file, transform and fit the data
        """
        self.CaliperFromRawDataProcedure()
        return self.caliper

    def CaliperFromRawDataProcedure(self):
        """
        Procedure to fit a line to transformed raw, length versus diam data
        and thereby enable calculation of an effective caliper for the
        material on a roll of substrate.

        This use case only uses the file_raw Class input --to read in raw
        data
        """
        self.ReadRawData()
        self.AddCalculatedRawCols()
        self.FitRawData()
        self.CalculateCaliper()
    
    def ReadRawData(self):
        """
        Import experimental length versus diam data to Pandas DataFrame
        """
        self.df_raw = pd.read_excel(self.file_raw)
    
    def AddCalculatedRawCols(self):
        """
        Add Calculated columns to length, diam raw measurement data
        """
        self.df_raw['diam_m'] = self.df_raw['diameter'] / 1000
        self.df_raw['diam_m^2'] = self.df_raw['diam_m'] ** 2

    def FitRawData(self):
        """
        Calculate slope, intercept, and R-squared attributes for 
        raw data linear fit
        """
        if self.df_raw is None:
            raise ValueError("No raw data available to fit.")

        X = self.df_raw['diam_m^2'].values.reshape(-1, 1)
        y = self.df_raw['length'].values

        reg = LinearRegression()
        reg.fit(X, y)

        self.slope = reg.coef_[0]
        self.intercept = reg.intercept_
        self.R_squared = reg.score(X, y)
    
    def CalculateCaliper(self):
        """
        Calculate the caliper attribute from the slope and convert to mm
        Round caliper to 4 decimal places.
        """
        self.caliper = math.pi / (4 * self.slope)
        self.caliper *= 1000
        self.caliper = round(self.caliper, 4)

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
    Plot raw and transformed data
    =========================================================================
    """
    def PlotRawAndTransformedData(self):
        text = 'Diameter (mm)', 'Length (m)', 'Length vs. Diameter'
        self.XYDataPlot(self.df_raw['diameter'], self.df_raw['length'], 
                        text[0],  text[1], text[2])

        text = 'Diameter Squared (m^2)', 'Length (m)', 'Length vs. Diameter Squared'
        self.XYDataPlot(self.df_raw['diam_m^2'], self.df_raw['length'], 
                        text[0],  text[1], text[2]) 


    """
    =========================================================================
    CalculateRollLength Procedure - Length calculation given caliper, diam 
    and diam_core inputs. 

    All inputs in units of mm. length output in meters
    =========================================================================
    """
    @property
    def CalculateLength(self):
        self.CalculateLengthProcedure()
        return self.length
    
    def CalculateLengthProcedure(self):
        """
        Calculate roll length in meters
        JDL 4/27/23; modified 5/1/23
        """
        mm_m = 1000.
        numerator = math.pi * ((self.diam_roll / mm_m) ** 2 - 
                               (self.diam_core / mm_m) ** 2)
        denom = (4 * (self.caliper / mm_m))
        self.length = round(numerator / denom, 1)

    """
    =========================================================================
    Utility methods
    =========================================================================
    """
    @staticmethod
    def XYDataPlot(X, Y, x_label, y_label, plot_title):
        """
        XY Plot of raw and transformed data
        """
        plt.scatter(X, Y)
        plt.xlabel(x_label), plt.ylabel(y_label)
        plt.title(plot_title)
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.show()