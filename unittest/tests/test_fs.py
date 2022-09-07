from unittest import mock
from app import fs

# Mock using a decorator
# Patching the "check_output" function used in fs.print_contents_of_cwd() to return a bytes string with a value of "foo bar"
@mock.patch("app.fs.check_output", return_value=b"foo\nbar\n")
def test_print_contents_of_cwd_success_dec(mock_check_output): # We have to add a name of the mocked function here (even if not used)
    actual_result = fs.print_contents_of_cwd()
    expected_directory = b"foo"

    # Checking that the expected directory is listed in the result
    assert expected_directory in actual_result


# Mock usinga  context manager
def test_print_contents_of_cwd_success_con():
    with mock.patch("app.fs.check_output", return_value=b"foo\nbar\n"):
        actual_result = fs.print_contents_of_cwd()
    expected_directory = b"foo"

    assert expected_directory in actual_result


# Mock using start stop (good for avoiding lots of decorators or/and lots of nested context managers)
def test_print_contents_of_csw_success_start_stop():
    # Call the setup function (note: if using the unittest.TestCase class then these are automatically called(?))
    p = setUp()

    actual_result = fs.print_contents_of_cwd()
    expected_directory = b"baz"

    assert expected_directory in actual_result

    # Stop the patcher, or it will continue to operate for the rest of the test suite
    tearDown(p)



def setUp():
    patcher = mock.patch("app.fs.check_output", return_value=b"foo\nbar\nbaz\n")
    patcher.start()
    return patcher

def tearDown(patcher):
    patcher.stop()
