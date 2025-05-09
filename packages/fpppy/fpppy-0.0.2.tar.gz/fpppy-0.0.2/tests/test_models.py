def test_import_linear_regression():
    from fpppy.models import LinearRegression

    assert hasattr(LinearRegression, "add_prediction_intervals")
