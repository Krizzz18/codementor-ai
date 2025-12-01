"""
Tests for CodeMentor AI Agents
"""

import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.code_executor import SafeCodeExecutor


def test_code_executor_simple():
    """Test basic code execution"""
    executor = SafeCodeExecutor()
    result = executor.execute("print('Hello, World!')")
    assert result["success"] == True
    assert "Hello, World!" in result["output"]


def test_code_executor_math():
    """Test mathematical operations"""
    executor = SafeCodeExecutor()
    result = executor.execute("print(2 + 2)")
    assert result["success"] == True
    assert "4" in result["output"]


def test_code_executor_loop():
    """Test loop execution"""
    executor = SafeCodeExecutor()
    code = """for i in range(3):
    print(i)"""
    result = executor.execute(code)
    assert result["success"] == True
    assert "0" in result["output"]
    assert "1" in result["output"]
    assert "2" in result["output"]


def test_code_executor_timeout():
    """Test timeout protection"""
    executor = SafeCodeExecutor()
    result = executor.execute("while True: pass")
    assert result["success"] == False
    assert "timeout" in result["error"].lower()


def test_code_executor_error():
    """Test error handling"""
    executor = SafeCodeExecutor()
    result = executor.execute("print(undefined_variable)")
    assert result["success"] == False
    assert "NameError" in result["error"]


def test_code_executor_security():
    """Test security restrictions"""
    executor = SafeCodeExecutor()
    # Should fail - file I/O not allowed
    result = executor.execute("open('test.txt', 'w')")
    assert result["success"] == False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
