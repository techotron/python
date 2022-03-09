https://changhsinlee.com/pytest-mock/

```
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```


The `MagicMock` object allows us to mimic a constant, an object with attributes or a function. 

When we use Pytest, the `mocker` fixture is the interface from `pytest-mock` that gives us `MagicMock`. 

You typically want to mock an object **where the object is imported INTO** (rather than where it's imported from). 

## Examples
The code is the documentation. Comments are included in the code to provide context. Each example demonstrates how to mock a certain object. To organise this, I've used the prefix <object_type>_filename.py. So the example for mocking constants consists of `constant_constants.py` and `constant_functions.py`. The test names don't follow the same convention but they are named descriptively anyway.

To run the tests run `pytest` inside the venv


**Note:** You may need to install `pytest-mock` at the user level if you see the error "mocker not found": `pip install --user pytest-mock`
