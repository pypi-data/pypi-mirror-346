import numpy as np
from scipy.optimize import curve_fit

def complexity_to_str(score, is_space=False):
    """
    Convert a complexity score to a human-readable string.
    
    Parameters:
    -----------
    score : int
        The complexity score from analysis
    is_space : bool
        Whether this is a space complexity calculation
        
    Returns:
    --------
    str
        Human-readable complexity notation
    """
    if score == 0:
        return "O(1)"
    elif score == 1:
        return "O(n)"
    elif score == 2:
        return "O(n²)" if not is_space else "O(n)"
    elif score == 3:
        return "O(n³)" if not is_space else "O(n)"
    elif score > 3:
        return f"O(n^{score})" if not is_space else "O(n)"
    elif score == -1:
        return "O(log n)"
    return "O(?)"


def fit_curve(x, y):
    """Fit different complexity curves to the data and determine the best fit."""
    # Define curve functions for different time complexities
    def constant(n, a):
        return a * np.ones_like(n)
        
    def logarithmic(n, a):
        return a * np.log(n)
        
    def linear(n, a):
        return a * n
        
    def linearithmic(n, a):
        return a * n * np.log(n)
        
    def quadratic(n, a):
        return a * n**2
        
    def cubic(n, a):
        return a * n**3
        
    def exponential(n, a, b):
        return a * b**n
    
    # Convert inputs to numpy arrays
    x_array = np.array(x, dtype=float)
    y_array = np.array(y, dtype=float)
    
    # Initialize scores dictionary
    scores = {}
    
    # Fit each curve and calculate mean squared error
    try:
        # Constant O(1)
        popt, _ = curve_fit(constant, x_array, y_array)
        scores["O(1)"] = np.mean((constant(x_array, *popt) - y_array) ** 2)
    except:
        scores["O(1)"] = float('inf')
        
    try:
        # Logarithmic O(log n)
        # Avoid log(0)
        valid_indices = x_array > 0
        if np.sum(valid_indices) >= 2:  # Need at least 2 points
            popt, _ = curve_fit(logarithmic, x_array[valid_indices], y_array[valid_indices])
            scores["O(log n)"] = np.mean((logarithmic(x_array[valid_indices], *popt) - y_array[valid_indices]) ** 2)
        else:
            scores["O(log n)"] = float('inf')
    except:
        scores["O(log n)"] = float('inf')
        
    try:
        # Linear O(n)
        popt, _ = curve_fit(linear, x_array, y_array)
        scores["O(n)"] = np.mean((linear(x_array, *popt) - y_array) ** 2)
    except:
        scores["O(n)"] = float('inf')
        
    try:
        # Linearithmic O(n log n)
        # Avoid log(0)
        valid_indices = x_array > 0
        if np.sum(valid_indices) >= 2:  # Need at least 2 points
            popt, _ = curve_fit(linearithmic, x_array[valid_indices], y_array[valid_indices])
            scores["O(n log n)"] = np.mean((linearithmic(x_array[valid_indices], *popt) - y_array[valid_indices]) ** 2)
        else:
            scores["O(n log n)"] = float('inf')
    except:
        scores["O(n log n)"] = float('inf')
        
    try:
        # Quadratic O(n²)
        popt, _ = curve_fit(quadratic, x_array, y_array)
        scores["O(n²)"] = np.mean((quadratic(x_array, *popt) - y_array) ** 2)
    except:
        scores["O(n²)"] = float('inf')
        
    try:
        # Cubic O(n³)
        popt, _ = curve_fit(cubic, x_array, y_array)
        scores["O(n³)"] = np.mean((cubic(x_array, *popt) - y_array) ** 2)
    except:
        scores["O(n³)"] = float('inf')
    
    # Find the best fit (lowest error)
    best_fit = min(scores.items(), key=lambda x: x[1])
    return best_fit[0]


def fit_complexity(data, is_space=False):
    """
    Fit runtime or memory data to a complexity class.
    
    Parameters:
    -----------
    data : list
        List of (n, measurement) tuples
    is_space : bool
        Whether this is space complexity data
        
    Returns:
    --------
    str
        Estimated complexity notation
    """
    if len(data) < 2:
        return "O(?)"  # Not enough data

    n_values, measurements = zip(*data)
    
    # Special case for flat measurements (constant complexity)
    if max(measurements) - min(measurements) < 1e-6 or max(measurements) < 1e-5:
        return "O(1)"
    
    # Try curve fitting for more accurate complexity estimation
    try:
        import scipy
        best_fit = fit_curve(n_values, measurements)
        return best_fit
    except (ImportError, RuntimeError):
        # Fallback to simple ratio analysis if scipy not available or fitting fails
        ratios = [measurements[i + 1] / max(measurements[i], 1e-10) for i in range(len(measurements) - 1)]
        n_ratios = [n_values[i + 1] / max(n_values[i], 1) for i in range(len(n_values) - 1)]
        
        avg_ratio = sum(ratios) / len(ratios)
        avg_n_ratio = sum(n_ratios) / len(n_ratios)
        
        # Simplified classification based on growth rates
        if avg_ratio <= 1.2:  # Nearly constant
            return "O(1)"
        elif avg_ratio <= 2 * avg_n_ratio:  # Linear or logarithmic
            if all(r <= 1.5 for r in ratios) and avg_n_ratio > 5:
                return "O(log n)"
            else:
                return "O(n)"
        elif avg_ratio <= 4 * avg_n_ratio:  # Potentially linearithmic
            return "O(n log n)"
        elif avg_ratio <= 1.5 * avg_n_ratio**2:  # Quadratic
            return "O(n²)"
        else:
            return "O(n³)" if not is_space else "O(n²)"