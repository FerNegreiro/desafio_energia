import pandas as pd

class CsvLoader:
    def __init__(self, file_path: str, date_col: str, data_col: str):
        self.file_path = file_path
        self.date_col = date_col
        self.data_col = data_col

    def load(self, freq: str = 'MS') -> pd.Series:
        df = pd.read_csv(self.file_path, parse_dates=[self.date_col], index_col=self.date_col)
        series = df[self.data_col].asfreq(freq)
        return series.dropna()