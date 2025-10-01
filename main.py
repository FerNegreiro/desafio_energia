import pandas as pd
import numpy as np  # Necessário para a raiz quadrada (np.sqrt)
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error

from loaders.csv_loader import CsvLoader
from loaders.newave_loader import NewaveLoader
from predictor.baseline_predictor import BaselinePredictor
from predictor.enriched_predictor import EnrichedPredictor

# --- CONFIGURAÇÕES GLOBAIS ---
# Estas variáveis precisam estar aqui no topo para que o resto do script as veja.
PRICE_FILE_PATH = 'data/prices/SE_A+2.csv'
NEWAVE_FILE_PATH = 'data/newave/cmarg.csv'
TRAIN_TEST_SPLIT_DATE = '2024-06-01'


def evaluate_model(y_true, y_pred, model_name):
    """Função para calcular e retornar as métricas de erro."""
    metrics = {
        'Model': model_name,
        'MAE': mean_absolute_error(y_true, y_pred),
        'RMSE': np.sqrt(mean_squared_error(y_true, y_pred)), # <-- Linha corrigida da etapa anterior
        'MAPE': mean_absolute_percentage_error(y_true, y_pred)
    }
    
    print(f"\n--- Resultados: {model_name} ---")
    print(f"  MAE:  {metrics['MAE']:.2f}")
    print(f"  RMSE: {metrics['RMSE']:.2f}")
    print(f"  MAPE: {metrics['MAPE']:.2%}")
    print("---------------------------------")
    return metrics


def run():
    """Função principal que orquestra todo o processo."""
    # --- CARREGAMENTO DOS DADOS ---
    print("Carregando dados...")
    price_loader = CsvLoader(PRICE_FILE_PATH, date_col='Date', data_col='Price')
    price_series = price_loader.load()

    newave_loader = NewaveLoader(NEWAVE_FILE_PATH)
    cmo_series = newave_loader.load_and_process()

    # --- PREPARAÇÃO E DIVISÃO DOS DADOS ---
    print("Preparando e dividindo os dados para treino e teste...")
    full_df = pd.concat([price_series, cmo_series], axis=1).dropna()
    full_df.columns = ['price', 'cmo']

    train_df = full_df[full_df.index < TRAIN_TEST_SPLIT_DATE]
    test_df = full_df[full_df.index >= TRAIN_TEST_SPLIT_DATE]
    
    y_train_price, exog_train = train_df['price'], train_df[['cmo']]
    y_test_price, exog_test = test_df['price'], test_df[['cmo']]

    # --- EXECUÇÃO DO MODELO BASELINE ---
    print("\nTreinando Modelo Baseline (apenas com preços)...")
    baseline_predictor = BaselinePredictor()
    baseline_predictor.fit(y_train_price)
    baseline_preds = baseline_predictor.predict(steps=len(y_test_price))
    baseline_metrics = evaluate_model(y_test_price, baseline_preds, 'Baseline (SARIMA)')

    # --- EXECUÇÃO DO MODELO ENRIQUECIDO ---
    print("Treinando Modelo Enriquecido (com dados do Newave)...")
    enriched_predictor = EnrichedPredictor()
    enriched_predictor.fit(y_train_price, exog_train)
    enriched_preds = enriched_predictor.predict(steps=len(y_test_price), future_exog_data=exog_test)
    enriched_metrics = evaluate_model(y_test_price, enriched_preds, 'Enriched (SARIMAX + CMO)')

    # --- COMPARAÇÃO FINAL ---
    results_df = pd.DataFrame([baseline_metrics, enriched_metrics])
    
    print("\n" + "="*50)
    print("           Relatório Final de Comparação")
    print("="*50)
    print(results_df.to_string(index=False))
    print("="*50)
    
    mae_baseline = results_df.loc[0, 'MAE']
    mae_enriched = results_df.loc[1, 'MAE']
    if mae_enriched < mae_baseline:
        print("\nConclusão: O modelo enriquecido com dados do Newave (CMO) teve um desempenho MELHOR.")
    else:
        print("\nConclusão: O modelo enriquecido não superou o baseline neste teste.")


if __name__ == '__main__':
    run()