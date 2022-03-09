from cmath import exp
import pytest
from mock_examples.function_main import slow_function
from .utils import is_ci

@pytest.mark.skipif(is_ci(), reason="no need to run slow tests locally")
def test_slow_function_super_slow():
    expected = 9
    actual = slow_function()
    assert expected == actual

def test_slow_function_mocked_api_call(mocker):
    mocker.patch(
        'mock_examples.function_main.api_call',
        return_value=5
    )

    expected = 5
    actual = slow_function()
    assert expected == actual

# Here, mocker.patch() specifies the target function to mock (the call to api_call() within the 
#  slow_function() function inside function_main.py)

# Another way of putting it would be "when you see api_call() called inside function_main.py, mock
#  it with this return value"
