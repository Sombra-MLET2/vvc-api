from sqlalchemy.orm import Session

from dataprocessing import utils
from dataprocessing.parsears import common_parser
from dtos import ProcessingDTO
from repositories import processing_repository

def process_file(csv_file_path: str, db: Session):
    
    sep_file = get_sep_file(csv_file_path=csv_file_path)
    
    df_processing = utils.trata_csv(arquivo_nome=str(csv_file_path),
                                    sep_arquivo=sep_file,
                                    colunas_a_manter=['control', 'cultivar'],
                                    colunas_a_remover=['id'],
                                    nome_coluna_controle='cultivation',
                                    nome_coluna_ano='year',
                                    nome_coluna_valor='quantity')

    assert utils.validate_numeric_column(df_processing, 'year', 'quantity') == True

    data_to_insert: list = []

    for _, row in df_processing.iterrows():
        category_id = common_parser.get_category(db=db, meta_name=str(row['control']))

        processing_dto = ProcessingDTO(id=None,
                                       cultivation=row['cultivar'],
                                       quantity=row['quantity'],
                                       year=row['year'],
                                       category_id=category_id,
                                       grape_class_id=category_id)

        processing_exists = processing_repository.find_one(db=db, dto=processing_dto)
        if not processing_exists:
            data_to_insert.append(processing_dto)

    if data_to_insert:
        processing_repository.create_new(db=db, data=data_to_insert)
    else:
        raise Exception(f"The data from the {csv_file_path} file has already been inserted into the database previously..")
    

def get_sep_file(csv_file_path: str) -> str:
    sep = ';'
    if "processamento-viniferas" not in csv_file_path:
        sep = '\t'
    return sep