import pandas as pd
import numpy as np
import os

def gerar_dados_correlacionados(price_path='data/prices/SE_A+2.csv', newave_path='data/newave/cmarg.csv'):
    """
    Gera arquivos CSV com séries temporais sintéticas e correlacionadas de Preço e CMO.
    """
    
    os.makedirs(os.path.dirname(price_path), exist_ok=True)
    os.makedirs(os.path.dirname(newave_path), exist_ok=True)

    datas = pd.to_datetime(pd.date_range(start='2020-01-01', end='2025-09-01', freq='MS'))
    n = len(datas)
    fator_correlacao = 1.5 
    base_cmo = pd.Series(index=datas, data=[80 + 40 * np.sin(i / 6 * np.pi) for i in range(n)])
    ruido_cmo = np.random.normal(0, 15, n)
    cmo_final = base_cmo + ruido_cmo
    cmo_final[cmo_final < 15] = 15
    
    df_cmo = pd.DataFrame({'date': datas, 'cmo_se': cmo_final.round(2)})
    df_cmo.to_csv(newave_path, index=False)
    print(f"Arquivo de CMO sintético salvo em: {newave_path}")

    preco_base = 100
    tendencia_preco = np.linspace(0, 50, n)
    ruido_preco = np.random.normal(0, 20, n)
    
    precos = preco_base + (cmo_final * fator_correlacao) + tendencia_preco + ruido_preco
    precos[precos < 40] = 40

    df_precos = pd.DataFrame({'Date': datas, 'Price': precos.round(2)})
    df_precos.to_csv(price_path, index=False)
    print(f"Arquivo de preços sintéticos (correlacionado) salvo em: {price_path}")

if __name__ == '__main__':
    gerar_dados_correlacionados()