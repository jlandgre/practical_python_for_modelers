import sys, os
def SetProjFiles(proj_abbrev, root_folder, cwd_jupyter, IsTest=False, subdir_tests=''):
    """
    This demonstrates moving files instancing out of a 'dashboard' ipynb --to reduce clutter in
    a file potentially used by non-coders to run a model
    JDL updated 4/12/23
    """
    lsthome = cwd_jupyter.split(os.sep)
    idx_root = lsthome.index(root_folder) + 1
    dir_projfiles = os.sep.join(lsthome[0:idx_root] + [proj_abbrev + '_scripts', 'projfiles'])
    if dir_projfiles not in sys.path: sys.path.append(dir_projfiles)
    import projfiles
    files = projfiles.Files(proj_abbrev, subdir_home=lsthome[-1], IsTest=IsTest, subdir_tests=subdir_tests)
    files.PrintLocations()
    return files