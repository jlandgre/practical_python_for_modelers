#Version 4/12/23
#J.D. Landgrebe/Data-Delve Engineer LLC
#Covered under MIT Open Source License (https://github.com/jlandgre/Python_Projfiles)
import inspect, os

class Files():
    """
    Class for keeping track of project files in standard project folder structure

    __init__() Arguments:
      proj_abbrev [String] project prefix string for folder names
      subdir_home [String] name of a Home subdirectory within
        proj/proj_case_studies folder
      IsTest [Boolean] Toggles between production and testing (IsTest=True).
      subdir_tests [String] allows files related to specific issues to be placed
        in subfolders within the Proj/proj_scripts/tests subfolder.

        For example, if Issues List issue 42 relates to solving a bug, the folder
        "tests/issue_042_2023_10_BugFix" subfolder would contain example files to
        recreate the issue along with text or Word doc documentation exlaining
        the cause of the bug and how it was fixed

    Naming and Case Conventions:
    * lowercase for project-specific attributes except if creates ambiguity;
      then use underscore to separate words
    * self.path_xxx is a complete directory path with os-specific separator as
      last character
    * self.pf_xxx is a complete directory path + filename
    * self.f_xxx is a filename with extension
    * self.path_subdir_xxx is a folder name or directory path suffix

    JDL Updated 4/12/23
    """
    def __init__(self, proj_abbrev, subdir_home='', IsTest=False, subdir_tests=''):
        self.IsTest = IsTest #Boolean toggle for test versus production mode
        self.subdir_tests = subdir_tests
        self.proj_abbrev = proj_abbrev

        #Initialize Class attributes
        self.lstpaths = [] #Internal list of paths
        self.path_root = '' #Project root directory
        self.path_scripts = '' #proj_scripts subdirectory
        self.path_tests = '' #tests subfolder within proj_scripts
        self.path_data = '' #proj_data subdirectory
        self.path_case_studies = '' #proj_case_studies subdirectory
        self.path_home = '' #optional "home" for current activeity (e.g. case_studies subfolder)
        self.subdir_tests = '' #optional path to tests subfolder (based on subdir_tests)
        self.path_subdir_home = '' #optional path to home subfolder (within proj_case_studies)

        #Optional Case Study "Home" directory (subfolder in proj/proj_case_studies)
        if len(subdir_home) > 0: self.path_subdir_home = subdir_home

        #Optional subdirectory within tests folder - to contain issue-specific files
        if IsTest: self.subdir_tests = subdir_tests

        #Set generic and project-specific paths
        self.SetGenericProjectPaths()
        self.SetProjectSpecificPaths()

    def SetGenericProjectPaths(self):
        """
        Set strings for project-specific files and paths
        """
        #Instance Project Paths and set top-level folder names and paths
        iLevels = 3
        self.BuildLstPaths(iLevels)
        self.path_root = self.lstpaths[2]
        self.path_scripts = self.lstpaths[1]
        self.path_tests = self.path_scripts + 'tests' + os.sep
        self.path_data = self.path_root + self.proj_abbrev + '_data' + os.sep
        sName = self.proj_abbrev + '_case_studies'
        self.path_case_studies = self.path_root + sName + os.sep

        #If a home subdirectory was specified, set path_home
        if len(self.path_subdir_home) > 0:
          self.path_home = self.path_case_studies + self.path_subdir_home + os.sep

        #If testing, reassign root and data directories to proj/proj_scripts/tests
        if self.IsTest:
          self.path_root = self.path_tests
          self.path_data = self.path_tests

          #reassign data path if tests subdirectory specified
          if len(self.subdir_tests) > 0:
            self.path_data = self.path_data + self.subdir_tests + os.sep
            #self.path_home = self.path_data

        #Store user-specific credentials/tokens outside of main project folder
        self.pf_credentials = self.path_root + 'credentials.csv'

        #ColInfo location
        self.spf_colinfo = self.path_scripts + 'colinfo.xlsx'
        if self.IsTest: self.spf_colinfo = self.path_root + 'colinfo.xlsx'

    def SetProjectSpecificPaths(self):
        """
        Project specific directories and files
        """
        #xxx
        self.path_xxx = self.path_home + 'xxx' + os.sep

    def BuildLstPaths(self, iLevels):
        """
        Build list of nested directory paths based on location of projfiles.py
        Uses inspect.getframeinfo() method
        JDL Updated 1/16/23
        """
        # List paths to iLevels levels - starting with home/top, lst[0]; 4/8/22
        PF_thisfile = inspect.getframeinfo(inspect.currentframe()).filename
        path_thisfile = str(os.path.dirname(os.path.abspath(PF_thisfile))) + os.sep
        lstdirs = path_thisfile.split(os.sep)

        self.lstpaths = []
        for i in range(len(lstdirs)-1, len(lstdirs) - iLevels-1, -1):
            self.lstpaths.append(os.sep.join(lstdirs[0:i]) + os.sep)
    
    def PrintLocations(self):
      print('\n')
      print('files.path_root\n', self.path_root, '\n')
      print('files.path_data\n', self.path_data, '\n')
      print('files.path_case_studies\n', self.path_case_studies, '\n')
      print('files.path_home\n', self.path_home, '\n')
      print('files.path_scripts\n', self.path_scripts, '\n')
      if self.IsTest:
        print('files.path_tests\n', self.path_tests, '\n')

