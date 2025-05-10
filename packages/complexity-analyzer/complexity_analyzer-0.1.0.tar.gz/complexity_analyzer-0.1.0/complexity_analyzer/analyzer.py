import ast
import inspect
import sys
import textwrap
import logging
from functools import wraps
from .profiler import profile_complexity, plot_complexity
from .utils import complexity_to_str

# Set up logging
logger = logging.getLogger("complexity_analyzer")
handler = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)s: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.WARNING)

class ComplexityAnalysisError(Exception):
    """Base exception for complexity analysis errors."""
    pass

class StaticAnalysisError(ComplexityAnalysisError):
    """Exception raised when static analysis fails."""
    pass

class ComplexityAnalyzer(ast.NodeVisitor):
    def __init__(self, func_name=None):
        self.time_complexity = 0
        self.space_complexity = 0
        self.variables = set()
        self.current_depth = 0
        self.func_name = func_name
        self.has_recursion = False
        self.loops_count = 0
        self.conditionals_count = 0
        self.detected_patterns = set()

    def visit_For(self, node):
        self.current_depth += 1
        self.loops_count += 1
        self.time_complexity = max(self.time_complexity, self.current_depth)
        self.generic_visit(node)
        self.current_depth -= 1

    def visit_While(self, node):
        self.current_depth += 1
        self.loops_count += 1
        self.time_complexity = max(self.time_complexity, self.current_depth)
        self.generic_visit(node)
        self.current_depth -= 1

    def visit_If(self, node):
        self.conditionals_count += 1
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name == "sort" or func_name == "sorted":
                self.time_complexity = max(self.time_complexity, 2)  # O(n log n)
                self.detected_patterns.add("sorting")
            elif func_name in ["append", "extend", "insert"]:
                self.space_complexity += 1
                self.detected_patterns.add("list_modification")
            elif func_name in ["min", "max", "sum"]:
                # These functions typically have O(n) time complexity
                self.time_complexity = max(self.time_complexity, 1)
                self.detected_patterns.add("linear_operation")
            elif self.func_name and func_name == self.func_name:
                self.has_recursion = True
                self.detected_patterns.add("recursion")
        
        # Check for binary search in common libraries
        elif isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name):
                if node.func.value.id == "bisect" and node.func.attr in ["bisect", "bisect_left", "bisect_right", "insort"]:
                    self.time_complexity = max(self.time_complexity, -1)  # O(log n)
                    self.detected_patterns.add("binary_search")
        
        self.generic_visit(node)

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.variables.add(target.id)
        self.generic_visit(node)

    def visit_BinOp(self, node):
        # Check for binary search patterns
        if isinstance(node.op, ast.FloorDiv) and isinstance(node.left, ast.BinOp):
            if isinstance(node.left.op, ast.Add):
                # Pattern like (left + right) // 2, common in binary search
                self.time_complexity = max(self.time_complexity, -1)  # Log n
                self.detected_patterns.add("binary_search")
        self.generic_visit(node)

    def visit_ListComp(self, node):
        # List comprehensions are typically O(n)
        self.time_complexity = max(self.time_complexity, 1)
        self.space_complexity += 1
        self.detected_patterns.add("list_comprehension")
        self.generic_visit(node)

    def visit_DictComp(self, node):
        # Dict comprehensions are typically O(n)
        self.time_complexity = max(self.time_complexity, 1)
        self.space_complexity += 1
        self.detected_patterns.add("dict_comprehension")
        self.generic_visit(node)

    def visit_Subscript(self, node):
        # Check for dictionary/hashmap usage
        if isinstance(node.value, ast.Name) and node.value.id in self.variables:
            self.detected_patterns.add("hashmap_access")
        self.generic_visit(node)

def analyze_code(code_str):
    """
    Analyze complexity from a code string.
    
    Parameters:
    -----------
    code_str : str
        The code to analyze
        
    Returns:
    --------
    str
        Human-readable complexity analysis
        
    Raises:
    -------
    StaticAnalysisError
        If the code cannot be parsed or analyzed
    """
    try:
        cleaned_code = textwrap.dedent(code_str).strip()
        if not cleaned_code:
            raise StaticAnalysisError("No valid code to analyze")
        
        tree = ast.parse(cleaned_code)
        func_name = None
        
        # Find function name if it's a function definition
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                func_name = node.name
                break
        
        analyzer = ComplexityAnalyzer(func_name)
        analyzer.visit(tree)
        
        # Apply special case for recursion
        if analyzer.has_recursion:
            # Recursive algorithms can have various complexities
            # For simple recursion without branching, it's usually O(n)
            # For divide and conquer, it's usually O(log n) or O(n log n)
            if "binary_search" in analyzer.detected_patterns:
                time_str = "O(log n)"
            elif analyzer.loops_count > 0:
                time_str = "O(n log n)"  # Likely a divide and conquer with loop
            else:
                time_str = "O(n)"  # Simple recursion
        # Apply special case for binary search pattern
        elif "binary_search" in analyzer.detected_patterns:
            time_str = "O(log n)"
        # Apply special case for sorting
        elif "sorting" in analyzer.detected_patterns:
            time_str = "O(n log n)"
        else:
            time_str = complexity_to_str(analyzer.time_complexity)
            
        space_str = complexity_to_str(analyzer.space_complexity, is_space=True)
        
        # Enhanced output with detected patterns
        patterns_info = ""
        if analyzer.detected_patterns:
            patterns_info = f"\nDetected patterns: {', '.join(analyzer.detected_patterns)}"
            
        return f"Time Complexity: {time_str}, Space Complexity: {space_str}{patterns_info}"
    
    except SyntaxError as e:
        msg = f"Invalid code syntax: {e}"
        logger.error(msg)
        raise StaticAnalysisError(msg) from e
    except Exception as e:
        msg = f"Analysis failed: {e}"
        logger.error(msg)
        raise StaticAnalysisError(msg) from e

def set_log_level(level):
    """
    Set the logging level for the complexity analyzer.
    
    Parameters:
    -----------
    level : int or str
        Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    logger.setLevel(level)

def complexity(func=None, *, input_sizes=None, visualize=True, verbose=True, 
               catch_errors=True, custom_input_generator=None, max_runtime=30):
    """
    Decorator to analyze and profile a function's complexity.
    
    Parameters:
    -----------
    func : callable, optional
        The function to analyze
    input_sizes : list, optional
        Custom input sizes for profiling (default: [10, 100, 1000])
    visualize : bool, optional
        Whether to display visualization graphs (default: True)
    verbose : bool, optional
        Whether to print detailed analysis (default: True)
    catch_errors : bool, optional
        Whether to catch and handle errors (default: True)
    custom_input_generator : callable, optional
        A function that generates test inputs for each size
        Format: custom_input_generator(size) -> input_value
    max_runtime : int, optional
        Maximum allowed runtime in seconds for the analysis (default: 30)
        
    Returns:
    --------
    wrapped_func : callable
        The wrapped function with complexity analysis
    
    Raises:
    -------
    ComplexityAnalysisError
        If analysis fails and catch_errors is False
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            sizes = input_sizes or (10, 100, 1000)
            
            # Static analysis
            if verbose:
                try:
                    source_lines = inspect.getsourcelines(func)[0]
                    source = ''.join(line for line in source_lines if not line.strip().startswith('@'))
                    static_result = analyze_code(source)
                    print(f"Static Analysis - {static_result}")
                except (OSError, TypeError, ValueError, StaticAnalysisError) as e:
                    error_msg = f"Warning: Could not perform static analysis ({e})"
                    if verbose:
                        print(error_msg)
                    logger.warning(error_msg)
                    if not catch_errors:
                        raise ComplexityAnalysisError(error_msg) from e

            # Runtime profiling
            try:
                # If custom input generator is provided, use it
                if custom_input_generator:
                    # Override args with generated test input
                    if args:
                        args_list = list(args)
                        test_input = custom_input_generator(max(sizes))
                        args_list[0] = test_input
                        args = tuple(args_list)
                    else:
                        # If no args provided, add the generated input as first arg
                        args = (custom_input_generator(max(sizes)),)
                
                result = profile_complexity(
                    func, *args, 
                    input_sizes=sizes, 
                    max_runtime=max_runtime,
                    **kwargs
                )
                
                if verbose:
                    print(f"Profiled - Time Complexity: {result.time_complexity}, "
                          f"Space Complexity: {result.space_complexity}")
                
                if visualize:
                    try:
                        plot_complexity(func.__name__, result.time_data, result.space_data)
                    except Exception as e:
                        error_msg = f"Warning: Visualization failed ({e})"
                        logger.warning(error_msg)
                        if verbose:
                            print(error_msg)
                
                # Execute the function with original arguments
                return_value = func(*args, **kwargs)
                
                # Attach complexity results to return value if possible
                if hasattr(return_value, "__dict__"):
                    return_value._complexity_result = result
                
                return return_value
                
            except Exception as e:
                error_msg = f"Warning: Profiling failed ({e})"
                if verbose:
                    print(error_msg)
                logger.warning(error_msg)
                
                if not catch_errors:
                    raise ComplexityAnalysisError(error_msg) from e
                
                # If profiling fails but catch_errors is True, run the function normally
                return func(*args, **kwargs)
                
        return wrapper
    
    # Handle both @complexity and @complexity() usage
    if func is None:
        return decorator
    return decorator(func)