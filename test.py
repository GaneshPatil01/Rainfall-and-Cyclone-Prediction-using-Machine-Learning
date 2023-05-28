import pandas as pd
from datetime import datetime
from helper import prediction

def test_prediction():
    # Create sample data for testing
    dates = pd.date_range(start='2021-01-01', end='2022-01-01', freq='MS')
    values = [10, 15, 20, 25, 30]
    data = pd.DataFrame({'DATE': dates, 'VALUE': values})
    
    # Provide a specific date for forecasting
    forecast_date = datetime(2022, 2, 1)
    
    # Call the prediction function
    result = prediction(data, forecast_date)
    
    # Assert the expected output
    expected_value = 35.0  # Replace with the expected forecasted value
    assert result == expected_value
    print('Test Case Pass Successfully')
