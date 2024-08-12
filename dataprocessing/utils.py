import pandas as pd
import re
#from dataprocessing.tests import validate_numeric_column

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
        nome_coluna_preco: str = None,
        nome_coluna_duplicidade: str = None, 
        itens_isolar: list = None,
        tratar_vm_erro: bool = False
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

    # Verifica se no arquivo existe a coluna 'control'.
    # Caso exista, faz o tratamento das categorias. 
    if ('control' in arquivo.columns) and nome_coluna_duplicidade:
        arquivo['control'] = arquivo['control'].apply(tratar_espacamento)
        arquivo[nome_coluna_duplicidade] = arquivo[nome_coluna_duplicidade].apply(tratar_espacamento)

        if arquivo['control'].any():
            # Substitui os valores NaN na coluna 'control' pelos valores correspondentes da coluna especificada em nome_coluna_duplicidade.
            arquivo['control'].fillna(arquivo[nome_coluna_duplicidade], inplace=True)
        
        if tratar_vm_erro:
            arquivo = substituir_vm_por_vv(df=arquivo)

        if itens_isolar:
            arquivo, df_isolados = isolar_linhas_nao_categoria(df_arquivo=arquivo, itens_isolar=itens_isolar)
            
            # Seta a coluna category_name e category_meta_name com o dado da coluna control
            df_isolados.loc[:, 'category_name'] = df_isolados['control']
            df_isolados.loc[:, 'category_meta_name'] = df_isolados['control']

        # Obter categorias a partir da coluna 'control' do arquivo. 
        df_categorias = obter_categorias(df_arquivo=arquivo)

        # Obter apenas o prefixo da coluna 'controll'.
        # Exemplo: vm_Tinto -> vm_
        arquivo['control'] = arquivo['control'].apply(separar_metadata)
        
        # Filtra as linhas onde o valor da coluna 'produto' é diferente do valor da coluna 'categoria'
        arquivo = arquivo[arquivo['control'] != arquivo[nome_coluna_duplicidade]]
        
        #arquivo = merge_com_categoria(df_arquivo=arquivo)
        arquivo = pd.merge(arquivo, df_categorias, left_on='control', right_on='category_meta_name')
        
        if itens_isolar:
            arquivo = pd.concat([arquivo, df_isolados], ignore_index=True)

        colunas_a_manter.append('category_name')
        colunas_a_manter.append('category_meta_name')

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


def obter_categorias(df_arquivo) -> pd.DataFrame:
    _df = pd.DataFrame()
    _df['control'] = df_arquivo['control'].apply(separar_metadata).unique()

    nome = filtrar_dados(df_arquivo=_df, regex=r'^(?!\w{1,}_$).*$', coluna='control')
    meta_nome = filtrar_dados(df_arquivo=_df, regex='^\w{1,}_$', coluna='control')

    df_categorias = pd.DataFrame()
    df_categorias['category_name'] = nome
    df_categorias['category_meta_name'] = meta_nome

    # Tratar [sc == NaN] = Sem classificacao
    df_categorias = tratar_categoria_sc(df=df_categorias)

    return df_categorias
                       

def isolar_linhas_nao_categoria(df_arquivo, itens_isolar):
    itens_isolar_bool = df_arquivo['control'].isin(itens_isolar)      
    df_isolados = df_arquivo.loc[itens_isolar_bool]
    df_arquivo = df_arquivo.loc[~itens_isolar_bool]
    return df_arquivo, df_isolados


def teste():
    # Eemove linhas com totais.
    df_arquivo = df_arquivo[df_arquivo['control'] != df_arquivo['categoria']]


def separar_metadata(cell: str):
    if '_' in cell:
        cell = cell.split('_')[0] + '_'
    return cell


def tratar_espacamento(str_cell):
    try:
        # Remover palavra entre '()', exemplo: (VINIFERA)
        new_str_cell = re.sub(r'^([\s\w]+)\(.*\)', r'\1', str_cell)

        # Remover espacoes inicio e fim da str_cell
        new_str_cell = new_str_cell.strip()

        # Remover espacamento duplo 
        new_str_cell = re.sub(r"(\s+)", ' ', new_str_cell)
    except Exception as e :
        new_str_cell = str_cell
    return new_str_cell


def filtrar_dados(df_arquivo, regex: str, coluna: str  ):
    _df_arquivo = df_arquivo.where(df_arquivo[coluna].str.match(regex))
    _df_arquivo = _df_arquivo.dropna().reset_index()
    return _df_arquivo[coluna]


def substituir_vm_por_vv(df):
    # Localize o dado 'VINHO  FINO DE MESA' na coluna "control"
    str_buscar = 'VINHO FINO DE MESA'
    ext_df_str_buscar = df.loc[df['control'] == str_buscar]

    # Retorne as próximas 3 linhas a partir da linha encontrada
    proximas_3_linhas = df.loc[ext_df_str_buscar.index[0]:ext_df_str_buscar.index[0] + 3]

    # Nas linhas encontradas troca vm_' por 'vv_'.
    proximas_3_linhas['control'] = proximas_3_linhas['control'].apply(lambda x: x.replace('vm_', 'vv_'))

    # Atualiza dataframe com as alteracoes. 
    df.loc[proximas_3_linhas.index, 'control'] = proximas_3_linhas['control']

    return df


def tratar_categoria_sc(df):
    tamanho_df_categorias = df['category_name'].size

    # Verifique se o tamanho é igual a um e se o valor é 'sc'
    if tamanho_df_categorias == 1 and df['category_name'].iloc[0] == 'sc':
        df['category_name'] = 'SEM CLASSIFICACAO'
        df['category_meta_name'] = 'sc'
    
    return df 