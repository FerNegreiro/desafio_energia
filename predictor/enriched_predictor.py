import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX

class EnrichedPredictor:
    def __init__(self, p=2, d=1, q=2, P=1, D=1, Q=1, s=12):
        self.order = (p, d, q)
        self.seasonal_order = (P, D, Q, s)
        self.model_results = None

    def fit(self, historical_prices: pd.Series, exog_data: pd.DataFrame):
        model = SARIMAX(endog=historical_prices, exog=exog_data, order=self.order, seasonal_order=self.seasonal_order)
        self.model_results = model.fit(disp=False)

    def predict(self, steps: int, future_exog_data: pd.DataFrame) -> pd.Series:
        return self.model_results.get_forecast(steps=steps, exog=future_exog_data).predicted_mean