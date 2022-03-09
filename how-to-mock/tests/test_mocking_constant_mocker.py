
import mock_examples.constant_functions
from mock_examples.constant_functions import double


# mocking the module where it's imported, not where CONSTANT_A is from
## NOTE: "mocker" here is a fixture from pytest-mock.
def test_mocking_constant_a(mocker):
    mocker.patch.object(mock_examples.constant_functions, 'CONSTANT_A', 2)
    expected = 4
    actual = double()

    assert expected == actual

# Docs: https://docs.python.org/3/library/unittest.mock.html#patch-object
# In the above example, mocker.patch.object is taking 3 args; 
# - The object to be patched
# - The attribute name (ie the thing in the target which you want to patch)
# - The object to replace the attribute with (in this case, we're patching CONSTANT_A to equal 2 instead of 1)
