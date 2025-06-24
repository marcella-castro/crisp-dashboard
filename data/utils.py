import pandas as pd
import logging
    
def number_of_processos(df: pd.DataFrame) -> int:
    # Busca a coluna que contém 'Número do Processo' de forma flexível
    for col in df.columns:
        if 'número do processo' in col.lower():
            unique_vals = df[col].unique()
            logging.info(f"Coluna encontrada: {col}")
            logging.info(f"Quantidade de únicos: {len(unique_vals)}")
            return df[col].nunique()
    logging.warning(f"Coluna 'Número do Processo' não encontrada. Colunas disponíveis: {df.columns.tolist()}")
    return 0


def number_of_countries(df: pd.DataFrame) -> int:
    """Get the number of countries in the dataset."""
    return len(unique_countries(df))


def number_of_restaurants(df: pd.DataFrame) -> int:
    """Retorna o número de linhas do DataFrame (processos analisados)."""
    return len(df.index)


def top_cuisine(df: pd.DataFrame) -> str:
    """Retorna '-' pois não há coluna 'Cuisine' no novo dataset."""
    return "-"


def number_of_cities(df: pd.DataFrame) -> int:
    """Get the number of cities in the dataset."""
    return len(df[df["City"].notna()]["City"].unique())


def unique_countries(df: pd.DataFrame) -> pd.Series:
    """Get unique countries from the dataset."""
    return df[df["Country"].notna()]["Country"].unique()
