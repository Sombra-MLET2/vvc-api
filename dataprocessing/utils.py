import pandas as pd

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
        nome_novo_pais: str = None
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

    # Adicionando a coluna 'nome_coluna_tipo' com o valor 'nome_material' se especificado
    if nome_material is not None and nome_coluna_tipo is not None:
        arquivo[nome_coluna_tipo] = nome_material

    # Renomeando coluna de país se necessário
    if nome_antigo_pais is not None and nome_novo_pais is not None:
        arquivo.rename(columns={nome_antigo_pais: nome_novo_pais}, inplace=True)

    return arquivo

def read_all_files():
    producao_csv = trata_csv('Producao.csv', ';', ['control'], ['id', 'produto'], 'name', 'year', 'quantity')
    processa_viniferas = trata_csv('ProcessaViniferas.csv', ';', ['control'], ['id', 'cultivar'], 'cultivation', 'year',
                                   'quantity')
    ProcessaMesa_csv = trata_csv('ProcessaMesa.csv', '\t', ['control'], ['id', 'cultivar'], 'cultivation', 'year',
                                 'quantity')
    ProcessaSemclass_csv = trata_csv('ProcessaSemclass.csv', '\t', ['control'], ['id', 'cultivar'], 'cultivation',
                                     'year', 'quantity')
    ProcessaAmericanas_csv = trata_csv('ProcessaAmericanas.csv', '\t', ['control'], ['id', 'cultivar'], 'cultivation',
                                       'year', 'quantity')
    comercio_csv = trata_csv('Comercio.csv', ';', ['control'], ['id', 'Produto'], 'name', 'year', 'quantity')
    impVinhos_csv = trata_csv('ImpVinhos.csv', ';', ['País'], ['Id'], 'cultivation', 'year', 'quantity', 'category',
                              'Vinhos', 'País', 'country')
    impEspumantes_csv = trata_csv('ImpEspumantes.csv', ';', ['País'], ['Id'], 'cultivation', 'year', 'quantity',
                                  'category', 'Espumantes', 'País', 'country')
    impFrescas_csv = trata_csv('ImpFrescas.csv', ';', ['País'], ['Id'], 'cultivation', 'year', 'quantity', 'category',
                               'Frescas', 'País', 'country')
    impPassas_csv = trata_csv('ImpPassas.csv', ';', ['País'], ['Id'], 'cultivation', 'year', 'quantity', 'category',
                              'Passas', 'País', 'country')
    impSuco_csv = trata_csv('ImpSuco.csv', ';', ['País'], ['Id'], 'cultivation', 'year', 'quantity', 'category',
                            'Passas', 'País', 'country')
    expSuco_csv = trata_csv('ExpSuco.csv', ';', ['País'], ['Id'], 'cultivation', 'year', 'quantity', 'category',
                            'Sucos', 'País', 'country')
    expVinho_csv = trata_csv('ExpVinho.csv', ';', ['País'], ['Id'], 'cultivation', 'year', 'quantity', 'category',
                             'Vinhos', 'País', 'country')
    expEspumantes_csv = trata_csv('ExpEspumantes.csv', ';', ['País'], ['Id'], 'cultivation', 'year', 'quantity',
                                  'category', 'Espumantes', 'País', 'country')
    expUva_csv = trata_csv('ExpUva.csv', ';', ['País'], ['Id'], 'cultivation', 'year', 'quantity', 'category', 'Uvas',
                           'País', 'country')



