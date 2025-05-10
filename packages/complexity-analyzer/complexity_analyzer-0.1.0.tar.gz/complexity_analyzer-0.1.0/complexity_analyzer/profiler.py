import time
import tracemalloc
import sys
import signal
import matplotlib.pyplot as plt
import numpy as np
import logging
from dataclasses import dataclass
from .utils import fit_complexity

# Set up logging
logger = logging.getLogger("complexity_analyzer.profiler")

class ProfilingError(Exception):
    """Exception raised when profiling fails."""
    pass

class TimeoutError(ProfilingError):
    """Exception raised when profiling times out."""
    pass

@dataclass
class ComplexityResult:
    time_complexity: str
    space_complexity: str
    time_data: list  # List of (n, time) tuples
    space_data: list  # List of (n, space) tuples
    
    def __str__(self):
        return f"Time Complexity: {self.time_complexity}, Space Complexity: {self.space_complexity}"
    
    def summary(self):
        """Return a detailed summary of profiling results."""
        return {
            "time_complexity": self.time_complexity,
            "space_complexity": self.space_complexity,
            "time_measurements": self.time_data,
            "space_measurements": self.space_data
        }
    
    def to_dict(self):
        """Convert results to a dictionary for serialization."""
        return {
            "time_complexity": self.time_complexity,
            "space_complexity": self.space_complexity,
            "time_data": [(int(n), float(t)) for n, t in self.time_data],
            "space_data": [(int(n), float(s)) for n, s in self.space_data]
        }

def timeout_handler(signum, frame):
    """Handler for timeout signal."""
    raise TimeoutError("Function execution timed out")

def safe_execution(func, args, kwargs, timeout=30):
    """
    Execute a function with a timeout.
    
    Parameters:
    -----------
    func : callable
        Function to execute
    args : tuple
        Positional arguments
    kwargs : dict
        Keyword arguments
    timeout : int, optional
        Timeout in seconds (default: 30)
        
    Returns:
    --------
    Any
        Result of function execution
        
    Raises:
    -------
    TimeoutError
        If execution times out
    """
    # Set timeout handler
    if hasattr(signal, 'SIGALRM'):  # Unix/Linux/Mac
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(timeout)
        try:
            result = func(*args, **kwargs)
            signal.alarm(0)  # Disable alarm
            return result
        except TimeoutError:
            raise
        except Exception as e:
            signal.alarm(0)  # Disable alarm
            raise e
    else:  # Windows doesn't support SIGALRM
        # Simplified timeout for Windows (less accurate)
        start_time = time.time()
        result = func(*args, **kwargs)
        if time.time() - start_time > timeout:
            logger.warning(f"Function execution took longer than {timeout} seconds, but couldn't be interrupted on Windows.")
        return result

def create_test_input(n, original_input=None, input_type=None):
    """
    Create a test input of size n based on the original input type.
    
    Parameters:
    -----------
    n : int
        Desired size of the input
    original_input : Any, optional
        Original input to base the test input on
    input_type : str, optional
        Type of input to create ("list", "string", "number", "matrix")
        
    Returns:
    --------
    Any
        Generated test input
    """
    if original_input is not None:
        if isinstance(original_input, (list, tuple)):
            # Create a properly sized input based on the original structure
            if len(original_input) == 0:
                element_type = int  # Default to integers
            else:
                element_type = type(original_input[0])
            
            if element_type == int:
                return list(range(n))
            elif element_type == str:
                return ['a' * (i % 10 + 1) for i in range(n)]
            elif element_type == float:
                return [float(i) for i in range(n)]
            elif isinstance(original_input[0], (list, tuple)):  # Matrix
                inner_size = len(original_input[0]) if original_input[0] else 1
                return [[j for j in range(inner_size)] for i in range(n)]
            else:
                # For other types, create a list of n zeros
                return [0] * n
                
        elif isinstance(original_input, str):
            # Create a string of length n
            return 'a' * n
            
        elif isinstance(original_input, (int, float)):
            # For numeric inputs, use n as the value (limited to avoid huge computation)
            return min(n, 1000000)
            
        elif isinstance(original_input, dict):
            # Create a dictionary with n items
            return {str(i): i for i in range(n)}
            
        else:
            # For unsupported types, try converting to a list
            try:
                return list(range(n))
            except:
                raise ValueError(f"Unsupported input type: {type(original_input)}")
    
    # If no original input or input_type is provided, use explicit input_type
    if input_type:
        if input_type == "list":
            return list(range(n))
        elif input_type == "string":
            return 'a' * n
        elif input_type == "number":
            return min(n, 1000000)
        elif input_type == "matrix":
            return [[j for j in range(int(np.sqrt(n)))] for i in range(int(np.sqrt(n)))]
        elif input_type == "dict":
            return {str(i): i for i in range(n)}
        else:
            raise ValueError(f"Unsupported input_type: {input_type}")
    
    # Default to a list of integers
    return list(range(n))

def profile_complexity(func, *args, input_sizes=(10, 100, 1000), iterations=None, 
                       input_type=None, max_runtime=30, **kwargs):
    """
    Profile time and space complexity empirically.
    
    Parameters:
    -----------
    func : callable
        The function to analyze
    *args : tuple
        Arguments to pass to the function
    input_sizes : tuple or list
        Sizes of inputs to test (default: (10, 100, 1000))
    iterations : int, optional
        Number of iterations for each size. If None, automatically determined.
    input_type : str, optional
        Type of input to generate ("list", "string", "number", "matrix", "dict")
    max_runtime : int, optional
        Maximum runtime in seconds for each input size (default: 30)
    **kwargs : dict
        Keyword arguments to pass to the function
        
    Returns:
    --------
    ComplexityResult
        Object containing complexity analysis results
        
    Raises:
    -------
    ProfilingError
        If profiling fails
    """
    if not callable(func):
        raise ProfilingError("Input must be a callable function")

    times = []
    spaces = []
    
    # Test each input size
    for n in input_sizes:
        try:
            if args:
                # Use the first argument as a base for the test input
                test_input = create_test_input(n, args[0], input_type)
                test_args = (test_input,) + args[1:]
            else:
                # Create a default test input if no arguments are provided
                test_input = create_test_input(n, input_type=input_type)
                test_args = (test_input,)

            # Increase recursion limit for large inputs
            old_limit = sys.getrecursionlimit()
            sys.setrecursionlimit(max(1000, n * 2))  # More generous recursion limit

            # Determine iterations based on input size
            if iterations is None:
                iterations = max(3, min(50, 10000 // max(n, 1)))
            
            # Time profiling with warmup
            try:
                # Warmup (with timeout)
                safe_execution(func, test_args, kwargs, timeout=max_runtime)
                
                # Actual measurement
                start_time = time.perf_counter()
                for _ in range(iterations):
                    safe_execution(func, test_args, kwargs, timeout=max_runtime // iterations)
                elapsed = (time.perf_counter() - start_time) / iterations
                times.append((n, elapsed))
                
            except TimeoutError:
                logger.warning(f"Execution timed out for input size {n}")
                # If we already have some data points, we can continue with larger sizes
                if times:
                    # Extrapolate time for larger input based on current complexity
                    last_n, last_time = times[-1]
                    if len(times) >= 2:
                        # Simple extrapolation based on growth rate
                        n_ratio = n / last_n
                        time_ratio = times[-1][1] / times[-2][1]
                        n_prev_ratio = last_n / times[-2][0]
                        growth_factor = time_ratio / n_prev_ratio
                        
                        extrapolated_time = last_time * (n_ratio ** growth_factor)
                        times.append((n, extrapolated_time))
                        logger.info(f"Extrapolated time for size {n}: {extrapolated_time:.6f}s")
                    else:
                        # Without enough data points, use a default O(n²) extrapolation
                        extrapolated_time = last_time * (n / last_n) ** 2
                        times.append((n, extrapolated_time))
                        logger.info(f"Extrapolated time for size {n}: {extrapolated_time:.6f}s (assuming O(n²))")
                else:
                    # If we have no data points yet, skip this input size and try a smaller one
                    fallback_size = max(5, n // 10)
                    if fallback_size not in input_sizes and fallback_size > 0:
                        logger.info(f"Trying fallback input size: {fallback_size}")
                        try:
                            test_input = create_test_input(fallback_size, args[0] if args else None, input_type)
                            test_args = (test_input,) + args[1:] if args else (test_input,)
                            
                            safe_execution(func, test_args, kwargs, timeout=max_runtime)
                            
                            start_time = time.perf_counter()
                            for _ in range(iterations):
                                safe_execution(func, test_args, kwargs, timeout=max_runtime // iterations)
                            elapsed = (time.perf_counter() - start_time) / iterations
                            times.append((fallback_size, elapsed))
                        except:
                            # If even the fallback fails, continue to the next input size
                            pass

            # Memory profiling
            try:
                tracemalloc.start()
                safe_execution(func, test_args, kwargs, timeout=max_runtime)
                _, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                spaces.append((n, peak / 1024))  # KB
            except Exception as e:
                logger.warning(f"Memory profiling failed for input size {n}: {e}")
                # If we have previous space measurements, extrapolate
                if spaces:
                    last_n, last_space = spaces[-1]
                    # Linear extrapolation for space (most common)
                    extrapolated_space = last_space * (n / last_n)
                    spaces.append((n, extrapolated_space))
                    logger.info(f"Extrapolated space for size {n}: {extrapolated_space:.2f}KB")

            # Restore recursion limit
            sys.setrecursionlimit(old_limit)
            
        except Exception as e:
            logger.error(f"Profiling failed for input size {n}: {e}")
            # Continue with the next input size rather than failing completely
            continue

    # Ensure we have at least one data point
    if not times:
        raise ProfilingError("Could not profile any input sizes successfully")
        
    # Analyze the data
    time_complexity = fit_complexity(times)
    
    # Determine space complexity
    if len(spaces) >= 2:
        space_values = [x[1] for x in spaces]
        space_range = max(space_values) - min(space_values)
        space_complexity = "O(1)" if space_range < 10 else fit_complexity(spaces, is_space=True)
    else:
        space_complexity = "O(?)"
        
    return ComplexityResult(time_complexity, space_complexity, times, spaces)

def plot_complexity(func_name, time_data, space_data, save_path=None, show_complexity_lines=True):
    """
    Generate graphs for time and space complexity.
    
    Parameters:
    -----------
    func_name : str
        Name of the function being analyzed
    time_data : list
        List of (n, time) tuples
    space_data : list
        List of (n, space) tuples
    save_path : str, optional
        If provided, save the plot to this path instead of displaying it
    show_complexity_lines : bool, optional
        Whether to show reference complexity lines (default: True)
    """
    try:
        n_values, times = zip(*time_data)
        _, spaces = zip(*space_data)

        fig = plt.figure(figsize=(12, 10))
        
        # Time Complexity Plot
        ax1 = plt.subplot(2, 1, 1)
        ax1.plot(n_values, times, marker='o', label='Measured Time')
        
        # Add reference curves for common complexities
        if show_complexity_lines:
            x = np.array(n_values)
            scale_factor = times[0] / max(1, n_values[0])  # Avoid division by zero
            
            # O(1)
            ax1.plot(x, [times[0]] * len(x), '--', label='O(1)', alpha=0.5, color='green')
            
            # O(log n)
            if n_values[0] > 0:  # Avoid log(0)
                ax1.plot(x, [scale_factor * np.log2(n) for n in x], '--', label='O(log n)', alpha=0.5, color='blue')
            
            # O(n)
            ax1.plot(x, scale_factor * x, '--', label='O(n)', alpha=0.5, color='orange')
            
            # O(n log n)
            if n_values[0] > 0:  # Avoid log(0)
                ax1.plot(x, [scale_factor * n * np.log2(n) for n in x], '--', label='O(n log n)', alpha=0.5, color='purple')
            
            # O(n²)
            ax1.plot(x, scale_factor * x**2, '--', label='O(n²)', alpha=0.5, color='red')
            
            # O(2^n)
            with np.errstate(over='ignore'):  # Ignore overflow warnings
                exponential_values = [scale_factor * 2**min(n, 30) for n in x]  # Limit n to avoid overflow
                ax1.plot(x, exponential_values, '--', label='O(2^n)', alpha=0.5, color='brown')
        
        ax1.set_xlabel('Input Size (n)')
        ax1.set_ylabel('Time (seconds)')
        ax1.set_title(f'Time Complexity for {func_name}')
        ax1.grid(True)
        ax1.legend()

        # Space Complexity Plot
        ax2 = plt.subplot(2, 1, 2)
        ax2.plot(n_values, spaces, marker='o', color='orange', label='Measured Space')
        
        # Add reference curves for common space complexities
        if show_complexity_lines:
            space_scale = spaces[0] / max(1, n_values[0])  # Avoid division by zero
            
            # O(1)
            ax2.plot(x, [spaces[0]] * len(x), '--', label='O(1)', alpha=0.5, color='green')
            
            # O(log n)
            if n_values[0] > 0:  # Avoid log(0)
                ax2.plot(x, [space_scale * np.log2(n) for n in x], '--', label='O(log n)', alpha=0.5, color='blue')
            
            # O(n)
            ax2.plot(x, space_scale * x, '--', label='O(n)', alpha=0.5, color='orange')
            
            # O(n²)
            ax2.plot(x, space_scale * x**2, '--', label='O(n²)', alpha=0.5, color='red')
        
        ax2.set_xlabel('Input Size (n)')
        ax2.set_ylabel('Space (KB)')
        ax2.set_title(f'Space Complexity for {func_name}')
        ax2.grid(True)
        ax2.legend()

        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path)
            plt.close(fig)
        else:
            try:
                plt.show()
            except Exception as e:
                logger.warning(f"Could not display plot: {e}")
                # Save to a default location if display fails
                plt.savefig(f"{func_name}_complexity.png")
                plt.close(fig)
                logger.info(f"Plot saved to {func_name}_complexity.png")
    
    except Exception as e:
        logger.error(f"Plotting failed: {e}")
        # Don't raise an exception here since plotting is not critical