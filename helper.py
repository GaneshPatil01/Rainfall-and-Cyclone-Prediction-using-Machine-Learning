import pandas as pd
import numpy as np
from prophet import Prophet
model = Prophet()

def prediction(data,d):
    data = data[['DATE','VALUE']]
    data.index= data['DATE']
    data = data.drop(columns=['DATE'])
    idx = pd.date_range(min(data.index), max(data.index),freq='MS')
    data = data.reindex(idx, fill_value=np.nan)
    data = data.reset_index()
    data = data.rename(columns={'index':'ds', 'VALUE':'y'})
    model.fit(data)
    future_date = pd.DataFrame({'ds':[d]})
    forecast = model.predict(future_date)
    # forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    return forecast[['yhat']].values[0]