import pandas as pd
# from flask_caching import Cache

from data.loader import load_data

TIMEOUT = 60 * 60 * 24  # Cache data for aproximadamente 1 dia

cache = None  # Dummy para evitar erro de importação

def retrieve_data() -> pd.DataFrame:
    """Função usada para carregar os dados SEM cache."""
    data = load_data()
    return data
