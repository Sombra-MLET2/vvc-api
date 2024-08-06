import pandas as pd
from dataprocessing.tests import validate_numeric_column

def trata_csv(
        arquivo_nome: str,
        sep_arquivo: str,
        colunas_a_manter: list,
        colunas_a_remover: list,
        nome_coluna_controle: str,
        nome_coluna_ano: str,
        nome_coluna_valor: str,
        nome_coluna_tipo: str = None,
        nome_material: str = None,
        nome_antigo_pais: str = None,
        nome_novo_pais: str = None,
        nome_coluna_preco: str = None
) -> pd.DataFrame:
    """
    Processa um arquivo CSV realizando operações de transformação e limpeza dos dados.

    Parâmetros:
    arquivo_nome (str): Nome do arquivo CSV a ser processado.
    sep_arquivo (str): Separador utilizado no arquivo CSV (por exemplo, ',' ou ';').
    colunas_a_manter (list): Lista com os nomes das colunas que devem ser mantidas no DataFrame final.
    colunas_a_remover (list): Lista com os nomes das colunas que devem ser removidas do DataFrame.
    nome_coluna_controle (str): Nome da coluna que será renomeada para 'nome_coluna_controle'.
    nome_coluna_ano (str): Nome da nova coluna que representará os anos após a transposição dos dados.
    nome_coluna_valor (str): Nome da nova coluna que conterá os valores após a transposição dos dados.
    nome_coluna_tipo (str, opcional): Nome da coluna que será adicionada ao DataFrame com o valor de 'nome_material'.
    nome_material (str, opcional): Valor que será atribuído à coluna 'nome_coluna_tipo'.
    nome_antigo_pais (str, opcional): Nome da coluna que deve ser renomeada para 'nome_novo_pais'.
    nome_novo_pais (str, opcional): Novo nome para a coluna 'nome_antigo_pais'.

    Retorna:
    pd.DataFrame: DataFrame processado conforme as especificações fornecidas.
    """

    # Lendo o arquivo CSV
    arquivo = pd.read_csv(arquivo_nome, sep=sep_arquivo, decimal=',')

    # Removendo colunas desnecessárias
    arquivo.drop(columns=colunas_a_remover, inplace=True)

    # Identificando colunas que serão transpostas (ou seja, que não estão na lista de colunas a manter)
    colunas_a_transpor = [coluna for coluna in arquivo.columns if coluna not in colunas_a_manter]

    # Transpondo o DataFrame: as colunas identificadas serão transformadas em linhas
    arquivo = arquivo.melt(id_vars=colunas_a_manter, value_vars=colunas_a_transpor, var_name=nome_coluna_ano,
                           value_name=nome_coluna_valor)

    # Renomeando a coluna de controle
    arquivo.rename(columns={nome_coluna_controle: nome_coluna_controle}, inplace=True)

    # Substituindo valores ausentes e específicos por zero
    arquivo = arquivo.fillna(0)
    arquivo = arquivo.replace('nd', 0)
    arquivo = arquivo.replace('*', 0)
    arquivo = arquivo.replace('+', 0)

    # Adicionando a coluna 'nome_coluna_tipo' com o valor 'nome_material' se especificado
    if nome_material is not None and nome_coluna_tipo is not None:
        arquivo[nome_coluna_tipo] = nome_material

    # Renomeando coluna de país se necessário
    if nome_antigo_pais is not None and nome_novo_pais is not None:
        arquivo.rename(columns={nome_antigo_pais: nome_novo_pais}, inplace=True)

    # Define o tipo int para a coluna nome_coluna_valor
    arquivo[nome_coluna_valor] = arquivo[nome_coluna_valor].astype(int)

    if nome_coluna_preco:
        arquivo = separar_preco_quantidade(df_arquivo=arquivo,
                                           nome_coluna_ano=nome_coluna_ano,
                                           nome_coluna_valor=nome_coluna_valor,
                                           nome_coluna_tipo=nome_coluna_tipo,
                                           nome_novo_pais=nome_novo_pais,
                                           nome_coluna_preco=nome_coluna_preco)

    return arquivo


def separar_preco_quantidade(df_arquivo, 
                             nome_coluna_ano: str, 
                             nome_coluna_valor: str, 
                             nome_coluna_tipo: str, 
                             nome_novo_pais: str, 
                             nome_coluna_preco: str):
    
    # Regex para identificar anos com ponto. Exemplo: 1970.1, 1971.1, 1972.1
    regex_ano_com_ponto = r'^\d{4}\.1$'

    # Filtra os valores para a coluna preco.
    df_arquivo[nome_coluna_preco] = df_arquivo[nome_coluna_valor].where(df_arquivo[nome_coluna_ano].str.match(regex_ano_com_ponto))
    
    # Filtra os valores para coluna quantidade.
    df_arquivo[nome_coluna_valor] = df_arquivo[nome_coluna_valor].where(~df_arquivo[nome_coluna_ano].str.match(regex_ano_com_ponto))

    # Remove ".1" das linhas da coluna ano.
    df_arquivo[nome_coluna_ano] = df_arquivo[nome_coluna_ano].apply(lambda x: x.split('.')[0]) 
    
    # Substitui NaN por 0.
    df_arquivo.fillna(0, inplace=True)

    # Agrupa por pais e ano e aplica a soma nas colunas preco e quantidade para eliminar os ZEROS e unificar as linhas. 
    df_arquivo_gp = df_arquivo.groupby([nome_novo_pais, nome_coluna_ano, nome_coluna_tipo]).agg({nome_coluna_valor: 'sum', nome_coluna_preco: 'sum'}).reset_index()

    # Define a coluna quantidade com o tipo int. 
    df_arquivo_gp[nome_coluna_valor] = df_arquivo_gp[nome_coluna_valor].astype(int)

    return df_arquivo_gp

