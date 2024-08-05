from sqlalchemy.orm import Session

from dataprocessing import utils
from dataprocessing.parsears import common_parser
from dtos import SaleDTO
from repositories import sale_repository

def process_file(csv_file_path: str, db: Session):
    df_sale = utils.trata_csv(arquivo_nome=str(csv_file_path),
                              sep_arquivo=';',
                              colunas_a_manter=['control', 'Produto'],
                              colunas_a_remover=['id'],
                              nome_coluna_controle='name',
                              nome_coluna_ano='year',
                              nome_coluna_valor='quantity')

    assert utils.validate_numeric_column(df_sale, 'year', 'quantity') == True

    data_to_insert: list = []

    for _, row in df_sale.iterrows():
        category_id = common_parser.get_category(db=db, meta_name=str(row['control']))

        sale_dto = SaleDTO(id=None,
                           name=row['Produto'],
                           quantity=row['quantity'],
                           year=row['year'],
                           category_id=category_id)

        sale_exists = sale_repository.find_one(db=db, dto=sale_dto)
        if not sale_exists:
            data_to_insert.append(sale_dto)


    if data_to_insert:
        sale_repository.create_new(db=db, data=data_to_insert)
    else:
        raise Exception(f"The data from the {csv_file_path} file has already been inserted into the database previously..")