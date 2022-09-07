from unittest import mock
from app import fs

# Patching the "check_output" function used in fs.print_contents_of_cwd() to return a bytes string with a value of "foo bar"
@mock.patch("app.fs.check_output", return_value=b"foo\nbar\n")
def test_print_contents_of_cwd_success(mock_check_output): # We have to add a name of the mocked function here (even if not used)
    actual_result = fs.print_contents_of_cwd()
    expected_directory = b"foo"
    
    # Checking that the expected directory is listed in the result
    assert expected_directory in actual_result
