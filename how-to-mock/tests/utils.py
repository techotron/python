import os

# Here we have a helper function which we can use to conditionally run tests using a 
#  pytest decorator, eg: @pytest.mark.skipif(is_ci(), reason="no need to run slow tests locally")
def is_ci():
    try:
        os.environ['CI']
    except KeyError as e:
        return True
    return False
