import pandas as pd
#import pytest
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
    arquivo = arquivo.replace('+', 0)

    # Adicionando a coluna 'nome_coluna_tipo' com o valor 'nome_material' se especificado
    if nome_material is not None and nome_coluna_tipo is not None:
        arquivo[nome_coluna_tipo] = nome_material

    # Renomeando coluna de país se necessário
    if nome_antigo_pais is not None and nome_novo_pais is not None:
        arquivo.rename(columns={nome_antigo_pais: nome_novo_pais}, inplace=True)

    return arquivo


def read_all_files():
    '''
    ================================
    Os codigos fonte abaixo comentado estão sendo migrados para os seus respectivos 
    parsers em: “./parsears/*_parser.py”.
    ================================
    '''

    # Arquivo de produção
    #producao_csv = trata_csv('Producao.csv', ';', ['control'], ['id', 'produto'], 'name', 'year', 'quantity')

    #assert validate_numeric_column(producao_csv, 'year', 'quantity') == True

    #Arquivos de processamento
    processa_viniferas_csv = trata_csv('ProcessaViniferas.csv', ';', ['control'], ['id', 'cultivar'], 'cultivation', 'year',
                                   'quantity')

    assert validate_numeric_column(processa_viniferas_csv, 'year', 'quantity') == True

    processa_mesa_csv = trata_csv('ProcessaMesa.csv', '\t', ['control'], ['id', 'cultivar'], 'cultivation', 'year',
                                 'quantity')

    assert validate_numeric_column(processa_mesa_csv,'year','quantity') == True

    processa_sem_class_csv = trata_csv('ProcessaSemclass.csv', '\t', ['control'], ['id', 'cultivar'], 'cultivation',
                                     'year', 'quantity')

    assert validate_numeric_column(processa_sem_class_csv,'year','quantity') == True

    processa_americanas_csv = trata_csv('ProcessaAmericanas.csv', '\t', ['control'], ['id', 'cultivar'], 'cultivation',
                                       'year', 'quantity')

    assert validate_numeric_column(processa_americanas_csv,'year','quantity') == True

    # Arquivo de Comercio
    #comercio_csv = trata_csv('Comercio.csv', ';', ['control'], ['id', 'Produto'], 'name', 'year', 'quantity')

    #assert validate_numeric_column(comercio_csv, 'year', 'quantity') == True

    # Arquivos de Importação
    impVinhos_csv = trata_csv('ImpVinhos.csv', ';', ['País'], ['Id'], 'cultivation', 'year', 'quantity', 'category',
                              'Vinhos', 'País', 'country')

    assert validate_numeric_column(impVinhos_csv, 'year', 'quantity') == True

    impEspumantes_csv = trata_csv('ImpEspumantes.csv', ';', ['País'], ['Id'], 'cultivation', 'year', 'quantity',
                                  'category', 'Espumantes', 'País', 'country')

    assert validate_numeric_column(impEspumantes_csv, 'year', 'quantity') == True

    impFrescas_csv = trata_csv('ImpFrescas.csv', ';', ['País'], ['Id'], 'cultivation', 'year', 'quantity', 'category',
                               'Frescas', 'País', 'country')

    assert validate_numeric_column(impFrescas_csv, 'year', 'quantity') == True

    impPassas_csv = trata_csv('ImpPassas.csv', ';', ['País'], ['Id'], 'cultivation', 'year', 'quantity', 'category',
                              'Passas', 'País', 'country')

    assert validate_numeric_column(impPassas_csv, 'year', 'quantity') == True

    impSuco_csv = trata_csv('ImpSuco.csv', ';', ['País'], ['Id'], 'cultivation', 'year', 'quantity', 'category',
                            'Passas', 'País', 'country')

    assert validate_numeric_column(impSuco_csv,'year','quantity') == True

    #Arquivos de Exportação
    expSuco_csv = trata_csv('ExpSuco.csv', ';', ['País'], ['Id'], 'cultivation', 'year', 'quantity', 'category',
                            'Sucos', 'País', 'country')

    assert validate_numeric_column(expSuco_csv,'year','quantity') == True

    expVinho_csv = trata_csv('ExpVinho.csv', ';', ['País'], ['Id'], 'cultivation', 'year', 'quantity', 'category',
                             'Vinhos', 'País', 'country')

    assert validate_numeric_column(expVinho_csv,'year','quantity') == True


    expEspumantes_csv = trata_csv('ExpEspumantes.csv', ';', ['País'], ['Id'], 'cultivation', 'year', 'quantity',
                                  'category', 'Espumantes', 'País', 'country')

    assert validate_numeric_column(expEspumantes_csv,'year','quantity') == True

    expUva_csv = trata_csv('ExpUva.csv', ';', ['País'], ['Id'], 'cultivation', 'year', 'quantity', 'category', 'Uvas',
                           'País', 'country')

    assert validate_numeric_column(expUva_csv,'year','quantity') == True



