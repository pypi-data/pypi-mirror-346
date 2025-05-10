#!/usr/bin/env python
import argparse
import ast
import importlib.util
import os
import sys
from textwrap import dedent

from complexity_analyzer import analyze_code, complexity
from complexity_analyzer.profiler import profile_complexity, plot_complexity


def load_function_from_file(file_path, function_name=None):
    """
    Load a function from a Python file.
    
    Parameters:
    -----------
    file_path : str
        Path to the Python file
    function_name : str, optional
        Name of the function to load. If None, loads the first function defined.
    
    Returns:
    --------
    function : callable
        The loaded function
    """
    # Get absolute path
    abs_path = os.path.abspath(file_path)
    
    # Load module
    module_name = os.path.basename(file_path).replace('.py', '')
    spec = importlib.util.spec_from_file_location(module_name, abs_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    # Find function
    if function_name:
        if not hasattr(module, function_name):
            functions = [name for name, val in module.__dict__.items() 
                        if callable(val) and not name.startswith('_')]
            raise ValueError(f"Function '{function_name}' not found in {file_path}. "
                            f"Available functions: {', '.join(functions)}")
        return getattr(module, function_name)
    else:
        # Find first function defined in the module
        functions = [name for name, val in module.__dict__.items() 
                    if callable(val) and not name.startswith('_') 
                    and getattr(val, '__module__', None) == module.__name__]
        
        if not functions:
            raise ValueError(f"No functions found in {file_path}")
        
        return getattr(module, functions[0])


def extract_functions_from_file(file_path):
    """
    Extract all function definitions from a Python file.
    
    Parameters:
    -----------
    file_path : str
        Path to the Python file
    
    Returns:
    --------
    list
        List of (function_name, function_code) tuples
    """
    with open(file_path, 'r') as f:
        content = f.read()
    
    tree = ast.parse(content)
    functions = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Get the function's source code
            start_line = node.lineno
            end_line = max(child.lineno for child in ast.walk(node) if hasattr(child, 'lineno'))
            
            # Read lines from the file to get the exact code
            with open(file_path, 'r') as f:
                lines = f.readlines()
                func_code = ''.join(lines[start_line-1:end_line])
            
            functions.append((node.name, func_code))
    
    return functions


def run_analysis(args):
    """Run the analysis based on command line arguments."""
    if args.code:
        # Analyze string of code
        result = analyze_code(dedent(args.code))
        print(result)
        return
    
    if args.file:
        if args.analyze_all:
            # Analyze all functions in the file
            functions = extract_functions_from_file(args.file)
            print(f"Found {len(functions)} functions in {args.file}")
            for name, code in functions:
                print(f"\n{'-'*40}\nAnalyzing function: {name}\n{'-'*40}")
                result = analyze_code(code)
                print(result)
        
        elif args.run and args.function:
            # Run and profile a specific function
            try:
                func = load_function_from_file(args.file, args.function)
                
                # Determine input sizes
                sizes = args.input_sizes if args.input_sizes else [10, 100, 1000]
                
                # Create test input
                test_input = list(range(max(sizes)))
                
                print(f"Profiling function: {func.__name__}")
                result = profile_complexity(func, test_input, input_sizes=sizes)
                print(f"Time Complexity: {result.time_complexity}")
                print(f"Space Complexity: {result.space_complexity}")
                
                # Generate plot
                plot_complexity(func.__name__, result.time_data, result.space_data, 
                                save_path=args.save_plot)
                
                if args.save_plot:
                    print(f"Plot saved to: {args.save_plot}")
            except Exception as e:
                print(f"Error running function: {e}")
                sys.exit(1)
        else:
            # Static analysis of a specific function or the first one
            try:
                if args.function:
                    # Find specific function
                    functions = extract_functions_from_file(args.file)
                    for name, code in functions:
                        if name == args.function:
                            result = analyze_code(code)
                            print(f"Analysis of function '{name}':")
                            print(result)
                            break
                    else:
                        print(f"Function '{args.function}' not found in {args.file}")
                else:
                    # Analyze first function
                    functions = extract_functions_from_file(args.file)
                    if functions:
                        name, code = functions[0]
                        result = analyze_code(code)
                        print(f"Analysis of function '{name}':")
                        print(result)
                    else:
                        print(f"No functions found in {args.file}")
            except Exception as e:
                print(f"Error analyzing file: {e}")
                sys.exit(1)


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Analyze time and space complexity of Python code",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=dedent("""
        Examples:
          # Analyze code directly
          complexity-analyzer --code "def bubble_sort(arr):
              n = len(arr)
              for i in range(n):
                  for j in range(0, n - i - 1):
                      if arr[j] > arr[j + 1]:
                          arr[j], arr[j + 1] = arr[j + 1], arr[j]
              return arr"
          
          # Analyze a file
          complexity-analyzer --file my_algorithm.py
          
          # Analyze a specific function in a file
          complexity-analyzer --file my_algorithm.py --function bubble_sort
          
          # Run and profile a function
          complexity-analyzer --file my_algorithm.py --function bubble_sort --run
          
          # Run with custom input sizes and save the plot
          complexity-analyzer --file my_algorithm.py --function bubble_sort --run --input-sizes 50 500 5000 --save-plot complexity_plot.png
        """)
    )
    
    parser.add_argument('--code', type=str, help='Python code to analyze')
    parser.add_argument('--file', type=str, help='Path to Python file')
    parser.add_argument('--function', type=str, help='Function name to analyze (default: first function)')
    parser.add_argument('--run', action='store_true', help='Run and profile the function')
    parser.add_argument('--analyze-all', action='store_true', help='Analyze all functions in the file')
    parser.add_argument('--input-sizes', type=int, nargs='+', help='Input sizes for profiling (default: 10 100 1000)')
    parser.add_argument('--save-plot', type=str, help='Save plot to file instead of displaying')
    
    args = parser.parse_args()
    
    if not (args.code or args.file):
        parser.print_help()
        sys.exit(1)
    
    run_analysis(args)


if __name__ == '__main__':
    main()