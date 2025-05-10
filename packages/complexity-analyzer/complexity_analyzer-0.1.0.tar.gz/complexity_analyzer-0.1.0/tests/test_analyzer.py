import unittest
from complexity_analyzer import complexity, analyze_code
from io import StringIO
import sys

class TestAnalyzer(unittest.TestCase):
    def test_bubble_sort(self):
        @complexity
        def bubble_sort(arr):
            n = len(arr)
            for i in range(n):
                for j in range(0, n - i - 1):
                    if arr[j] > arr[j + 1]:
                        arr[j], arr[j + 1] = arr[j + 1], arr[j]
            return arr

        # Use a larger, unsorted input
        input_data = [5, 2, 9, 1, 5, 6, 3, 8, 4, 7]
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        result = bubble_sort(input_data)
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        self.assertEqual(result, sorted(input_data))
        self.assertIn("Time Complexity: O(n²)", output)

    def test_linear_sum(self):
        @complexity
        def linear_sum(arr):
            total = 0
            for num in arr:
                total += num
            return total

        old_stdout = sys.stdout
        sys.stdout = StringIO()
        result = linear_sum([1, 2, 3, 4, 5])
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        self.assertEqual(result, 15)
        self.assertIn("Time Complexity: O(n)", output)

    def test_invalid_code(self):
        with self.assertRaises(ValueError):
            analyze_code("def invalid(:")

if __name__ == "__main__":
    unittest.main()