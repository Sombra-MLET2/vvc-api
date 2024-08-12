from sqlalchemy.orm import Session

from dataprocessing import utils
from dataprocessing.parsears import common_parser
from dataprocessing.tests import validate_numeric_column
from dtos import ProcessingDTO
from repositories import processing_repository


def process_file(csv_file_path: str, db: Session):

    categoria_submenu, categoria_meta_nome = get_catagoria_in_submenu(csv_file_path)
    category_id = common_parser.get_category(db=db, name=categoria_submenu, meta_name=categoria_meta_nome)

    sep_file = get_sep_file(csv_file_path=csv_file_path)

    df_processing = utils.trata_csv(arquivo_nome=str(csv_file_path),
                                    sep_arquivo=sep_file,
                                    colunas_a_manter=['cultivar'],
                                    colunas_a_remover=['id', 'control'],
                                    nome_coluna_controle='cultivation',
                                    nome_coluna_ano='year',
                                    nome_coluna_valor='quantity',
                                    nome_coluna_duplicidade='cultivar')

    assert validate_numeric_column(df_processing, 'year', 'quantity') == True

    data_to_insert: list = []

    for _, row in df_processing.iterrows():
        grape_class_id = common_parser.get_category(db=db,
                                                    name=str(row['category_name']),
                                                    meta_name=str(row['category_meta_name']))

        processing_dto = ProcessingDTO(id=None,
                                       cultivation=row['cultivar'],
                                       quantity=row['quantity'],
                                       year=row['year'],
                                       category_id=category_id,
                                       grape_class_id=grape_class_id)

        processing_exists = processing_repository.find_one(
            db=db, dto=processing_dto)
        if not processing_exists:
            data_to_insert.append(processing_dto)

    if data_to_insert:
        processing_repository.create_new(db=db, data=data_to_insert)
    else:
        raise Exception(f"The data from the {
                        csv_file_path} file has already been inserted into the database previously..")


def get_sep_file(csv_file_path: str) -> str:
    sep = ';'
    if "processamento-viniferas" not in csv_file_path:
        sep = '\t'
    return sep


def get_catagoria_in_submenu(csv_file_path: str) -> str:
    categoria_nome = ''
    categoria_meta_nome = ""

    if "processamento-americanas-e-hibridas" in csv_file_path:
        categoria_nome = 'americanas e hibridas'.upper()
        categoria_meta_nome = "usehb_"
    elif "processamento-sem-classificacao" in csv_file_path:
        categoria_nome = 'SEM CLASSIFICACAO'
        categoria_meta_nome = "sc"
    elif "processamento-uvas-de-mesa" in csv_file_path:
        categoria_nome = 'UVA DE MESA'
        categoria_meta_nome = "uvm_"
    elif "processamento-viniferas" in csv_file_path:
        categoria_nome = 'VINHO FINO DE MESA'
        categoria_meta_nome = "vv_"
    return categoria_nome, categoria_meta_nome
