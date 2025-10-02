import pandas as pd
import numpy as np
import os


def gerar_dados_sinteticos(price_path='data/prices/SE_A+2.csv', newave_path='data/newave/cmarg.csv'):
    """
    Gera arquivos CSV com séries temporais sintéticas de preços de energia e CMO do Newave.
    """
    
    os.makedirs(os.path.dirname(price_path), exist_ok=True)
    os.makedirs(os.path.dirname(newave_path), exist_ok=True)

    
    datas_preco = pd.to_datetime(pd.date_range(start='2020-01-01', end='2025-09-01', freq='MS'))
    n_preco = len(datas_preco)
    precos = 150 + np.linspace(0, 80, n_preco) + 25 * np.sin(np.linspace(0, n_preco/12 * 2 * np.pi, n_preco) - (np.pi/2)) + np.random.normal(0, 15, n_preco)
    precos[precos < 30] = 30
    df_precos = pd.DataFrame({'Date': datas_preco, 'Price': precos.round(2)})
    df_precos.to_csv(price_path, index=False)
    print(f"Arquivo de preços sintéticos salvo em: {price_path}")

    
    datas_cmo = pd.to_datetime(pd.date_range(start='2020-01-01', periods=72, freq='MS'))
    n_cmo = len(datas_cmo)
    base_cmo = pd.Series(index=datas_cmo, data=[80 + 40 * np.sin(i / 6 * np.pi) for i in range(n_cmo)])
    cmo_final = base_cmo + np.random.normal(0, 20, n_cmo)
    cmo_final[cmo_final < 15] = 15
    df_cmo = pd.DataFrame({'date': datas_cmo, 'cmo_se': cmo_final.round(2)})
    df_cmo.to_csv(newave_path, index=False)
    print(f"Arquivo de CMO sintético salvo em: {newave_path}")



if __name__ == '__main__':
    gerar_dados_sinteticos()
