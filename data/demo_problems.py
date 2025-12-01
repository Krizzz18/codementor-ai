"""
Sample Programming Problems for Demo
"""

PROBLEMS = {
    "fizzbuzz": {
        "title": "FizzBuzz",
        "description": """Write a function fizzbuzz() that prints numbers from 1 to 100.
- For multiples of 3, print "Fizz"
- For multiples of 5, print "Buzz"
- For multiples of both 3 and 5, print "FizzBuzz"
- Otherwise, print the number""",
        "difficulty": "Easy",
        "concepts": ["loops", "conditionals", "modulo"]
    },
    "palindrome": {
        "title": "Palindrome Checker",
        "description": """Write a function is_palindrome(s) that returns True if the string s is a palindrome (reads the same forwards and backwards), False otherwise.
Ignore spaces and capitalization.

Examples:
- is_palindrome("racecar") → True
- is_palindrome("hello") → False
- is_palindrome("A man a plan a canal Panama") → True""",
        "difficulty": "Easy",
        "concepts": ["strings", "conditionals"]
    },
    "sum_list": {
        "title": "Sum of List",
        "description": """Write a function sum_list(numbers) that takes a list of integers and returns their sum.
Do NOT use the built-in sum() function.

Example:
- sum_list([1, 2, 3, 4]) → 10
- sum_list([]) → 0""",
        "difficulty": "Easy",
        "concepts": ["loops", "lists", "variables"]
    },
    "reverse_string": {
        "title": "Reverse String",
        "description": """Write a function reverse_string(s) that returns the reverse of string s.
Do NOT use slicing ([::-1]).

Example:
- reverse_string("hello") → "olleh"
- reverse_string("Python") → "nohtyP" """,
        "difficulty": "Easy",
        "concepts": ["loops", "strings"]
    }
}
