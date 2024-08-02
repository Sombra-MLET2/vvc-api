import pandas as pd

def validate_numeric_column(df, column_year_name, column_quantity_name):
    """
    Verifica se todos os valores na colunas especificadas do DataFrame são numéricos.

    Args:
    df (pd.DataFrame): O DataFrame a ser verificado.
    column_name (str): O nome da coluna a ser verificada.

    Returns:
    bool: True se todos os valores forem numéricos, caso contrário, False.
    """
    return pd.to_numeric(df[column_year_name], errors='coerce').notna().all() and pd.to_numeric(df[column_quantity_name], errors='coerce').notna().all()


def get_non_numeric_values(df, column_year_name, column_quantity_name):
    """
    Retorna os valores que não foram convertidos para numérico em nas duas colunas numéricas dos DataFrames.

    Args:
    df (pd.DataFrame): O DataFrame a ser verificado.
    column_year_name (str): O nome da coluna de ano a ser verificada.
    column_quantity_name (str): O nome da coluna de quantidade a ser verificada.

    Returns:
    dict: Um dicionário com os valores não numéricos para cada coluna.
    """
    non_numeric_years = df[column_year_name][pd.to_numeric(df[column_year_name], errors='coerce').isna()]
    non_numeric_quantities = df[column_quantity_name][pd.to_numeric(df[column_quantity_name], errors='coerce').isna()]

    return {
        column_year_name: non_numeric_years.tolist(),
        column_quantity_name: non_numeric_quantities.tolist()
    }