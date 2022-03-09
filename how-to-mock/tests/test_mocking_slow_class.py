from mock_examples.class_main import slow_dataset

def test_mocking_class_method(mocker):
    expected = "xyz"

    def mock_load(self):
        return "xyz"

    mocker.patch(
        # Dataset is in class_slow.py but it's imported to class_main.py, 
        #  therefore we target class_main.py
        'mock_examples.class_main.Dataset.load_data',
        mock_load
    )

    actual = slow_dataset()
    assert expected == actual
