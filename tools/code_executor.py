"""
Safe Python Code Execution Sandbox
"""

import sys
from io import StringIO
import signal
from contextlib import contextmanager
from typing import Dict


class TimeoutException(Exception):
    """Raised when code execution exceeds time limit"""
    pass


@contextmanager
def time_limit(seconds):
    """Context manager for timing out code execution"""
    def signal_handler(signum, frame):
        raise TimeoutException("Code execution timed out")
    
    # Windows doesn't support SIGALRM, so we'll use a simpler approach
    import threading
    timer = threading.Timer(seconds, lambda: (_ for _ in ()).throw(TimeoutException("Code execution timed out")))
    timer.start()
    try:
        yield
    finally:
        timer.cancel()


class SafeCodeExecutor:
    """
    Executes student Python code in restricted sandbox.
    SECURITY: No file I/O, no network, no dangerous imports, 5-second timeout.
    """
    ALLOWED_BUILTINS = [
        # Core functions
        'print', 'input', 'len', 'range', 'reversed', 'slice',
        # Type conversions
        'str', 'int', 'float', 'bool', 'bytes', 'bytearray',
        # Data structures
        'list', 'dict', 'tuple', 'set', 'frozenset',
        # Math operations
        'abs', 'min', 'max', 'sum', 'round', 'pow', 'divmod',
        # Iterators/generators
        'sorted', 'enumerate', 'zip', 'map', 'filter', 'iter', 'next',
        # Logic
        'all', 'any', 'bool',
        # Type checking
        'type', 'isinstance', 'issubclass', 'callable',
        # Object introspection
        'dir', 'vars', 'getattr', 'setattr', 'hasattr', 'delattr',
        # String/formatting
        'format', 'chr', 'ord', 'ascii', 'repr', 'bin', 'hex', 'oct',
        # Classes
        'object', 'property', 'classmethod', 'staticmethod',
        # Others
        'id', 'hash', 'help', 'isinstance'
    ]
    
    def execute(self, code: str, test_input: str = None) -> Dict:
        """
        Execute code safely and return results.
        
        Returns:
            {
                "output": stdout capture,
                "error": error message if any,
                "success": bool
            }
        """
        # Capture stdout
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()
        
        result = {"success": False, "output": "", "error": ""}
        
        try:
            # Create restricted globals with safe builtins
            import builtins
            safe_globals = {
                '__builtins__': {
                    name: getattr(builtins, name) 
                    for name in self.ALLOWED_BUILTINS 
                    if hasattr(builtins, name)
                }
            }
            
            # Execute code with timeout protection
            # Using threading (Windows-compatible)
            import threading
            import time
            
            exception_holder = []
            
            def run_code():
                try:
                    exec(code, safe_globals)
                except Exception as e:
                    exception_holder.append(e)
            
            thread = threading.Thread(target=run_code)
            thread.daemon = True
            thread.start()
            thread.join(timeout=5.0)
            
            if thread.is_alive():
                result["error"] = "Code execution timed out (5 seconds limit)"
            elif exception_holder:
                e = exception_holder[0]
                result["error"] = f"{type(e).__name__}: {str(e)}"
            else:
                result["output"] = captured_output.getvalue()
                result["success"] = True
                
        except Exception as e:
            result["error"] = f"{type(e).__name__}: {str(e)}"
        finally:
            sys.stdout = old_stdout
            
        return result
