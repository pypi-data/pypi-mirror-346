# r_interface.py

import os
from pathlib import Path
import rpy2.robjects as rob
from rpy2.robjects.packages import importr

required_r_packages = ['limma', 'ggplot2', 'impute', 'dplyr', 'matrixStats', 'stats', 'tidyr', 'samr', 'writexl', 'car', 'fdrtool']
loaded_r_packages = {}

for pkg in required_r_packages:
    try:
        loaded_r_packages[pkg] = importr(pkg)
    except Exception as e:
        print(f"Failed to load R package '{pkg}': {e}")


def source_r_script(relative_paths):
    """
    Load an R script using a path relative to the package.
    """
    # Get the directory where r_interface.py is located
    package_dir = Path(__file__).parent
    
    for relative_path in relative_paths:
        # Resolve the full absolute path to the R script
        script_path = package_dir/relative_path
        
        # Ensure script exists
        if not script_path.exists():
            raise FileNotFoundError(f"R script not found: {script_path}")
        
        # Load R script in R environement
        rob.r['source'](str(script_path))

    


def get_r_function(func_name):
    """
    Retrieve an R function that has been sourced.
    """
    if func_name not in rob.r.ls():
        raise ValueError(f"R function '{func_name}' not found. Make sure the script containing it is sourced.")
    return rob.r[func_name]