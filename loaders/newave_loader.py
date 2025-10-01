import pandas as pd

class NewaveLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_and_process(self) -> pd.Series:
        # Lógica SIMULADA. A implementação real usaria a biblioteca 'inewave'.
        cmo_df = pd.read_csv(self.file_path, parse_dates=['date'], index_col='date')
        return cmo_df['cmo_se'].asfreq('MS').dropna()