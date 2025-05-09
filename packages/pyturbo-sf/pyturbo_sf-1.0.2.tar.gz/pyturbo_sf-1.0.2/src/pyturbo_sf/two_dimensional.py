"""Two-dimensional structure function calculations."""

import numpy as np
import xarray as xr
from joblib import Parallel, delayed
import bottleneck as bn
import gc
from scipy import stats
from numpy.lib.stride_tricks import sliding_window_view


from .core import (validate_dataset_2d, setup_bootsize_2d, calculate_adaptive_spacings_2d,
                  compute_boot_indexes_2d, get_boot_indexes_2d)
from .utils import (fast_shift_2d, check_and_reorder_variables_2d, map_variables_by_pattern_2d)
                   
##################################Structure Functions Types########################################

def calc_longitudinal_2d(subset, variables_names, order, dims, ny, nx):
    """
    Calculate longitudinal structure function: (du*dx + dv*dy)^n / |r|^n
    or (du*dx + dw*dz)^n / |r|^n or (dv*dy + dw*dz)^n / |r|^n depending on the plane.
    
    Parameters
    ----------
    subset : xarray.Dataset
        Subset of the dataset containing required variables
    variables_names : list
        List of variable names (should contain two velocity components)
    order : int
        Order of the structure function
    dims, ny, nx : various
        Additional parameters needed for calculation
        
    Returns
    -------
    numpy.ndarray, numpy.ndarray, numpy.ndarray
        Structure function values, DX values, DY values
    """
    if len(variables_names) != 2:
        raise ValueError(f"Longitudinal structure function requires exactly 2 velocity components, got {len(variables_names)}")
    
    # Check and reorder variables if needed based on plane
    var1, var2 = check_and_reorder_variables_2d(variables_names, dims)
    
    # Arrays to store results
    results = np.full(ny * nx, np.nan)
    dx_vals = np.full(ny * nx, 0.0)
    dy_vals = np.full(ny * nx, 0.0)
    
    # Get the velocity components
    comp1_var = subset[var1].values
    comp2_var = subset[var2].values
    
    # Get coordinate variables based on the plane
    if dims == ['y', 'x']:
        # (y, x) plane
        x_coord = subset.x.values
        y_coord = subset.y.values
    elif dims == ['z', 'x']:
        # (z, x) plane
        x_coord = subset.x.values
        y_coord = subset.z.values  # Using y_coord to store z-coordinate for consistency
    elif dims == ['z', 'y']:
        # (z, y) plane
        x_coord = subset.y.values  # Using x_coord to store y-coordinate for consistency
        y_coord = subset.z.values
    else:
        raise ValueError(f"Unsupported dimension combination: {dims}")
    
    # Loop through all points
    idx = 0
    for iy in range(ny):
        for ix in range(nx):
                            
            # Compute actual physical separation
            dx = fast_shift_2d(x_coord, iy, ix) - x_coord
            dy = fast_shift_2d(y_coord, iy, ix) - y_coord
            
            
            # Compute norm of separation vector
            norm = np.maximum(np.sqrt(dx**2 + dy**2), 1e-10) # to avoid dividing by zero
             
            
            # Calculate velocity differences
            dcomp1 = fast_shift_2d(comp1_var, iy, ix) - comp1_var
            dcomp2 = fast_shift_2d(comp2_var, iy, ix) - comp2_var
            
            # Store the separation distances
            dx_vals[idx] = bn.nanmean(dx)
            dy_vals[idx] = bn.nanmean(dy)
            
            
            # Project velocity difference onto separation direction (longitudinal)
            delta_parallel = dcomp1 * (dx/norm) + dcomp2 * (dy/norm)
            
            # Compute structure function
            sf_val = (delta_parallel) ** order
            results[idx] = bn.nanmean(sf_val)
            
            idx += 1
            
    return results, dx_vals, dy_vals


def calc_transverse_2d(subset, variables_names, order, dims, ny, nx):
    """
    Calculate transverse structure function: (du*dy - dv*dx)^n / |r|^n
    or (du*dz - dw*dx)^n / |r|^n or (dv*dz - dw*dy)^n / |r|^n depending on the plane.
    
    Parameters
    ----------
    subset : xarray.Dataset
        Subset of the dataset containing required variables
    variables_names : list
        List of variable names (should contain two velocity components)
    order : int
        Order of the structure function
    dims, ny, nx : various
        Additional parameters needed for calculation
        
    Returns
    -------
    numpy.ndarray, numpy.ndarray, numpy.ndarray
        Structure function values, DX values, DY values
    """
    if len(variables_names) != 2:
        raise ValueError(f"Transverse structure function requires exactly 2 velocity components, got {len(variables_names)}")
    
    # Check and reorder variables if needed based on plane
    var1, var2 = check_and_reorder_variables_2d(variables_names, dims, fun='transverse')
    
    # Arrays to store results
    results = np.full(ny * nx, np.nan)
    dx_vals = np.full(ny * nx, 0.0)
    dy_vals = np.full(ny * nx, 0.0)
    
    # Get the velocity components
    comp1_var = subset[var1].values
    comp2_var = subset[var2].values
    
    # Get coordinate variables based on the plane
    if dims == ['y', 'x']:
        # (y, x) plane
        x_coord = subset.x.values
        y_coord = subset.y.values
    elif dims == ['z', 'x']:
        # (z, x) plane
        x_coord = subset.x.values
        y_coord = subset.z.values  # Using y_coord to store z-coordinate for consistency
    elif dims == ['z', 'y']:
        # (z, y) plane
        x_coord = subset.y.values  # Using x_coord to store y-coordinate for consistency
        y_coord = subset.z.values
    else:
        raise ValueError(f"Unsupported dimension combination: {dims}")
    
    # Loop through all points
    idx = 0
    for iy in range(ny):
        for ix in range(nx):
                            
            # Compute actual physical separation
            dx = fast_shift_2d(x_coord, iy, ix) - x_coord
            dy = fast_shift_2d(y_coord, iy, ix) - y_coord
            
            
            # Compute norm of separation vector
            norm = np.maximum(np.sqrt(dx**2 + dy**2), 1.0e-10)                
            
            # Calculate velocity differences
            dcomp1 = fast_shift_2d(comp1_var, iy, ix) - comp1_var
            dcomp2 = fast_shift_2d(comp2_var, iy, ix) - comp2_var
            
            # Store the separation distances
            dx_vals[idx] = bn.nanmean(dx)
            dy_vals[idx] = bn.nanmean(dy)
            
            # Calculate transverse component (perpendicular to separation direction)
            delta_perp = dcomp1 * (dy/norm) - dcomp2 * (dx/norm)
            
            # Compute structure function
            sf_val = (delta_perp) ** order
            results[idx] = bn.nanmean(sf_val)
            
            idx += 1
            
    return results, dx_vals, dy_vals


def calc_default_vel_2d(subset, variables_names, order, dims, ny, nx):
    """
    Calculate default velocity structure function: (du^n + dv^n)
    or (du^n + dw^n) or (dv^n + dw^n) depending on the plane.
    
    Parameters
    ----------
    subset : xarray.Dataset
        Subset of the dataset containing required variables
    variables_names : list
        List of variable names (should contain two velocity components)
    order : int
        Order of the structure function
    dims, ny, nx : various
        Additional parameters needed for calculation
        
    Returns
    -------
    numpy.ndarray, numpy.ndarray, numpy.ndarray
        Structure function values, DX values, DY values
    """
    if len(variables_names) != 2:
        raise ValueError(f"Default velocity structure function requires exactly 2 velocity components, got {len(variables_names)}")
    
    # Check and reorder variables if needed based on plane
    var1, var2 = check_and_reorder_variables_2d(variables_names, dims, fun='default_vel')
    
    # Arrays to store results
    results = np.full(ny * nx, np.nan)
    dx_vals = np.full(ny * nx, 0.0)
    dy_vals = np.full(ny * nx, 0.0)
    
    # Get the velocity components
    comp1_var = subset[var1].values
    comp2_var = subset[var2].values
    
    # Get coordinate variables based on the plane
    if dims == ['y', 'x']:
        # (y, x) plane
        x_coord = subset.x.values
        y_coord = subset.y.values
    elif dims == ['z', 'x']:
        # (z, x) plane
        x_coord = subset.x.values
        y_coord = subset.z.values  # Using y_coord to store z-coordinate for consistency
    elif dims == ['z', 'y']:
        # (z, y) plane
        x_coord = subset.y.values  # Using x_coord to store y-coordinate for consistency
        y_coord = subset.z.values
    else:
        raise ValueError(f"Unsupported dimension combination: {dims}")
    
    # Loop through all points
    idx = 0
    for iy in range(ny):
        for ix in range(nx):
            
            # Compute actual physical separation
            dx = fast_shift_2d(x_coord, iy, ix) - x_coord
            dy = fast_shift_2d(y_coord, iy, ix) - y_coord
                            
            # Calculate velocity differences
            dcomp1 = fast_shift_2d(comp1_var, iy, ix) - comp1_var
            dcomp2 = fast_shift_2d(comp2_var, iy, ix) - comp2_var
            
            # Store the separation distances
            dx_vals[idx] = bn.nanmean(dx)
            dy_vals[idx] = bn.nanmean(dy)
            
            # Calculate default velocity structure function: du^n + dv^n
            sf_val = (dcomp1 ** order) + (dcomp2 ** order)
            results[idx] = bn.nanmean(sf_val)
            
            idx += 1
            
    return results, dx_vals, dy_vals


def calc_scalar_2d(subset, variables_names, order, dims, ny, nx):
    """
    Calculate scalar structure function: (dscalar^n)
    
    Parameters
    ----------
    subset : xarray.Dataset
        Subset of the dataset containing required variables
    variables_names : list
        List of variable names (should contain one scalar variable)
    order : int
        Order of the structure function
    dims, ny, nx : various
        Additional parameters needed for calculation
        
    Returns
    -------
    numpy.ndarray, numpy.ndarray, numpy.ndarray
        Structure function values, DX values, DY values
    """
    if len(variables_names) != 1:
        raise ValueError(f"Scalar structure function requires exactly 1 scalar variable, got {len(variables_names)}")
    
    # Get the scalar variable name
    scalar_name = variables_names[0]
    
    # Arrays to store results
    results = np.full(ny * nx, np.nan)
    dx_vals = np.full(ny * nx, 0.0)
    dy_vals = np.full(ny * nx, 0.0)
    
    # Get the scalar variable
    scalar_var = subset[scalar_name].values
    
    # Get coordinate variables based on the plane
    if dims == ['y', 'x']:
        # (y, x) plane
        x_coord = subset.x.values
        y_coord = subset.y.values
    elif dims == ['z', 'x']:
        # (z, x) plane
        x_coord = subset.x.values
        y_coord = subset.z.values  # Using y_coord to store z-coordinate for consistency
    elif dims == ['z', 'y']:
        # (z, y) plane
        x_coord = subset.y.values  # Using x_coord to store y-coordinate for consistency
        y_coord = subset.z.values
    else:
        raise ValueError(f"Unsupported dimension combination: {dims}")
    
    # Loop through all points
    idx = 0
    for iy in range(ny):
        for ix in range(nx):
            
            # Compute actual physical separation
            dx = fast_shift_2d(x_coord, iy, ix) - x_coord
            dy = fast_shift_2d(y_coord, iy, ix) - y_coord
            
            # Calculate scalar difference
            dscalar = fast_shift_2d(scalar_var, iy, ix) - scalar_var
            
            # Store the separation distances
            dx_vals[idx] = bn.nanmean(dx)
            dy_vals[idx] = bn.nanmean(dy)
            
            # Calculate scalar structure function: dscalar^n
            sf_val = dscalar ** order
            results[idx] = bn.nanmean(sf_val)
            
            idx += 1
            
    return results, dx_vals, dy_vals


def calc_scalar_scalar_2d(subset, variables_names, order, dims, ny, nx):
    """
    Calculate scalar-scalar structure function: (dscalar1^n * dscalar2^k)
    
    Parameters
    ----------
    subset : xarray.Dataset
        Subset of the dataset containing required variables
    variables_names : list
        List of variable names (should contain two scalar variables)
    order : tuple
        Tuple of orders (n, k) for the structure function
    dims, ny, nx : various
        Additional parameters needed for calculation
        
    Returns
    -------
    numpy.ndarray, numpy.ndarray, numpy.ndarray
        Structure function values, DX values, DY values
    """
    if len(variables_names) != 2:
        raise ValueError(f"Scalar-scalar structure function requires exactly 2 scalar components, got {len(variables_names)}")
    
    if not isinstance(order, tuple) or len(order) != 2:
        raise ValueError(f"Order must be a tuple (n, k) for scalar-scalar structure function, got {order}")
    
    # Unpack order tuple
    n, k = order
    
    # Check and reorder variables if needed based on plane
    var1, var2 = variables_names
    
    # Arrays to store results
    results = np.full(ny * nx, np.nan)
    dx_vals = np.full(ny * nx, 0.0)
    dy_vals = np.full(ny * nx, 0.0)
    
    # Get the scalar variable
    scalar_var1 = subset[var1].values
    scalar_var2 = subset[var2].values
    
    # Get coordinate variables based on the plane
    if dims == ['y', 'x']:
        # (y, x) plane
        x_coord = subset.x.values
        y_coord = subset.y.values
    elif dims == ['z', 'x']:
        # (z, x) plane
        x_coord = subset.x.values
        y_coord = subset.z.values  # Using y_coord to store z-coordinate for consistency
    elif dims == ['z', 'y']:
        # (z, y) plane
        x_coord = subset.y.values  # Using x_coord to store y-coordinate for consistency
        y_coord = subset.z.values
    else:
        raise ValueError(f"Unsupported dimension combination: {dims}")
    
    # Loop through all points
    idx = 0
    for iy in range(ny):
        for ix in range(nx):
            
            # Compute actual physical separation
            dx = fast_shift_2d(x_coord, iy, ix) - x_coord
            dy = fast_shift_2d(y_coord, iy, ix) - y_coord
            
            # Calculate scalars difference
            dscalar1 = fast_shift_2d(scalar_var1, iy, ix) - scalar_var1
            dscalar2 = fast_shift_2d(scalar_var2, iy, ix) - scalar_var2
            
            # Store the separation distances
            dx_vals[idx] = bn.nanmean(dx)
            dy_vals[idx] = bn.nanmean(dy)
            
            # Calculate scalar-scalar structure function: dscalar^n * dscalar^k
            sf_val = (dscalar1 ** n) * (dscalar2 ** k)
            results[idx] = bn.nanmean(sf_val)
            
            idx += 1
            
    return results, dx_vals, dy_vals


def calc_longitudinal_transverse_2d(subset, variables_names, order, dims, ny, nx):
    """
    Calculate cross longitudinal-transverse structure function: (du_longitudinal^n * du_transverse^k)
    
    Parameters
    ----------
    subset : xarray.Dataset
        Subset of the dataset containing required variables
    variables_names : list
        List of variable names (should contain two velocity components)
    order : tuple
        Tuple of orders (n, k) for the structure function
    dims, ny, nx : various
        Additional parameters needed for calculation
        
    Returns
    -------
    numpy.ndarray, numpy.ndarray, numpy.ndarray
        Structure function values, DX values, DY values
    """
    if len(variables_names) != 2:
        raise ValueError(f"Longitudinal-transverse structure function requires exactly 2 velocity components, got {len(variables_names)}")
    
    if not isinstance(order, tuple) or len(order) != 2:
        raise ValueError(f"Order must be a tuple (n, k) for longitudinal-transverse structure function, got {order}")
    
    # Unpack order tuple
    n, k = order
    
    # Check and reorder variables if needed based on plane
    var1, var2 = check_and_reorder_variables_2d(variables_names, dims, fun='longitudinal_transverse')
    
    # Arrays to store results
    results = np.full(ny * nx, np.nan)
    dx_vals = np.full(ny * nx, 0.0)
    dy_vals = np.full(ny * nx, 0.0)
    
    # Get the velocity components
    comp1_var = subset[var1].values
    comp2_var = subset[var2].values
    
    # Get coordinate variables based on the plane
    if dims == ['y', 'x']:
        # (y, x) plane
        x_coord = subset.x.values
        y_coord = subset.y.values
    elif dims == ['z', 'x']:
        # (z, x) plane
        x_coord = subset.x.values
        y_coord = subset.z.values  # Using y_coord to store z-coordinate for consistency
    elif dims == ['z', 'y']:
        # (z, y) plane
        x_coord = subset.y.values  # Using x_coord to store y-coordinate for consistency
        y_coord = subset.z.values
    else:
        raise ValueError(f"Unsupported dimension combination: {dims}")
    
    # Loop through all points
    idx = 0
    for iy in range(ny):
        for ix in range(nx):
            
            # Compute actual physical separation
            dx = fast_shift_2d(x_coord, iy, ix) - x_coord
            dy = fast_shift_2d(y_coord, iy, ix) - y_coord
            
            
            # Compute norm of separation vector
            norm = np.maximum(np.sqrt(dx**2 + dy**2), 1.0e-10)
                            
            # Calculate velocity differences
            dcomp1 = fast_shift_2d(comp1_var, iy, ix) - comp1_var
            dcomp2 = fast_shift_2d(comp2_var, iy, ix) - comp2_var
            
            # Store the separation distances
            dx_vals[idx] = bn.nanmean(dx)
            dy_vals[idx] = bn.nanmean(dy)
            
            
            # Project velocity difference onto separation direction (longitudinal)
            delta_parallel = dcomp1 * (dx/norm) + dcomp2 * (dy/norm)
            
            # Calculate perpendicular component (transverse)
            delta_perp = dcomp1 * (dy/norm) - dcomp2 * (dx/norm)
            
            # Calculate longitudinal-transverse structure function: delta_parallel^n * delta_perp^k
            sf_val = (delta_parallel ** n) * (delta_perp ** k)
            results[idx] = bn.nanmean(sf_val)
            
            idx += 1
            
    return results, dx_vals, dy_vals


def calc_longitudinal_scalar_2d(subset, variables_names, order, dims, ny, nx):
    """
    Calculate cross longitudinal-scalar structure function: (du_longitudinal^n * dscalar^k)
    
    Parameters
    ----------
    subset : xarray.Dataset
        Subset of the dataset containing required variables
    variables_names : list
        List of variable names (should contain two velocity components and one scalar)
    order : tuple
        Tuple of orders (n, k) for the structure function
    dims, ny, nx : various
        Additional parameters needed for calculation
        
    Returns
    -------
    numpy.ndarray, numpy.ndarray, numpy.ndarray
        Structure function values, DX values, DY values
    """
    if len(variables_names) != 3:
        raise ValueError(f"Longitudinal-scalar structure function requires 3 variables (2 velocity components and 1 scalar), got {len(variables_names)}")
    
    if not isinstance(order, tuple) or len(order) != 2:
        raise ValueError(f"Order must be a tuple (n, k) for longitudinal-scalar structure function, got {order}")
    
    # Unpack order tuple
    n, k = order
    
    # Check and reorder variables if needed based on plane
    tmp = check_and_reorder_variables_2d(variables_names, dims, fun='longitudinal_scalar')
    vel_vars, scalar_var = tmp[:2], tmp[-1]
    var1, var2 = vel_vars
    
    # Arrays to store results
    results = np.full(ny * nx, np.nan)
    dx_vals = np.full(ny * nx, 0.0)
    dy_vals = np.full(ny * nx, 0.0)
    
    # Get the velocity components and scalar
    comp1_var = subset[var1].values
    comp2_var = subset[var2].values
    scalar_var_values = subset[scalar_var].values
    
    # Get coordinate variables based on the plane
    if dims == ['y', 'x']:
        # (y, x) plane
        x_coord = subset.x.values
        y_coord = subset.y.values
        print(f"Using (y, x) plane with components {var1}, {var2} and scalar {scalar_var}")
    elif dims == ['z', 'x']:
        # (z, x) plane
        x_coord = subset.x.values
        y_coord = subset.z.values  # Using y_coord to store z-coordinate for consistency
        print(f"Using (z, x) plane with components {var1}, {var2} and scalar {scalar_var}")
    elif dims == ['z', 'y']:
        # (z, y) plane
        x_coord = subset.y.values  # Using x_coord to store y-coordinate for consistency
        y_coord = subset.z.values
        print(f"Using (z, y) plane with components {var1}, {var2} and scalar {scalar_var}")
    else:
        raise ValueError(f"Unsupported dimension combination: {dims}")
    
    # Loop through all points
    idx = 0
    for iy in range(ny):
        for ix in range(nx):
            
            # Compute actual physical separation
            dx = fast_shift_2d(x_coord, iy, ix) - x_coord
            dy = fast_shift_2d(y_coord, iy, ix) - y_coord
            
            
            # Compute norm of separation vector
            norm = np.maximum(np.sqrt(dx**2 + dy**2), 1.0e-10)
            
            # Calculate velocity and scalar differences
            dcomp1 = fast_shift_2d(comp1_var, iy, ix) - comp1_var
            dcomp2 = fast_shift_2d(comp2_var, iy, ix) - comp2_var
            dscalar = fast_shift_2d(scalar_var_values, iy, ix) - scalar_var_values
            
            # Store the separation distances
            dx_vals[idx] = bn.nanmean(dx)
            dy_vals[idx] = bn.nanmean(dy)
            
            
            # Project velocity difference onto separation direction (longitudinal)
            delta_parallel = dcomp1 * (dx/norm) + dcomp2 * (dy/norm)
            
            # Calculate longitudinal-scalar structure function: delta_parallel^n * dscalar^k
            sf_val = (delta_parallel ** n) * (dscalar ** k)
            results[idx] = bn.nanmean(sf_val)
            
            idx += 1
            
    return results, dx_vals, dy_vals


def calc_transverse_scalar_2d(subset, variables_names, order, dims, ny, nx):
    """
    Calculate cross transverse-scalar structure function: (du_transverse^n * dscalar^k)
    
    Parameters
    ----------
    subset : xarray.Dataset
        Subset of the dataset containing required variables
    variables_names : list
        List of variable names (should contain two velocity components and one scalar)
    order : tuple
        Tuple of orders (n, k) for the structure function
    dims, ny, nx : various
        Additional parameters needed for calculation
        
    Returns
    -------
    numpy.ndarray, numpy.ndarray, numpy.ndarray
        Structure function values, DX values, DY values
    """
    if len(variables_names) != 3:
        raise ValueError(f"Transverse-scalar structure function requires 3 variables (2 velocity components and 1 scalar), got {len(variables_names)}")
    
    if not isinstance(order, tuple) or len(order) != 2:
        raise ValueError(f"Order must be a tuple (n, k) for transverse-scalar structure function, got {order}")
    
    # Unpack order tuple
    n, k = order
    
    # Check and reorder variables if needed based on plane
    tmp = check_and_reorder_variables_2d(variables_names, dims, fun='transverse_scalar')
    vel_vars, scalar_var = tmp[:2], tmp[-1]
    var1, var2 = vel_vars
    
    # Arrays to store results
    results = np.full(ny * nx, np.nan)
    dx_vals = np.full(ny * nx, 0.0)
    dy_vals = np.full(ny * nx, 0.0)
    
    # Get the velocity components and scalar
    comp1_var = subset[var1].values
    comp2_var = subset[var2].values
    scalar_var_values = subset[scalar_var].values
    
    # Get coordinate variables based on the plane
    if dims == ['y', 'x']:
        # (y, x) plane
        x_coord = subset.x.values
        y_coord = subset.y.values
        print(f"Using (y, x) plane with components {var1}, {var2} and scalar {scalar_var}")
    elif dims == ['z', 'x']:
        # (z, x) plane
        x_coord = subset.x.values
        y_coord = subset.z.values  # Using y_coord to store z-coordinate for consistency
        print(f"Using (z, x) plane with components {var1}, {var2} and scalar {scalar_var}")
    elif dims == ['z', 'y']:
        # (z, y) plane
        x_coord = subset.y.values  # Using x_coord to store y-coordinate for consistency
        y_coord = subset.z.values
        print(f"Using (z, y) plane with components {var1}, {var2} and scalar {scalar_var}")
    else:
        raise ValueError(f"Unsupported dimension combination: {dims}")
    
    # Loop through all points
    idx = 0
    for iy in range(ny):
        for ix in range(nx):
            
            # Compute actual physical separation
            dx = fast_shift_2d(x_coord, iy, ix) - x_coord
            dy = fast_shift_2d(y_coord, iy, ix) - y_coord
            
            
            # Compute norm of separation vector
            norm = np.maximum(np.sqrt(dx**2 + dy**2), 1.0e-10)
            
            
            # Calculate velocity and scalar differences
            dcomp1 = fast_shift_2d(comp1_var, iy, ix) - comp1_var
            dcomp2 = fast_shift_2d(comp2_var, iy, ix) - comp2_var
            dscalar = fast_shift_2d(scalar_var_values, iy, ix) - scalar_var_values
            
            # Store the separation distances
            dx_vals[idx] = bn.nanmean(dx)
            dy_vals[idx] = bn.nanmean(dy)
            
            # Calculate transverse component (perpendicular to separation direction)
            delta_perp = dcomp1 * (dy/norm) - dcomp2 * (dx/norm)
            
            # Calculate transverse-scalar structure function: delta_perp^n * dscalar^k
            sf_val = (delta_perp ** n) * (dscalar ** k)
            results[idx] = bn.nanmean(sf_val)
            
            idx += 1
            
    return results, dx_vals, dy_vals
    
def calc_advective_2d(subset, variables_names, order, dims, ny, nx):
    """
    Calculate advective structure function: (du*deltaadv_u + dv*deltaadv_v)^n
    or (du*deltaadv_u + dw*deltaadv_w)^n or (dv*deltaadv_v + dw*deltaadv_w)^n
    depending on the plane.
    
    Parameters
    ----------
    subset : xarray.Dataset
        Subset of the dataset containing required variables
    variables_names : list
        List of variable names (should contain four velocity components: u, v and adv_u, adv_v)
    order : int
        Order of the structure function
    dims, ny, nx : various
        Additional parameters needed for calculation
        
    Returns
    -------
    numpy.ndarray, numpy.ndarray, numpy.ndarray
        Structure function values, DX values, DY values
    """
    if len(variables_names) != 4:
        raise ValueError(f"Advective structure function requires exactly 4 velocity components, got {len(variables_names)}")
    
    # Extract regular and advective velocity components
    # Identify which are regular velocity components and which are advective
    vel_vars = []
    adv_vars = []
    
    for var in variables_names:
        if var.startswith('adv_') or 'adv' in var.lower():
            adv_vars.append(var)
        else:
            vel_vars.append(var)
    
    # Check if we have the right number of components
    if len(vel_vars) != 2 or len(adv_vars) != 2:
        # If automatic detection fails, try a simpler approach - assume first two are regular velocity
        vel_vars = variables_names[:2]
        adv_vars = variables_names[2:]

    
    # Define expected components based on plane
    if dims == ['y', 'x']:
        expected_components = ['u', 'v']
    elif dims == ['z', 'x']:
        expected_components = ['u', 'w']
    elif dims == ['z', 'y']:
        expected_components = ['v', 'w']
    else:
        raise ValueError(f"Unsupported dimension combination: {dims}")
    
    # Function to map variables to expected components for this plane
    def map_to_components(vars_list, expected):
        if len(vars_list) != len(expected):
            raise ValueError(f"Expected {len(expected)} components, got {len(vars_list)}")
            
        result = [None] * len(expected)
        
        # Try direct matching first
        for i, exp in enumerate(expected):
            for var in vars_list:
                if exp in var.lower():
                    result[i] = var
                    break
        
        # If any component is still None, use order-based matching
        if None in result:

            return vars_list
            
        return result
    
    # Map velocity and advective variables to expected components
    var1, var2 = map_to_components(vel_vars, expected_components)
    advvar1, advvar2 = map_to_components(adv_vars, expected_components)
    
    
    # Arrays to store results
    results = np.full(ny * nx, np.nan)
    dx_vals = np.full(ny * nx, 0.0)
    dy_vals = np.full(ny * nx, 0.0)
    
    # Get the velocity components
    comp1_var = subset[var1].values
    comp2_var = subset[var2].values
    advcomp1_var = subset[advvar1].values
    advcomp2_var = subset[advvar2].values
    
    # Get coordinate variables based on the plane
    if dims == ['y', 'x']:
        # (y, x) plane
        x_coord = subset.x.values
        y_coord = subset.y.values
    elif dims == ['z', 'x']:
        # (z, x) plane
        x_coord = subset.x.values
        y_coord = subset.z.values  # Using y_coord to store z-coordinate for consistency
    elif dims == ['z', 'y']:
        # (z, y) plane
        x_coord = subset.y.values  # Using x_coord to store y-coordinate for consistency
        y_coord = subset.z.values
    
    # Loop through all points
    idx = 0
    for iy in range(ny):
        for ix in range(nx):
            # Compute actual physical separation
            dx = fast_shift_2d(x_coord, iy, ix) - x_coord
            dy = fast_shift_2d(y_coord, iy, ix) - y_coord
            
            # Calculate velocity differences
            dcomp1 = fast_shift_2d(comp1_var, iy, ix) - comp1_var
            dcomp2 = fast_shift_2d(comp2_var, iy, ix) - comp2_var
            
            # Calculate advective velocity differences
            dadvcomp1 = fast_shift_2d(advcomp1_var, iy, ix) - advcomp1_var
            dadvcomp2 = fast_shift_2d(advcomp2_var, iy, ix) - advcomp2_var
            
            # Store the separation distances
            dx_vals[idx] = bn.nanmean(dx)
            dy_vals[idx] = bn.nanmean(dy)
            
            # Calculate advective structure function: (du*deltaadv_u + dv*deltaadv_v)^n
            advective_term = dcomp1 * dadvcomp1 + dcomp2 * dadvcomp2
            sf_val = advective_term ** order
            results[idx] = bn.nanmean(sf_val)
            
            idx += 1
            
    return results, dx_vals, dy_vals


def calc_pressure_work_2d(subset, variables_names, order, dims, ny, nx):
    """
    Calculate pressure work structure function in 2D: (∇_j(δΦ δu_j))^n
    
    Parameters
    ----------
    subset : xarray.Dataset
        Subset of the dataset containing pressure and velocity components
    variables_names : list
        List of variable names (first is pressure, followed by velocity components)
    order : int
        Order of the structure function
    dims : list
        List of dimension names (should be ['y', 'x'], ['z', 'x'], or ['z', 'y'])
    ny, nx : int
        Array dimensions
        
    Returns
    -------
    numpy.ndarray, numpy.ndarray, numpy.ndarray
        Structure function values, DX values, DY values
    """
    if len(variables_names) < 3:  # Need pressure + 2 velocity components
        raise ValueError(f"Pressure work requires pressure and 2 velocity components, got {len(variables_names)}")
    
    # Check valid planes
    if dims not in [['y', 'x'], ['z', 'x'], ['z', 'y']]:
        raise ValueError(f"Dimensions must be one of: ['y', 'x'], ['z', 'x'], or ['z', 'y'], got {dims}")
    
    # Extract variables
    pressure_var = subset[variables_names[0]].values
    comp1_var = subset[variables_names[1]].values
    comp2_var = subset[variables_names[2]].values
    
    # Arrays to store results
    results = np.full(ny * nx, np.nan)
    dx_vals = np.full(ny * nx, 0.0)
    dy_vals = np.full(ny * nx, 0.0)
    
    # Get appropriate coordinate variables based on the plane
    if dims == ['y', 'x']:
        # (y, x) plane
        x_name, y_name = 'x', 'y'
        # Components correspond to u and v
        u_var = comp1_var
        v_var = comp2_var
    elif dims == ['z', 'x']:
        # (z, x) plane
        x_name, y_name = 'x', 'z'
        # Components correspond to u and w
        u_var = comp1_var
        v_var = comp2_var
    elif dims == ['z', 'y']:
        # (z, y) plane
        x_name, y_name = 'y', 'z'
        # Components correspond to v and w
        u_var = comp1_var
        v_var = comp2_var
    
    # Get coordinate variables as 2D arrays
    x_coord = subset[x_name].values
    y_coord = subset[y_name].values
    
    # Convert 1D coordinates to 2D arrays if needed
    if len(x_coord.shape) == 1:
        X, Y = np.meshgrid(x_coord, y_coord)
    else:
        X, Y = x_coord, y_coord
    
    # Loop through all points (we still need to loop over shifts)
    idx = 0
    for iy in range(ny):
        for ix in range(nx):
            # Compute actual physical separation
            dx = fast_shift_2d(X, iy, ix) - X
            dy = fast_shift_2d(Y, iy, ix) - Y
            
            # Store the separation distances
            dx_vals[idx] = bn.nanmean(dx)
            dy_vals[idx] = bn.nanmean(dy)
            
            # Calculate increments at each point
            dP = fast_shift_2d(pressure_var, iy, ix) - pressure_var
            du = fast_shift_2d(u_var, iy, ix) - u_var
            dv = fast_shift_2d(v_var, iy, ix) - v_var
            
            # Calculate the product of pressure and velocity increments at each point
            P_u_flux = dP * du
            P_v_flux = dP * dv
            
            # Calculate divergence using vectorized operations
            div_flux = np.zeros_like(pressure_var)
            
            # Create arrays for coordinate differences (central differences)
            # For x direction
            dx_central = np.zeros_like(X)
            dx_central[:, 1:-1] = (X[:, 2:] - X[:, :-2])
            # Use forward/backward differences at boundaries
            dx_central[:, 0] = (X[:, 1] - X[:, 0]) * 2
            dx_central[:, -1] = (X[:, -1] - X[:, -2]) * 2
            
            # For y direction
            dy_central = np.zeros_like(Y)
            dy_central[1:-1, :] = (Y[2:, :] - Y[:-2, :])
            # Use forward/backward differences at boundaries
            dy_central[0, :] = (Y[1, :] - Y[0, :]) * 2
            dy_central[-1, :] = (Y[-1, :] - Y[-2, :]) * 2
            
            # Calculate flux derivatives using central differences
            dP_u_flux_dx = np.zeros_like(P_u_flux)
            dP_u_flux_dx[:, 1:-1] = (P_u_flux[:, 2:] - P_u_flux[:, :-2]) / dx_central[:, 1:-1]
            # Use forward/backward differences at boundaries
            dP_u_flux_dx[:, 0] = (P_u_flux[:, 1] - P_u_flux[:, 0]) / (dx_central[:, 0] / 2)
            dP_u_flux_dx[:, -1] = (P_u_flux[:, -1] - P_u_flux[:, -2]) / (dx_central[:, -1] / 2)
            
            dP_v_flux_dy = np.zeros_like(P_v_flux)
            dP_v_flux_dy[1:-1, :] = (P_v_flux[2:, :] - P_v_flux[:-2, :]) / dy_central[1:-1, :]
            # Use forward/backward differences at boundaries
            dP_v_flux_dy[0, :] = (P_v_flux[1, :] - P_v_flux[0, :]) / (dy_central[0, :] / 2)
            dP_v_flux_dy[-1, :] = (P_v_flux[-1, :] - P_v_flux[-2, :]) / (dy_central[-1, :] / 2)
            
            # Sum the derivatives to get the divergence
            div_flux = dP_u_flux_dx + dP_v_flux_dy
            
            # Raise to specified order
            sf_val = div_flux ** order
            
            # Compute structure function
            results[idx] = bn.nanmean(sf_val)
            idx += 1
            
    return results, dx_vals, dy_vals
    
    
###################################################################################################

################################Main SF Function###################################################

def calculate_structure_function_2d(ds, dims, variables_names, order, fun='longitudinal', 
                                  nbx=0, nby=0, spacing=None, num_bootstrappable=0, 
                                  bootstrappable_dims=None, boot_indexes=None):
    """
    Main function to calculate structure functions based on specified type.
    
    Parameters
    ----------
    ds : xarray.Dataset
        Dataset containing velocity components and/or scalar fields
    dims : list
        List of dimension names
    variables_names : list
        List of variable names to use, depends on function type
    order : int or tuple
        Order(s) of the structure function
    fun : str, optional
        Type of structure function
    nbx, nby : int, optional
        Bootstrap indices for x and y dimensions
    spacing : dict or int, optional
        Spacing value to use
    num_bootstrappable : int, optional
        Number of bootstrappable dimensions
    bootstrappable_dims : list, optional
        List of bootstrappable dimensions
    boot_indexes : dict, optional
        Dictionary with spacing values as keys and boot indexes as values
        
    Returns
    -------
    numpy.ndarray, numpy.ndarray, numpy.ndarray
        Structure function values, DX values, DY values
    """
    # Start with the full dataset
    subset = ds
    
    # Only subset bootstrappable dimensions
    if num_bootstrappable > 0 and bootstrappable_dims:
        # Get boot indexes for bootstrappable dimensions
        if boot_indexes and spacing is not None:
            if isinstance(spacing, int):
                sp_value = spacing
            else:
                # Get the spacing for a bootstrappable dimension
                for dim in bootstrappable_dims:
                    if dim in spacing:
                        sp_value = spacing[dim]
                        break
                else:
                    sp_value = 1  # Default if no matching dimension found
                
            indexes = boot_indexes.get(sp_value, {}) if sp_value in boot_indexes else {}
        else:
            indexes = {}
        
        # Create subset selection
        subset_dict = {}
        
        if num_bootstrappable == 1:
            # Only one dimension is bootstrappable
            bootstrap_dim = bootstrappable_dims[0]
            # Determine which index (nbx or nby) to use based on which dimension is bootstrappable
            nb_index = nbx if bootstrap_dim == dims[1] else nby
            # Add only the bootstrappable dimension to subset dict
            if indexes and bootstrap_dim in indexes and indexes[bootstrap_dim].shape[1] > nb_index:
                subset_dict[bootstrap_dim] = indexes[bootstrap_dim][:, nb_index]
        else:
            # Both dimensions are bootstrappable
            for i, dim in enumerate(dims):
                nb_index = nby if i == 0 else nbx
                if indexes and dim in indexes and indexes[dim].shape[1] > nb_index:
                    subset_dict[dim] = indexes[dim][:, nb_index]
        
        # Apply subsetting if needed
        if subset_dict:
            subset = ds.isel(subset_dict)
    
    # Check if the required variables exist in the dataset
    for var_name in variables_names:
        if var_name not in subset:
            raise ValueError(f"Variable {var_name} not found in dataset")
    
    # Get dimensions of the first variable to determine array sizes
    ny, nx = subset[variables_names[0]].shape
    
    # Create results array for structure function
    results = np.full(ny * nx, np.nan)
    
    # Arrays to store separation distances
    dx_vals = np.full(ny * nx, 0.0)
    dy_vals = np.full(ny * nx, 0.0)
    
    
    # Calculate structure function based on specified type
    if fun == 'longitudinal':
        results, dx_vals, dy_vals = calc_longitudinal_2d(subset, variables_names, order, 
                                                     dims, ny, nx)
    elif fun == 'transverse':
        results, dx_vals, dy_vals = calc_transverse_2d(subset, variables_names, order, 
                                                   dims, ny, nx)
    elif fun == 'default_vel':
        results, dx_vals, dy_vals = calc_default_vel_2d(subset, variables_names, order, 
                                                    dims, ny, nx)
    elif fun == 'scalar':
        results, dx_vals, dy_vals = calc_scalar_2d(subset, variables_names, order, 
                                              dims, ny, nx)
    elif fun == 'scalar_scalar':
        results, dx_vals, dy_vals = calc_scalar_scalar_2d(subset, variables_names, order, 
                                                     dims, ny, nx)
    elif fun == 'longitudinal_transverse':
        results, dx_vals, dy_vals = calc_longitudinal_transverse_2d(subset, variables_names, order, 
                                                               dims, ny, nx)
    elif fun == 'longitudinal_scalar':
        results, dx_vals, dy_vals = calc_longitudinal_scalar_2d(subset, variables_names, order, 
                                                           dims, ny, nx)
    elif fun == 'transverse_scalar':
        results, dx_vals, dy_vals = calc_transverse_scalar_2d(subset, variables_names, order, 
                                                         dims, ny, nx)
    elif fun == 'advective':
        results, dx_vals, dy_vals = calc_advective_2d(subset, variables_names, order, 
                                                         dims, ny, nx)
    elif fun == 'pressure_work':
        results, dx_vals, dy_vals = calc_pressure_work_2d(subset, variables_names, order, 
                                                         dims, ny, nx)

    else:
        raise ValueError(f"Unsupported function type: {fun}")
    
    return results, dx_vals, dy_vals
###################################################################################################

#####################################Bootstrapping Monte Carlo#######################################################
def run_bootstrap_sf_2d(args):
    """Standalone bootstrap function for parallel processing in 2D."""
    ds, dims, variables_names, order, fun, nbx, nby, spacing, num_bootstrappable, bootstrappable_dims, boot_indexes = args
    return calculate_structure_function_2d(
        ds=ds, dims=dims, variables_names=variables_names, order=order, fun=fun,
        nbx=nbx, nby=nby, spacing=spacing, num_bootstrappable=num_bootstrappable,
        bootstrappable_dims=bootstrappable_dims, boot_indexes=boot_indexes
    )

def monte_carlo_simulation_2d(ds, dims, variables_names, order, nbootstrap, bootsize, 
                            num_bootstrappable, all_spacings, boot_indexes, bootstrappable_dims,
                            fun='longitudinal', spacing=None, n_jobs=-1, backend='threading'):
    """
    Run Monte Carlo simulation for structure function calculation with multiple bootstrap samples.
    """
    # If no bootstrappable dimensions, just calculate once with the full dataset
    if num_bootstrappable == 0:
        print("No bootstrappable dimensions. Calculating structure function once with full dataset.")
        results, dx_vals, dy_vals = calculate_structure_function_2d(
            ds=ds,
            dims=dims,
            variables_names=variables_names,
            order=order, 
            fun=fun,
            num_bootstrappable=num_bootstrappable
        )
        return [results], [dx_vals], [dy_vals]
    
    # Use default spacing of 1 if None provided
    if spacing is None:
        sp_value = 1
    # Convert dict spacing to single value if needed
    elif isinstance(spacing, dict):
        # Get the spacing for a bootstrappable dimension
        for dim in bootstrappable_dims:
            if dim in spacing:
                sp_value = spacing[dim]
                break
        else:
            sp_value = 1  # Default if no matching dimension found
    else:
        sp_value = spacing
    
    # Set the seed for reproducibility
    np.random.seed(10000000)
    
    # Get boot indexes for the specified spacing
    if sp_value in boot_indexes:
        indexes = boot_indexes[sp_value]
    else:
        # Calculate boot indexes on-the-fly
        data_shape = dict(ds.sizes)
        indexes = get_boot_indexes_2d(dims, data_shape, bootsize, all_spacings, boot_indexes, 
                                     bootstrappable_dims, num_bootstrappable, sp_value)
    
    # Create all argument arrays for parallel processing
    all_args = []
    
    # Prepare parameters based on bootstrappable dimensions
    if num_bootstrappable == 1:
        # One bootstrappable dimension - only randomize that dimension
        bootstrap_dim = bootstrappable_dims[0]
        
        if not indexes or bootstrap_dim not in indexes or indexes[bootstrap_dim].shape[1] == 0:
            print(f"Warning: No valid indices for dimension {bootstrap_dim} with spacing {sp_value}.")
            # Fall back to calculating once with full dataset
            results, dx_vals, dy_vals = calculate_structure_function_2d(
                ds=ds,
                dims=dims,
                variables_names=variables_names,
                order=order, 
                fun=fun,
                num_bootstrappable=num_bootstrappable
            )
            return [results], [dx_vals], [dy_vals]
        
        # Generate random indices for the bootstrappable dimension
        random_indices = np.random.choice(indexes[bootstrap_dim].shape[1], size=nbootstrap)
        
        # Create arguments for all bootstrap iterations
        for j in range(nbootstrap):
            if bootstrap_dim == dims[1]:  # x-dimension
                args = (
                    ds, dims, variables_names, order, fun,
                    random_indices[j], 0, sp_value, num_bootstrappable,
                    bootstrappable_dims, boot_indexes
                )
            else:  # y-dimension
                args = (
                    ds, dims, variables_names, order, fun,
                    0, random_indices[j], sp_value, num_bootstrappable,
                    bootstrappable_dims, boot_indexes
                )
            all_args.append(args)
            
    else:
        # Two bootstrappable dimensions - randomize both if possible
        valid_y_indices = dims[0] in indexes and indexes[dims[0]].shape[1] > 0
        valid_x_indices = dims[1] in indexes and indexes[dims[1]].shape[1] > 0
        
        if not valid_y_indices or not valid_x_indices:
            print("Warning: Not enough valid indices for bootstrapping with current spacing.")
            # Fall back to calculating once with full dataset
            results, dx_vals, dy_vals = calculate_structure_function_2d(
                ds=ds,
                dims=dims,
                variables_names=variables_names,
                order=order, 
                fun=fun,
                num_bootstrappable=num_bootstrappable
            )
            return [results], [dx_vals], [dy_vals]
        
        # Generate random indices for both dimensions
        nby = np.random.choice(indexes[dims[0]].shape[1], size=nbootstrap) 
        nbx = np.random.choice(indexes[dims[1]].shape[1], size=nbootstrap)
        
        # Create arguments for all bootstrap iterations
        for j in range(nbootstrap):
            args = (
                ds, dims, variables_names, order, fun,
                nbx[j], nby[j], sp_value, num_bootstrappable,
                bootstrappable_dims, boot_indexes
            )
            all_args.append(args)
    
    # Import modules for memory and system resource management
    import os
    import psutil
    
    # Calculate optimal number of workers
    if n_jobs < 0:  # All negative n_jobs values
        total_cpus = os.cpu_count()
        if n_jobs == -1:  # Special case: use all CPUs
            n_workers = total_cpus
        else:  # Use (all CPUs - |n_jobs| - 1)
            n_workers = max(1, total_cpus + n_jobs + 1)  # +1 because -2 means all except 1
    else:
        n_workers = n_jobs
    
    # Get available system memory
    available_memory = psutil.virtual_memory().available
    
    # Estimate dataset size per task - 2D data can be larger
    # This is a rough estimation based on the dataset structure
    data_size_per_task = ds.nbytes / (ds.dims[dims[0]] * ds.dims[dims[1]])
    # For 2D, we need more memory per task since each task processes multiple grid points
    estimated_task_memory = data_size_per_task * len(variables_names) * ds.dims[dims[0]] * 5
    
    # Calculate optimal batch size based on available resources
    # Balance between memory usage and task distribution
    memory_based_batch_size = int(available_memory / (estimated_task_memory * n_workers * 1.5))
    resource_based_batch_size = max(5, nbootstrap // (n_workers * 2))  # Previous approach
    
    # Use the smaller of the two to be conservative with memory
    batch_size = min(memory_based_batch_size, resource_based_batch_size)
    batch_size = max(1, batch_size)  # At least one task per batch
    
    # Set max_nbytes to protect against memory overflow
    # For 2D data, limit to 75% of available memory for safety
    max_nbytes = int(available_memory * 0.75)
    
    print(f"Running 2D bootstrap with {n_workers} workers")
    print(f"Task batch size: {batch_size} (of {nbootstrap} total bootstraps)")
    print(f"Estimated memory per task: {estimated_task_memory/1024/1024:.2f} MB")
    print(f"Available memory limit for Joblib: {max_nbytes/1024/1024/1024:.2f} GB")
    
    # Run simulations in parallel using the module-level function with memory management
    results = Parallel(n_jobs=n_jobs, verbose=1, batch_size=batch_size, 
                      backend=backend, max_nbytes=max_nbytes)(
        delayed(run_bootstrap_sf_2d)(args) for args in all_args
    )
    
    # Unpack results
    sf_results = [r[0] for r in results]
    dx_vals = [r[1] for r in results]
    dy_vals = [r[2] for r in results]
    
    return sf_results, dx_vals, dy_vals    
#####################################################################################################################

#################################Main 2D Binning Function############################################################
def bin_sf_2d(ds, variables_names, order, bins, bootsize=None, fun='longitudinal', 
            initial_nbootstrap=100, max_nbootstrap=1000, step_nbootstrap=100,
            convergence_eps=0.1, n_jobs=-1, backend='threading'):
    """
    Bin structure function with optimized 2D binning performance.
    
    Parameters
    -----------
    ds : xarray.Dataset
        Dataset containing velocity components and/or scalar fields
    variables_names : list
        List of variable names to use
    order : float or tuple
        Order(s) of the structure function
    bins : dict
        Dictionary with dimensions as keys and bin edges as values
    bootsize : dict, optional
        Dictionary with dimensions as keys and bootsize as values
    fun : str, optional
        Type of structure function
    initial_nbootstrap : int, optional
        Initial number of bootstrap samples
    max_nbootstrap : int, optional
        Maximum number of bootstrap samples
    step_nbootstrap : int, optional
        Step size for increasing bootstrap samples
    convergence_eps : float, optional
        Convergence threshold for bin standard deviation
    n_jobs : int, optional
        Number of jobs for parallel processing
    backend : str, optional
        Backend for joblib: 'threading', 'multiprocessing', or 'loky'. Default is 'threading'.
                
    Returns
    --------
    xarray.Dataset
        Dataset with binned structure function results
    """
    # Initialize and validate dataset
    dims, data_shape, valid_ds = validate_dataset_2d(ds)
    
    # Setup bootsize
    bootsize_dict, bootstrappable_dims, num_bootstrappable = setup_bootsize_2d(dims, data_shape, bootsize)
    
    # Calculate spacings
    spacings_info, all_spacings = calculate_adaptive_spacings_2d(dims, data_shape, bootsize_dict, 
                                                               bootstrappable_dims, num_bootstrappable)
    
    # Compute boot indexes
    boot_indexes = compute_boot_indexes_2d(dims, data_shape, bootsize_dict, all_spacings, bootstrappable_dims)
    
    print("\n" + "="*60)
    print(f"STARTING BIN_SF WITH FUNCTION TYPE: {fun}")
    print(f"Variables: {variables_names}, Order: {order}")
    print(f"Bootstrap parameters: initial={initial_nbootstrap}, max={max_nbootstrap}, step={step_nbootstrap}")
    print(f"Convergence threshold: {convergence_eps}")
    print(f"Bootstrappable dimensions: {bootstrappable_dims} (count: {num_bootstrappable})")
    print("="*60 + "\n")
    
    # Quick validation
    if not isinstance(bins, dict) or not all(dim in bins for dim in dims):
        raise ValueError("'bins' must be a dictionary with all dimensions as keys and bin edges as values")
    
    # Get bin properties
    dims_order = dims
    bins_x = np.array(bins[dims_order[1]])
    bins_y = np.array(bins[dims_order[0]])
    n_bins_x = len(bins_x) - 1
    n_bins_y = len(bins_y) - 1
    
    print(f"Bin dimensions: {dims_order[0]}={n_bins_y}, {dims_order[1]}={n_bins_x}")
    print(f"Total bins: {n_bins_x * n_bins_y}")
    
    # Determine log vs linear bins
    log_bins = {}
    for dim, bin_edges in bins.items():
        if len(bin_edges) < 2:
            raise ValueError(f"Bin edges for dimension '{dim}' must have at least 2 values")
        
        # Quick check for log vs linear bins
        ratios = bin_edges[1:] / bin_edges[:-1]
        ratio_std, ratio_mean = np.std(ratios), np.mean(ratios)
        
        if ratio_std / ratio_mean < 0.01:
            log_bins[dim] = abs(ratio_mean - 1.0) > 0.01  # True for log, False for linear
        else:
            log_bins[dim] = False  # Irregular spacing treated as linear
        
        print(f"Bin type for {dim}: {'logarithmic' if log_bins[dim] else 'linear'}")
    
    # Calculate bin centers
    if log_bins.get(dims_order[1], False):
        x_centers = np.sqrt(bins_x[:-1] * bins_x[1:])
    else:
        x_centers = 0.5 * (bins_x[:-1] + bins_x[1:])
        
    if log_bins.get(dims_order[0], False):
        y_centers = np.sqrt(bins_y[:-1] * bins_y[1:])
    else:
        y_centers = 0.5 * (bins_y[:-1] + bins_y[1:])
    
    # Special case: no bootstrappable dimensions
    if num_bootstrappable == 0:
        print("\nNo bootstrappable dimensions available. "
              "Calculating structure function once with full dataset.")
        
        # Calculate structure function once with the entire dataset
        results, dx_vals, dy_vals = calculate_structure_function_2d(
            ds=valid_ds,
            dims=dims,
            variables_names=variables_names,
            order=order,
            fun=fun,
            num_bootstrappable=num_bootstrappable
        )
        
        # Bin the results
        valid_mask = ~np.isnan(results) & ~np.isnan(dx_vals) & ~np.isnan(dy_vals)
        valid_results = results[valid_mask]
        valid_dx = dx_vals[valid_mask]
        valid_dy = dy_vals[valid_mask]
        
        # Create 2D binning grid
        x_bins_idx = np.clip(np.digitize(valid_dx, bins_x) - 1, 0, n_bins_x - 1)
        y_bins_idx = np.clip(np.digitize(valid_dy, bins_y) - 1, 0, n_bins_y - 1)
        
        # Initialize result arrays
        sf_means = np.full((n_bins_y, n_bins_x), np.nan)
        sf_stds = np.full((n_bins_y, n_bins_x), np.nan)
        point_counts = np.zeros((n_bins_y, n_bins_x), dtype=np.int32)
        
        # Calculate weights (using distances area)
        weights = np.abs(valid_dx*valid_dy)
        
        # Bin the data using unique bin IDs for vectorization
        bin_ids = y_bins_idx * n_bins_x + x_bins_idx
        unique_bins, inverse_indices, counts = np.unique(bin_ids, return_inverse=True, return_counts=True)
        
        # Process each unique bin
        for i, bin_id in enumerate(unique_bins):
            y_idx, x_idx = divmod(bin_id, n_bins_x)
            
            # Get mask for this bin
            bin_mask = inverse_indices == i
            bin_count = counts[i]
            
            # Extract values for this bin
            bin_sf = valid_results[bin_mask]
            bin_weights = weights[bin_mask]
            
            # Update counts
            point_counts[y_idx, x_idx] = bin_count
            
            # Calculate weighted mean
            weight_sum = np.sum(bin_weights)
            if weight_sum > 0:
                norm_weights = bin_weights / weight_sum
                sf_means[y_idx, x_idx] = np.sum(bin_sf * norm_weights)
                sf_stds[y_idx, x_idx] = np.sum(norm_weights * (bin_sf - sf_means[y_idx, x_idx])**2)
        
        # Create output dataset
        ds_binned = xr.Dataset(
            data_vars={
                'sf': ((dims_order[0], dims_order[1]), sf_means),
                'sf_std': ((dims_order[0], dims_order[1]), sf_stds),
                'point_counts': ((dims_order[0], dims_order[1]), point_counts)
            },
            coords={
                dims_order[1]: x_centers,
                dims_order[0]: y_centers
            },
            attrs={
                'bin_type_x': 'logarithmic' if log_bins.get(dims_order[1], False) else 'linear',
                'bin_type_y': 'logarithmic' if log_bins.get(dims_order[0], False) else 'linear',
                'order': str(order),
                'function_type': fun,
                'variables': variables_names,
                'bootstrappable_dimensions': 'none'
            }
        )
        
        # Add bin edges to the dataset
        ds_binned[f'{dims_order[1]}_bins'] = ((dims_order[1], 'edge'), np.column_stack([bins_x[:-1], bins_x[1:]]))
        ds_binned[f'{dims_order[0]}_bins'] = ((dims_order[0], 'edge'), np.column_stack([bins_y[:-1], bins_y[1:]]))
        
        print("2D SF COMPLETED SUCCESSFULLY (no bootstrapping)!")
        print("="*60)
        
        return ds_binned
    
    # Normal bootstrapping case (1 or 2 bootstrappable dimensions)
    # Get available spacings
    spacing_values = all_spacings
    print(f"Available spacings: {spacing_values}")
    
    # Initialize result arrays
    sf_totals = np.zeros((n_bins_y, n_bins_x), dtype=np.float64)
    sf_sq_totals = np.zeros((n_bins_y, n_bins_x), dtype=np.float64)
    weight_totals = np.zeros((n_bins_y, n_bins_x), dtype=np.int32) 
    point_counts = np.zeros((n_bins_y, n_bins_x), dtype=np.int32)
    bin_density = np.zeros((n_bins_y, n_bins_x), dtype=np.float32)
    bin_status = np.zeros((n_bins_y, n_bins_x), dtype=bool)
    bin_bootstraps = np.ones((n_bins_y, n_bins_x), dtype=np.int32) * initial_nbootstrap
    
    # Initialize spacing effectiveness tracking
    bin_spacing_effectiveness = {sp: np.zeros((n_bins_y, n_bins_x), dtype=np.float32) for sp in spacing_values}
    bin_spacing_bootstraps = {sp: np.zeros((n_bins_y, n_bins_x), dtype=np.int32) for sp in spacing_values}
    bin_spacing_counts = {sp: np.zeros((n_bins_y, n_bins_x), dtype=np.int32) for sp in spacing_values}
    
    # Optimized process function with vectorized 2D binning
    def process_spacing_data(sp_value, bootstraps, add_to_counts=True):
        """Process structure function data for a specific spacing value."""
        if bootstraps <= 0:
            return
            
        print(f"  Processing spacing {sp_value} with {bootstraps} bootstraps")
            
        # Run Monte Carlo simulation
        sf_results, dx_vals, dy_vals = monte_carlo_simulation_2d(
            ds=valid_ds,
            dims=dims,
            variables_names=variables_names,
            order=order, 
            nbootstrap=bootstraps, 
            bootsize=bootsize_dict,
            num_bootstrappable=num_bootstrappable,
            all_spacings=all_spacings,
            boot_indexes=boot_indexes,
            bootstrappable_dims=bootstrappable_dims,
            fun=fun, 
            spacing=sp_value,
            n_jobs=n_jobs,
            backend=backend
        )
        
        # Bin tracking for this spacing
        bin_points_added = np.zeros((n_bins_y, n_bins_x), dtype=np.int32)
        
        # Process all bootstrap samples
        for b in range(len(sf_results)):
            sf = sf_results[b]
            dx = dx_vals[b]
            dy = dy_vals[b]
            
            # Create mask for valid values
            valid = ~np.isnan(sf) & ~np.isnan(dx) & ~np.isnan(dy)
            if not np.any(valid):
                continue
                
            sf_valid = sf[valid]
            dx_valid = dx[valid]
            dy_valid = dy[valid]
            
            # Calculate weights as separation distance area
            weights = np.abs(dx_valid*dy_valid)
            
            # PERFORMANCE OPTIMIZATION: Use vectorized bin assignment
            # Create 2D bin indices using numpy's digitize
            x_indices = np.clip(np.digitize(dx_valid, bins_x) - 1, 0, n_bins_x - 1)
            y_indices = np.clip(np.digitize(dy_valid, bins_y) - 1, 0, n_bins_y - 1)
            
            # Create a unique bin ID for each point (much faster than nested loops)
            bin_ids = y_indices * n_bins_x + x_indices
            
            # Use numpy's unique with counts for fast aggregation
            unique_bins, inverse_indices, counts = np.unique(bin_ids, return_inverse=True, return_counts=True)
            
            # Process each unique bin
            for i, bin_id in enumerate(unique_bins):
                y_idx, x_idx = divmod(bin_id, n_bins_x)
                
                # Valid bin check
                if y_idx < 0 or y_idx >= n_bins_y or x_idx < 0 or x_idx >= n_bins_x:
                    continue
                
                # Get mask for this bin
                bin_mask = inverse_indices == i
                bin_count = counts[i]
                
                # Extract values for this bin
                bin_sf = sf_valid[bin_mask]
                bin_weights = weights[bin_mask]
                
                # Update counts
                if add_to_counts:
                    point_counts[y_idx, x_idx] += bin_count
                    bin_points_added[y_idx, x_idx] += bin_count
                    bin_spacing_counts[sp_value][y_idx, x_idx] += bin_count
                
                # Calculate weighted statistics
                weight_sum = np.sum(bin_weights)
                if weight_sum > 0:
                    norm_weights = bin_weights / weight_sum
                    
                    # Update accumulators
                    sf_totals[y_idx, x_idx] += np.sum(bin_sf * norm_weights)
                    sf_sq_totals[y_idx, x_idx] += np.sum((bin_sf**2) * norm_weights)
                    weight_totals[y_idx, x_idx] += 1
        
        # Update spacing effectiveness
        if add_to_counts and bootstraps > 0:
            # Vectorized update of effectiveness
            mask = bin_points_added > 0
            if np.any(mask):
                bin_spacing_effectiveness[sp_value][mask] = bin_points_added[mask] / bootstraps
                bin_spacing_bootstraps[sp_value][mask] += bootstraps
        
        # Clean memory
        del sf_results, dx_vals, dy_vals
        gc.collect()
    
    # Process initial bootstraps
    print("\nINITIAL BOOTSTRAP PHASE")
    init_samples_per_spacing = max(5, initial_nbootstrap // len(spacing_values))
    for sp_value in spacing_values:
        process_spacing_data(sp_value, init_samples_per_spacing, True)
    
    # Calculate bin density
    print("\nCALCULATING BIN DENSITIES")
    total_points = np.sum(point_counts)
    if total_points > 0:
        # Calculate all bin areas at once
        x_widths = bins_x[1:] - bins_x[:-1]
        y_widths = bins_y[1:] - bins_y[:-1]
        bin_areas = np.outer(y_widths, x_widths)
        
        # Vectorized density calculation
        bin_density = np.divide(point_counts, bin_areas * total_points, 
                              out=np.zeros_like(bin_density, dtype=np.float32), 
                              where=bin_areas > 0)
    
    # Normalize density
    max_density = np.max(bin_density) if np.any(bin_density > 0) else 1.0
    if max_density > 0:
        bin_density /= max_density
    
    print(f"Total points collected: {total_points}")
    print(f"Bins with points: {np.count_nonzero(point_counts)}/{n_bins_x * n_bins_y}")
    print(f"Maximum density bin has {np.max(point_counts)} points")
    
    # Calculate adaptive steps
    bootstrap_steps = np.maximum(
        step_nbootstrap, 
        (step_nbootstrap * (1 + 2 * bin_density)).astype(int)
    )
    
    # Fast calculation of statistics
    def calculate_bin_statistics():
        means = np.full((n_bins_y, n_bins_x), np.nan)
        stds = np.full((n_bins_y, n_bins_x), np.nan)
        
        # Only calculate for bins with data
        valid_bins = weight_totals > 0
        if np.any(valid_bins):
            means[valid_bins] = sf_totals[valid_bins] / weight_totals[valid_bins]
        
        # Calculate variance and std for bins with enough samples
        valid_var_bins = weight_totals > 1
        if np.any(valid_var_bins):
            variance = np.zeros_like(sf_totals)
            variance[valid_var_bins] = (sf_sq_totals[valid_var_bins] / weight_totals[valid_var_bins]) - (means[valid_var_bins]**2)
            stds[valid_var_bins] = np.sqrt(np.maximum(0, variance[valid_var_bins]))
        
        return means, stds
    
    # Calculate initial statistics
    print("\nCALCULATING INITIAL STATISTICS")
    sf_means, sf_stds = calculate_bin_statistics()
    
    # Mark bins with too few points as converged
    low_density_mask = (point_counts <= 10) & ~bin_status
    bin_status |= low_density_mask
    print(f"Marked {np.sum(low_density_mask)} low-density bins (< 10 points) as converged")

    # Mark bins with NaN standard deviations as converged
    nan_std_mask = np.isnan(sf_stds) & ~bin_status
    bin_status |= nan_std_mask
    print(f"Marked {np.sum(nan_std_mask)} bins with NaN standard deviations as converged")

    # Mark early converged bins
    early_converged = (sf_stds <= convergence_eps) & ~bin_status & (point_counts > 10)
    bin_status |= early_converged
    print(f"Marked {np.sum(early_converged)} bins as early-converged (std <= {convergence_eps})")
    
    # Main convergence loop
    iteration = 1
    
    print("\nSTARTING ADAPTIVE CONVERGENCE LOOP")
    while True:
        # Find unconverged bins
        unconverged = ~bin_status & (point_counts > 10) & (bin_bootstraps < max_nbootstrap)
        if not np.any(unconverged):
            print("All bins have converged or reached max bootstraps!")
            break
            
        print(f"\nIteration {iteration} - {np.sum(unconverged)} unconverged bins")
        
        # Create density-ordered bin list
        bin_list = []
        y_idxs, x_idxs = np.where(unconverged)
        for j, i in zip(y_idxs, x_idxs):
            bin_list.append((j, i, bin_density[j, i]))
        
        # Sort by density (highest first)
        bin_list.sort(key=lambda x: x[2], reverse=True)
        
        # Track how many bins converged in this iteration
        bins_converged_in_iteration = 0
        max_reached_in_iteration = 0
        
        # Process bins in order of decreasing density
        for bin_idx, (j, i, density) in enumerate(bin_list):
            # Skip if already converged
            if bin_status[j, i]:
                continue
                
            print(f"\nProcessing bin ({j},{i}) - Density: {density:.4f} - " + 
                 f"Current bootstraps: {bin_bootstraps[j, i]} - " + 
                 f"Current std: {sf_stds[j, i]:.6f} - " + 
                 f"Points: {point_counts[j, i]}")
                 
            # Use exact bootstrap step value
            step = bootstrap_steps[j, i]
            print(f"  Adding {step} more bootstraps to bin ({j},{i})")
            
            # Calculate spacing effectiveness for this bin
            spacing_effectiveness = {sp: bin_spacing_effectiveness[sp][j, i] for sp in spacing_values}
            
            # Sort spacings by effectiveness (highest first)
            sorted_spacings = sorted(spacing_effectiveness.items(), key=lambda x: x[1], reverse=True)
            
            # Use multi-spacing approach but more efficiently
            total_additional = 0
            remaining_step = step
            
            # Process all spacings based on their effectiveness
            total_effectiveness = sum(eff for _, eff in sorted_spacings if eff > 0)
            
            # Distribute bootstraps proportionally to effectiveness
            for sp_value, effectiveness in sorted_spacings:
                # Skip ineffective spacings
                if effectiveness <= 0: 
                    continue
                
                # Calculate proportion based on effectiveness
                if total_effectiveness > 0:
                    proportion = effectiveness / total_effectiveness
                    sp_additional = int(step * proportion)
                else:
                    sp_additional = 0.0
                
                sp_additional = min(sp_additional, remaining_step)
                
                # Process this spacing
                process_spacing_data(sp_value, sp_additional, False)
                
                # Update counters
                total_additional += sp_additional
                remaining_step -= sp_additional
                
                # Stop if we've allocated all bootstraps
                if remaining_step <= 0:
                    break
            
            # Update bootstrap counts
            bin_bootstraps[j, i] += total_additional
            
            # Recalculate statistics
            sf_means, sf_stds = calculate_bin_statistics()
            
            # Check for convergence or max bootstraps
            if sf_stds[j, i] <= convergence_eps:
                bin_status[j, i] = True
                print(f"  Bin ({j},{i}) CONVERGED after additional bootstraps with std {sf_stds[j, i]:.6f} <= {convergence_eps}")
                bins_converged_in_iteration += 1
            elif bin_bootstraps[j, i] >= max_nbootstrap:
                bin_status[j, i] = True
                print(f"  Bin ({j},{i}) reached MAX BOOTSTRAPS {max_nbootstrap}")
                max_reached_in_iteration += 1
        
        # Next iteration
        iteration += 1
        gc.collect()
    
    # Final convergence statistics
    converged_bins = np.sum(bin_status & (point_counts > 10))
    unconverged_bins = np.sum(~bin_status & (point_counts > 10))
    max_bootstrap_bins = np.sum((bin_bootstraps >= max_nbootstrap) & (point_counts > 10))
    
    print("\nFINAL CONVERGENCE STATISTICS:")
    print(f"  Total bins with data more than 10 points: {np.sum(point_counts > 10)}")
    print(f"  Converged bins: {converged_bins}")
    print(f"  Unconverged bins: {unconverged_bins}")
    print(f"  Bins at max bootstraps: {max_bootstrap_bins}")
    
    # Create output dataset
    print("\nCreating output dataset...")
    coord_dims = {
        dims_order[1]: x_centers,
        dims_order[0]: y_centers
    }
    
    ds_binned = xr.Dataset(
        data_vars={
            'sf': ((dims_order[0], dims_order[1]), sf_means),
            'sf_std': ((dims_order[0], dims_order[1]), sf_stds),
            'nbootstraps': ((dims_order[0], dims_order[1]), bin_bootstraps),
            'density': ((dims_order[0], dims_order[1]), bin_density),
            'point_counts': ((dims_order[0], dims_order[1]), point_counts),
            'converged': ((dims_order[0], dims_order[1]), bin_status)
        },
        coords=coord_dims,
        attrs={
            'bin_type_x': 'logarithmic' if log_bins.get(dims_order[1], False) else 'linear',
            'bin_type_y': 'logarithmic' if log_bins.get(dims_order[0], False) else 'linear',
            'convergence_eps': convergence_eps,
            'max_nbootstrap': max_nbootstrap,
            'initial_nbootstrap': initial_nbootstrap,
            'order': str(order),
            'function_type': fun,
            'spacing_values': list(spacing_values),
            'variables': variables_names,
            'bootstrappable_dimensions': ','.join(bootstrappable_dims),
            'backend': backend
        }
    )
    
    # Add bin edges to the dataset
    ds_binned[f'{dims_order[1]}_bins'] = ((dims_order[1], 'edge'), np.column_stack([bins_x[:-1], bins_x[1:]]))
    ds_binned[f'{dims_order[0]}_bins'] = ((dims_order[0], 'edge'), np.column_stack([bins_y[:-1], bins_y[1:]]))
    
    print("2D SF COMPLETED SUCCESSFULLY!")
    print("="*60)
    
    return ds_binned
#####################################################################################################################

##############################################Isotropic 2D SF########################################################
def get_isotropic_sf_2d(ds, variables_names, order=2.0, bins=None, bootsize=None,
                      initial_nbootstrap=100, max_nbootstrap=1000, 
                      step_nbootstrap=100, fun='longitudinal', 
                      n_bins_theta=36, window_size_theta=None, window_size_r=None,
                      convergence_eps=0.1, n_jobs=-1, backend='threading'):
    """
    Get isotropic (radially binned) structure function results.
    
    Parameters
    -----------
    ds : xarray.Dataset
        Dataset containing velocity components and/or scalar fields
    variables_names : list
        List of variable names to use
    order : float or tuple
        Order(s) of the structure function
    bins : dict
        Dictionary with 'r' as key and bin edges as values
    bootsize : dict, optional
        Dictionary with dimensions as keys and bootsize as values
    initial_nbootstrap : int, optional
        Initial number of bootstrap samples
    max_nbootstrap : int, optional
        Maximum number of bootstrap samples
    step_nbootstrap : int, optional
        Step size for increasing bootstrap samples
    fun : str, optional
        Type of structure function
    n_bins_theta : int, optional
        Number of angular bins
    window_size_theta : int, optional
        Window size for theta bootstrapping
    window_size_r : int, optional
        Window size for radial bootstrapping
    convergence_eps : float, optional
        Convergence threshold for bin standard deviation
    n_jobs : int, optional
        Number of jobs for parallel processing
    backend : str, optional
        Backend for joblib: 'threading', 'multiprocessing', or 'loky'. Default is 'threading'.
    
    Returns
    --------
    xarray.Dataset
        Dataset with isotropic structure function results
    """
    # Initialize and validate dataset
    dims, data_shape, valid_ds = validate_dataset_2d(ds)
    
    # Setup bootsize
    bootsize_dict, bootstrappable_dims, num_bootstrappable = setup_bootsize_2d(dims, data_shape, bootsize)
    
    # Calculate spacings
    spacings_info, all_spacings = calculate_adaptive_spacings_2d(dims, data_shape, bootsize_dict, 
                                                               bootstrappable_dims, num_bootstrappable)
    
    # Compute boot indexes
    boot_indexes = compute_boot_indexes_2d(dims, data_shape, bootsize_dict, all_spacings, bootstrappable_dims)
    
    print("\n" + "="*60)
    print(f"STARTING ISOTROPIC_SF WITH FUNCTION TYPE: {fun}")
    print(f"Variables: {variables_names}, Order: {order}")
    print(f"Bootstrap parameters: initial={initial_nbootstrap}, max={max_nbootstrap}, step={step_nbootstrap}")
    print(f"Convergence threshold: {convergence_eps}")
    print(f"Bootstrappable dimensions: {bootstrappable_dims} (count: {num_bootstrappable})")
    print("="*60 + "\n")
    
    # Validate bins
    if bins is None or 'r' not in bins:
        raise ValueError("'bins' must be a dictionary with 'r' as key and bin edges as values")
    
    r_bins = np.array(bins['r'])
    if len(r_bins) < 2:
        raise ValueError("Bin edges for 'r' must have at least 2 values")
    
    # Determine bin type (log or linear)
    ratios = r_bins[1:] / r_bins[:-1]
    ratio_std = np.std(ratios)
    ratio_mean = np.mean(ratios)
    
    if ratio_std / ratio_mean < 0.01:
        if np.abs(ratio_mean - 1.0) < 0.01:
            log_bins = False  # Linear bins
            r_centers = 0.5 * (r_bins[:-1] + r_bins[1:])
            print("Detected linear binning for radial dimension")
        else:
            log_bins = True  # Log bins
            r_centers = np.sqrt(r_bins[:-1] * r_bins[1:])
            print("Detected logarithmic binning for radial dimension")
    else:
        log_bins = False  # Default to linear if irregular spacing
        r_centers = 0.5 * (r_bins[:-1] + r_bins[1:])
        print("Detected irregular bin spacing for radial dimension, treating as linear")
    
    n_bins_r = len(r_centers)
    
    # Default window sizes if not provided
    if window_size_theta is None:
        window_size_theta = max(n_bins_theta // 3, 1)
    if window_size_r is None:
        window_size_r = max(n_bins_r // 3, 1)
    
    print(f"Using {n_bins_r} radial bins and {n_bins_theta} angular bins")
    print(f"Using window size {window_size_theta} for theta and {window_size_r} for r")
    
    # Set up angular bins (full circle)
    theta_bins = np.linspace(-np.pi, np.pi, n_bins_theta + 1)
    theta_centers = 0.5 * (theta_bins[:-1] + theta_bins[1:])
    
    # Special case: no bootstrappable dimensions
    if num_bootstrappable == 0:
        print("\nNo bootstrappable dimensions available. "
              "Calculating structure function once with full dataset.")
        
        # Calculate structure function once with the entire dataset
        results, dx_vals, dy_vals = calculate_structure_function_2d(
            ds=valid_ds,
            dims=dims,
            variables_names=variables_names,
            order=order,
            fun=fun,
            num_bootstrappable=num_bootstrappable
        )
        
        # Filter out invalid values
        valid_mask = ~np.isnan(results) & ~np.isnan(dx_vals) & ~np.isnan(dy_vals)
        valid_results = results[valid_mask]
        valid_dx = dx_vals[valid_mask]
        valid_dy = dy_vals[valid_mask]
        
        if len(valid_results) == 0:
            raise ValueError("No valid results found to bin")
        
        # Convert to polar coordinates
        r_valid = np.sqrt(valid_dx**2 + valid_dy**2)
        theta_valid = np.arctan2(valid_dy, valid_dx)
        
        # Create radial bin indices using numpy's digitize
        r_indices = np.clip(np.digitize(r_valid, r_bins) - 1, 0, n_bins_r - 1)
        theta_indices = np.clip(np.digitize(theta_valid, theta_bins) - 1, 0, n_bins_theta - 1)
        
        # Initialize arrays for binning
        sf_means = np.full(n_bins_r, np.nan)
        sf_stds = np.full(n_bins_r, np.nan)
        point_counts = np.zeros(n_bins_r, dtype=np.int32)
        sfr = np.full((n_bins_theta, n_bins_r), np.nan)
        sfr_counts = np.zeros((n_bins_theta, n_bins_r), dtype=np.int32)
        
        # Calculate weights (using distance)
        weights = r_valid
        
        # Process radial bins
        for r_idx in range(n_bins_r):
            # Get mask for this radial bin
            r_bin_mask = r_indices == r_idx
            if not np.any(r_bin_mask):
                continue
                
            # Extract values for this bin
            bin_sf = valid_results[r_bin_mask]
            bin_weights = weights[r_bin_mask]
            bin_thetas = theta_valid[r_bin_mask]
            bin_theta_indices = theta_indices[r_bin_mask]
                
            # Update counts
            point_counts[r_idx] = np.sum(r_bin_mask)
            
            # Calculate weighted mean
            weight_sum = np.sum(bin_weights)
            if weight_sum > 0:
                norm_weights = bin_weights / weight_sum
                sf_means[r_idx] = np.sum(bin_sf * norm_weights)
                sf_stds[r_idx] = np.sqrt(np.sum(norm_weights * (bin_sf - sf_means[r_idx])**2))
            
            # Process angular bins for this radial bin
            for theta_idx in range(n_bins_theta):
                # Get mask for this angular-radial bin
                theta_bin_mask = bin_theta_indices == theta_idx
                if not np.any(theta_bin_mask):
                    continue
                
                # Extract values for this angular-radial bin
                theta_sf = bin_sf[theta_bin_mask]
                theta_weights = bin_weights[theta_bin_mask]
                theta_weight_sum = np.sum(theta_weights)
                
                if theta_weight_sum > 0:
                    # Calculate weighted average
                    theta_norm_weights = theta_weights / theta_weight_sum
                    sfr[theta_idx, r_idx] = np.sum(theta_sf * theta_norm_weights)
                    sfr_counts[theta_idx, r_idx] = np.sum(theta_bin_mask)

        # Calculate confidence intervals
        confidence_level = 0.95
        z_score = stats.norm.ppf((1 + confidence_level) / 2)
        ci_upper = np.full_like(sf_means, np.nan)
        ci_lower = np.full_like(sf_means, np.nan)
        
        # For bins with data
        valid_bins = ~np.isnan(sf_means)
        if np.any(valid_bins):
            # If we have enough points, use standard error
            bins_with_multiple_points = (point_counts[valid_bins] > 1)
            if np.any(bins_with_multiple_points):
                indices = np.where(valid_bins)[0][bins_with_multiple_points]
                ci_upper[indices] = sf_means[indices] + z_score * sf_stds[indices] / np.sqrt(point_counts[indices])
                ci_lower[indices] = sf_means[indices] - z_score * sf_stds[indices] / np.sqrt(point_counts[indices])
            
            # For bins with only one point, just use the mean
            bins_with_one_point = (point_counts[valid_bins] == 1)
            if np.any(bins_with_one_point):
                indices = np.where(valid_bins)[0][bins_with_one_point]
                ci_upper[indices] = sf_means[indices]
                ci_lower[indices] = sf_means[indices]
        
        # Calculate error metrics
        # Calculate error metrics for final results
        print("\nCalculating error metrics and confidence intervals...")
        
        # Error of isotropy
        eiso = np.zeros(n_bins_r)
        
        # Create sliding windows for theta bootstrapping
        if n_bins_theta > window_size_theta:
            indices_theta = sliding_window_view(
                np.arange(n_bins_theta), 
                (n_bins_theta - window_size_theta + 1,), 
                writeable=False
            )[::1]
            
            n_samples_theta = len(indices_theta)
            
            for i in range(n_samples_theta):
                idx = indices_theta[i]
                mean_sf = bn.nanmean(sfr[idx, :], axis=0)
                eiso += np.abs(mean_sf - sf_means)
            
            eiso /= max(1, n_samples_theta)  # Avoid division by zero
        else:
            print("Warning: Window size for theta is too large. Skipping isotropy error calculation.")
        
        # Create sliding windows for r bootstrapping
        if n_bins_r > window_size_r:
            indices_r = sliding_window_view(
                np.arange(n_bins_r), 
                (n_bins_r - window_size_r + 1,), 
                writeable=False
            )[::1]
            
            n_samples_r = len(indices_r)
            
            # Use a subset of bins for homogeneity
            r_subset = r_centers[indices_r[0]]
            
            # Calculate mean across all angles
            meanh = np.zeros(len(r_subset))
            ehom = np.zeros(len(r_subset))
            
            for i in range(n_samples_r):
                idx = indices_r[i]
                meanh += bn.nanmean(sfr[:, idx], axis=0)
            
            meanh /= max(1, n_samples_r)  # Avoid division by zero
            
            for i in range(n_samples_r):
                idx = indices_r[i]
                ehom += np.abs(bn.nanmean(sfr[:, idx], axis=0) - meanh)
            
            ehom /= max(1, n_samples_r)  # Avoid division by zero
        else:
            print("Warning: Window size for r is too large. Using all r bins instead.")
            r_subset = r_centers
            meanh = bn.nanmean(sfr, axis=0)
            ehom = np.zeros_like(meanh)
        
        # Create output dataset
        ds_iso = xr.Dataset(
            data_vars={
                'sf_polar': (('theta', 'r'), sfr),  # Angular-radial values
                'sf': (('r'), sf_means),  # Isotropic values
                'error_isotropy': (('r'), eiso),  # Isotropy error
                'std': (('r'), sf_stds),  # Standard deviation
                'ci_upper': (('r'), ci_lower),  # Upper confidence interval
                'ci_lower': (('r'), ci_upper),  # Lower confidence interval
                'error_homogeneity': (('r_subset'), ehom),  # Homogeneity error
                'point_counts': (('r'), point_counts),  # Point counts
            },
            coords={
                'r': r_centers,
                'r_subset':r_subset,
                'theta': theta_centers
            },
            attrs={
                'order': str(order),
                'function_type': fun,
                'window_size_theta': window_size_theta,
                'window_size_r': window_size_r,
                'bin_type': 'logarithmic' if log_bins else 'linear',
                'variables': variables_names,
                'bootstrappable_dimensions': 'none'
            }
        )
        
        # Add bin edges to the dataset
        ds_iso['r_bins'] = (('r_edge'), r_bins)
        ds_iso['theta_bins'] = (('theta_edge'), theta_bins)
        
        print("ISOTROPIC SF COMPLETED SUCCESSFULLY (no bootstrapping)!")
        print("="*60)
        
        return ds_iso
    
    # Normal bootstrapping case (1 or 2 bootstrappable dimensions)
    # Get available spacings
    spacing_values = all_spacings
    print(f"Available spacings: {spacing_values}")
    
    # Initialize result arrays for vectorized operations
    sf_totals = np.zeros(n_bins_r, dtype=np.float64)       # Sum(sf * weight)
    sf_sq_totals = np.zeros(n_bins_r, dtype=np.float64)    # Sum(sf^2 * weight)
    weight_totals = np.zeros(n_bins_r, dtype=np.int32)     # Sum(weight)
    point_counts = np.zeros(n_bins_r, dtype=np.int32)      # Points per bin
    bin_density = np.zeros(n_bins_r, dtype=np.float32)     # Bin density distribution
    bin_status = np.zeros(n_bins_r, dtype=bool)            # Convergence status
    bin_bootstraps = np.ones(n_bins_r, dtype=np.int32) * initial_nbootstrap  # Bootstraps per bin
    
    # Arrays for angular-radial bins
    sfr = np.full((n_bins_theta, n_bins_r), np.nan)        # Angular-radial values
    sfr_counts = np.zeros((n_bins_theta, n_bins_r), dtype=np.int32)  # Counts per bin
    
    # Initialize spacing effectiveness tracking for adaptive sampling
    bin_spacing_effectiveness = {sp: np.zeros(n_bins_r, dtype=np.float32) for sp in spacing_values}
    bin_spacing_bootstraps = {sp: np.zeros(n_bins_r, dtype=np.int32) for sp in spacing_values}
    bin_spacing_counts = {sp: np.zeros(n_bins_r, dtype=np.int32) for sp in spacing_values}
    
    # Optimized process function with vectorized binning
    def process_spacing_data(sp_value, bootstraps, add_to_counts=True):
        """
        Process data for a specific spacing value with the specified number of bootstraps
        
        Parameters
        ----------
        sp_value : int
            Spacing value to use
        bootstraps : int
            Number of bootstrap samples to run
        add_to_counts : bool
            Whether to add points to bin counts for density calculation
        """
        if bootstraps <= 0:
            return
            
        print(f"  Processing spacing {sp_value} with {bootstraps} bootstraps")
            
        # Run Monte Carlo simulation
        sf_results, dx_vals, dy_vals = monte_carlo_simulation_2d(
            ds=valid_ds,
            dims=dims,
            variables_names=variables_names,
            order=order, 
            nbootstrap=bootstraps, 
            bootsize=bootsize_dict,
            num_bootstrappable=num_bootstrappable,
            all_spacings=all_spacings,
            boot_indexes=boot_indexes,
            bootstrappable_dims=bootstrappable_dims,
            fun=fun, 
            spacing=sp_value,
            n_jobs=n_jobs,
            backend=backend
        )
        
        # Bin tracking for this spacing
        bin_points_added = np.zeros(n_bins_r, dtype=np.int32)
        
        # Process all bootstrap samples
        for b in range(len(sf_results)):
            sf = sf_results[b]
            dx = dx_vals[b]
            dy = dy_vals[b]
            
            # Create mask for valid values
            valid = ~np.isnan(sf) & ~np.isnan(dx) & ~np.isnan(dy)
            if not np.any(valid):
                continue
                
            # Extract valid values
            sf_valid = sf[valid]
            dx_valid = dx[valid]
            dy_valid = dy[valid]
            
            # Convert to polar coordinates
            r_valid = np.sqrt(dx_valid**2 + dy_valid**2)
            theta_valid = np.arctan2(dy_valid, dx_valid)
            
            # Calculate weights as separation distance
            weights = r_valid
            
            # PERFORMANCE OPTIMIZATION: Use vectorized bin assignment
            # Create radial bin indices using numpy's digitize
            r_indices = np.clip(np.digitize(r_valid, r_bins) - 1, 0, n_bins_r - 1)
            theta_indices = np.clip(np.digitize(theta_valid, theta_bins) - 1, 0, n_bins_theta - 1)
            
            # Create unique bin IDs for vectorized processing
            r_bin_ids = np.unique(r_indices)
            
            # Process each unique radial bin
            for r_bin_id in r_bin_ids:
                # Get mask for this radial bin
                r_bin_mask = r_indices == r_bin_id
                if not np.any(r_bin_mask):
                    continue
                
                # Extract values for this bin
                bin_sf = sf_valid[r_bin_mask]
                bin_weights = weights[r_bin_mask]
                bin_thetas = theta_valid[r_bin_mask]
                bin_theta_indices = theta_indices[r_bin_mask]
                
                # Update counts if tracking
                if add_to_counts:
                    bin_count = np.sum(r_bin_mask)
                    point_counts[r_bin_id] += bin_count
                    bin_points_added[r_bin_id] += bin_count
                    bin_spacing_counts[sp_value][r_bin_id] += bin_count
                
                # Calculate weighted statistics for radial bin
                weight_sum = np.sum(bin_weights)
                if weight_sum > 0:
                    norm_weights = bin_weights / weight_sum
                    
                    # Update accumulators with vectorized operations
                    sf_totals[r_bin_id] += np.sum(bin_sf * norm_weights)
                    sf_sq_totals[r_bin_id] += np.sum((bin_sf**2) * norm_weights)
                    weight_totals[r_bin_id] += 1
                
                # Process angular bins within this radial bin
                # Get unique theta bins for this radial bin
                theta_bin_ids = np.unique(bin_theta_indices)
                
                for theta_bin_id in theta_bin_ids:
                    # Get mask for this angular-radial bin
                    theta_bin_mask = bin_theta_indices == theta_bin_id
                    if not np.any(theta_bin_mask):
                        continue
                    
                    # Extract values for this angular-radial bin
                    theta_sf = bin_sf[theta_bin_mask]
                    theta_weights = bin_weights[theta_bin_mask]
                    theta_weight_sum = np.sum(theta_weights)
                    
                    if theta_weight_sum > 0:
                        # Calculate weighted average
                        theta_norm_weights = theta_weights / theta_weight_sum
                        theta_weighted_sf = np.sum(theta_sf * theta_norm_weights)
                        
                        # Update angular-radial matrix
                        if np.isnan(sfr[theta_bin_id, r_bin_id]):
                            sfr[theta_bin_id, r_bin_id] = theta_weighted_sf
                        else:
                            # Weighted average with previous value
                            sfr[theta_bin_id, r_bin_id] = (sfr[theta_bin_id, r_bin_id] * sfr_counts[theta_bin_id, r_bin_id] + theta_weighted_sf) / (sfr_counts[theta_bin_id, r_bin_id] + 1)
                        
                        sfr_counts[theta_bin_id, r_bin_id] += 1
        
        # Update spacing effectiveness after processing all bootstraps
        if add_to_counts and bootstraps > 0:
            # Vectorized update of effectiveness
            mask = bin_points_added > 0
            if np.any(mask):
                bin_spacing_effectiveness[sp_value][mask] = bin_points_added[mask] / bootstraps
                bin_spacing_bootstraps[sp_value][mask] += bootstraps
        
        # Clean memory
        del sf_results, dx_vals, dy_vals
        gc.collect()
    
    # Process initial bootstraps
    print("\nINITIAL BOOTSTRAP PHASE")
    init_samples_per_spacing = max(5, initial_nbootstrap // len(spacing_values))
    for sp_value in spacing_values:
        process_spacing_data(sp_value, init_samples_per_spacing, True)
    
    # Calculate bin density for adaptive sampling
    print("\nCALCULATING BIN DENSITIES")
    total_points = np.sum(point_counts)
    if total_points > 0:
        # Calculate all bin areas at once
        bin_areas = np.pi * (r_bins[1:]**2 - r_bins[:-1]**2)
        
        # Vectorized density calculation
        bin_density = np.divide(point_counts, bin_areas * total_points, 
                              out=np.zeros_like(bin_density, dtype=np.float32), 
                              where=bin_areas > 0)
    
    # Normalize density
    max_density = np.max(bin_density) if np.any(bin_density > 0) else 1.0
    if max_density > 0:
        bin_density /= max_density
    
    print(f"Total points collected: {total_points}")
    print(f"Bins with points: {np.count_nonzero(point_counts)}/{n_bins_r}")
    print(f"Maximum density bin has {np.max(point_counts)} points")
    
    # Calculate adaptive step sizes based on density
    bootstrap_steps = np.maximum(
        step_nbootstrap, 
        (step_nbootstrap * (1 + 2 * bin_density)).astype(int)
    )
    
    # Fast vectorized calculation of bin statistics
    def calculate_bin_statistics():
        """
        Calculate current weighted means and standard deviations for all bins
        
        Returns
        -------
        tuple
            (means, stds) arrays of weighted means and standard deviations
        """
        means = np.full(n_bins_r, np.nan)
        stds = np.full(n_bins_r, np.nan)
        
        # Only calculate for bins with data
        valid_bins = weight_totals > 0
        if np.any(valid_bins):
            means[valid_bins] = sf_totals[valid_bins] / weight_totals[valid_bins]
        
        # Calculate variance and std for bins with enough samples
        valid_var_bins = weight_totals > 1
        if np.any(valid_var_bins):
            variance = np.zeros_like(sf_totals)
            variance[valid_var_bins] = (sf_sq_totals[valid_var_bins] / weight_totals[valid_var_bins]) - (means[valid_var_bins]**2)
            stds[valid_var_bins] = np.sqrt(np.maximum(0, variance[valid_var_bins]))
        
        return means, stds
    
    # Calculate initial statistics
    print("\nCALCULATING INITIAL STATISTICS")
    sf_means, sf_stds = calculate_bin_statistics()
    
    # Mark bins with too few points as converged
    low_density_mask = (point_counts <= 10) & ~bin_status
    bin_status |= low_density_mask
    print(f"Marked {np.sum(low_density_mask)} low-density bins (< 10 points) as converged")

    # Mark bins with NaN standard deviations as converged
    nan_std_mask = np.isnan(sf_stds) & ~bin_status
    bin_status |= nan_std_mask
    print(f"Marked {np.sum(nan_std_mask)} bins with NaN standard deviations as converged")
    
    # Mark early converged bins
    early_converged = (sf_stds <= convergence_eps) & ~bin_status & (point_counts > 10)
    bin_status |= early_converged
    print(f"Marked {np.sum(early_converged)} bins as early-converged (std <= {convergence_eps})")
    
    # Main convergence loop
    iteration = 1
    
    print("\nSTARTING ADAPTIVE CONVERGENCE LOOP")
    while True:
        # Find unconverged bins
        unconverged = ~bin_status & (point_counts > 10) & (bin_bootstraps < max_nbootstrap)
        if not np.any(unconverged):
            print("All bins have converged or reached max bootstraps!")
            break
            
        print(f"\nIteration {iteration} - {np.sum(unconverged)} unconverged bins")
        
        # Create density-ordered bin list for efficient processing
        bin_list = []
        r_idxs = np.where(unconverged)[0]
        for j in r_idxs:
            bin_list.append((j, bin_density[j]))
        
        # Sort by density (highest first)
        bin_list.sort(key=lambda x: x[1], reverse=True)
        
        # Track convergence metrics
        bins_converged_in_iteration = 0
        max_reached_in_iteration = 0
        
        # Process bins in order of decreasing density
        for bin_idx, (j, density) in enumerate(bin_list):
            # Skip if already converged
            if bin_status[j]:
                continue
                
            print(f"\nProcessing bin {j} (r={r_centers[j]:.4f}) - Density: {density:.4f} - " + 
                 f"Current bootstraps: {bin_bootstraps[j]} - " + 
                 f"Current std: {sf_stds[j]:.6f} - " + 
                 f"Points: {point_counts[j]}")
                
            # Use exact bootstrap step value based on density
            step = bootstrap_steps[j]
            print(f"  Adding up to {step} more bootstraps to bin {j}")
            
            # Calculate spacing effectiveness for this bin
            spacing_effectiveness = {sp: bin_spacing_effectiveness[sp][j] for sp in spacing_values}
            
            # Sort spacings by effectiveness (highest first)
            sorted_spacings = sorted(spacing_effectiveness.items(), key=lambda x: x[1], reverse=True)
            
            # Use multi-spacing approach but more efficiently
            total_additional = 0
            remaining_step = step
            
            # Process all spacings based on their effectiveness
            total_effectiveness = sum(eff for _, eff in sorted_spacings if eff > 0)
            
            # Distribute bootstraps proportionally to effectiveness
            for sp_value, effectiveness in sorted_spacings:
                # Skip ineffective spacings
                if effectiveness <= 0: 
                    continue
                
                # Calculate proportion based on effectiveness
                if total_effectiveness > 0:
                    proportion = effectiveness / total_effectiveness
                    sp_additional = int(step * proportion)
                else:
                    sp_additional = 0.0
                
                sp_additional = min(sp_additional, remaining_step)                    
                
                # Process this spacing
                process_spacing_data(sp_value, sp_additional, False)
                
                # Update counters
                total_additional += sp_additional
                remaining_step -= sp_additional
                
                # Stop if we've allocated all bootstraps
                if remaining_step <= 0:
                    break
            
            # Update bootstrap counts
            bin_bootstraps[j] += total_additional
            
            # Recalculate statistics
            sf_means, sf_stds = calculate_bin_statistics()
            
            # Check for convergence or max bootstraps
            if sf_stds[j] <= convergence_eps:
                bin_status[j] = True
                print(f"  Bin {j} (r={r_centers[j]:.4f}) CONVERGED with std {sf_stds[j]:.6f} <= {convergence_eps}")
                bins_converged_in_iteration += 1
            elif bin_bootstraps[j] >= max_nbootstrap:
                bin_status[j] = True
                print(f"  Bin {j} (r={r_centers[j]:.4f}) reached MAX BOOTSTRAPS {max_nbootstrap}")
                max_reached_in_iteration += 1
        
        # Next iteration
        iteration += 1
        gc.collect()
        
    # Final convergence statistics
    converged_bins = np.sum(bin_status & (point_counts > 10))
    unconverged_bins = np.sum(~bin_status & (point_counts > 10))
    max_bootstrap_bins = np.sum((bin_bootstraps >= max_nbootstrap) & (point_counts > 10))
    
    print("\nFINAL CONVERGENCE STATISTICS:")
    print(f"  Total bins with data more than 10 points: {np.sum(point_counts > 10)}")
    print(f"  Converged bins: {converged_bins}")
    print(f"  Unconverged bins: {unconverged_bins}")
    print(f"  Bins at max bootstraps: {max_bootstrap_bins}")
    
    # Calculate error metrics for final results
    print("\nCalculating error metrics and confidence intervals...")
    
    # Error of isotropy
    eiso = np.zeros(n_bins_r)
    
    # Create sliding windows for theta bootstrapping
    if n_bins_theta > window_size_theta:
        indices_theta = sliding_window_view(
            np.arange(n_bins_theta), 
            (n_bins_theta - window_size_theta + 1,), 
            writeable=False
        )[::1]
        
        n_samples_theta = len(indices_theta)
        
        for i in range(n_samples_theta):
            idx = indices_theta[i]
            mean_sf = bn.nanmean(sfr[idx, :], axis=0)
            eiso += np.abs(mean_sf - sf_means)
        
        eiso /= max(1, n_samples_theta)  # Avoid division by zero
    else:
        print("Warning: Window size for theta is too large. Skipping isotropy error calculation.")
    
    # Create sliding windows for r bootstrapping
    if n_bins_r > window_size_r:
        indices_r = sliding_window_view(
            np.arange(n_bins_r), 
            (n_bins_r - window_size_r + 1,), 
            writeable=False
        )[::1]
        
        n_samples_r = len(indices_r)
        
        # Use a subset of bins for homogeneity
        r_subset = r_centers[indices_r[0]]
        
        # Calculate mean across all angles
        meanh = np.zeros(len(r_subset))
        ehom = np.zeros(len(r_subset))
        
        for i in range(n_samples_r):
            idx = indices_r[i]
            meanh += bn.nanmean(sfr[:, idx], axis=0)
        
        meanh /= max(1, n_samples_r)  # Avoid division by zero
        
        for i in range(n_samples_r):
            idx = indices_r[i]
            ehom += np.abs(bn.nanmean(sfr[:, idx], axis=0) - meanh)
        
        ehom /= max(1, n_samples_r)  # Avoid division by zero
    else:
        print("Warning: Window size for r is too large. Using all r bins instead.")
        r_subset = r_centers
        meanh = bn.nanmean(sfr, axis=0)
        ehom = np.zeros_like(meanh)
    
    # Calculate confidence intervals
    confidence_level = 0.95
    z_score = stats.norm.ppf((1 + confidence_level) / 2)
    
    # Use weight_totals to determine which bins have data
    has_data = weight_totals > 0
    
    ci_upper = np.full_like(sf_means, np.nan)
    ci_lower = np.full_like(sf_means, np.nan)
    
    # Only calculate CIs for bins with data
    if np.any(has_data):
        ci_upper[has_data] = sf_means[has_data] + z_score * sf_stds[has_data] / np.sqrt(weight_totals[has_data])
        ci_lower[has_data] = sf_means[has_data] - z_score * sf_stds[has_data] / np.sqrt(weight_totals[has_data])
    
    # Create output dataset
    print("\nCreating output dataset...")
    ds_iso = xr.Dataset(
        data_vars={
            'sf_polar': (('theta', 'r'), sfr),          # Angular-radial values
            'sf': (('r'), sf_means),                    # Isotropic values
            'error_isotropy': (('r'), eiso),            # Isotropy error
            'std': (('r'), sf_stds),                    # Standard deviation
            'ci_upper': (('r'), ci_upper),              # Upper confidence interval
            'ci_lower': (('r'), ci_lower),              # Lower confidence interval
            'error_homogeneity': (('r_subset'), ehom),  # Homogeneity error
            'n_bootstrap': (('r'), bin_bootstraps),     # Bootstrap counts
            'bin_density': (('r'), bin_density),        # Bin densities
            'point_counts': (('r'), point_counts),      # Point counts
            'converged': (('r'), bin_status)            # Convergence status
        },
        coords={
            'r': r_centers,
            'r_subset': r_subset,
            'theta': theta_centers
        },
        attrs={
            'order': str(order),
            'function_type': fun,
            'window_size_theta': window_size_theta,
            'window_size_r': window_size_r,
            'convergence_eps': convergence_eps,
            'max_nbootstrap': max_nbootstrap,
            'initial_nbootstrap': initial_nbootstrap,
            'bin_type': 'logarithmic' if log_bins else 'linear',
            'variables': variables_names,
            'bootstrappable_dimensions': ','.join(bootstrappable_dims),
            'backend': backend
        }
    )
    
    # Add bin edges to the dataset
    ds_iso['r_bins'] = (('r_edge'), r_bins)
    ds_iso['theta_bins'] = (('theta_edge'), theta_bins)
    
    print("ISOTROPIC SF COMPLETED SUCCESSFULLY!")
    print("="*60)
    
    return ds_iso

#####################################################################################################################
