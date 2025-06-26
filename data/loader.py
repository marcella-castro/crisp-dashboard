import pandas as pd
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)

def load_data() -> pd.DataFrame:
    """Carrega o dataset do usuário para o dashboard, normalizando nomes de colunas."""
    path = Path("data/TJSP/df_processo_TJSP.csv")
    
    df = pd.read_csv(path)
    #print(df[['latitude', 'longitude']].head())
    df.columns = df.columns.str.strip()
    #logging.info(f"Colunas do DataFrame: {df.columns.tolist()}")
    #logging.info(f"Primeiras linhas:\n{df.head()}\n")
    return df

# Força o carregamento e logging ao importar este módulo
try:
    _df_debug = load_data()
except Exception as e:
    logging.error(f"Erro ao carregar o DataFrame: {e}")
