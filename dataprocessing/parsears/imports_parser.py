from sqlalchemy.orm import Session

from dataprocessing import utils
from dataprocessing.parsears import common_parser
from dataprocessing.tests import validate_numeric_column
from dtos import ImportDTO
from repositories import imports_repository


def process_file(csv_file_path: str, db: Session):

    nome_material, meta_nome = get_nome_material(csv_file_path)
    category_id = common_parser.get_category(db=db, 
                                             name=nome_material, 
                                             meta_name=meta_nome)

    df_import = utils.trata_csv(arquivo_nome=str(csv_file_path),
                                sep_arquivo=';',
                                colunas_a_manter=['País'],
                                colunas_a_remover=['Id'],
                                nome_coluna_controle='cultivation',
                                nome_coluna_ano='year',
                                nome_coluna_valor='quantity',
                                nome_coluna_tipo="category",
                                nome_material=nome_material,
                                nome_antigo_pais="País",
                                nome_novo_pais="country",
                                nome_coluna_preco="value")

    assert validate_numeric_column(df_import, 'year', 'quantity') == True

    data_to_insert: list = []

    for _, row in df_import.iterrows():
        country_id = common_parser.get_country(db=db, name=str(row['country']))

        import_dto = ImportDTO(id=None,
                               quantity=row['quantity'],
                               value=row['value'],
                               year=row['year'],
                               category_id=category_id,
                               country_id=country_id)

        import_exists = imports_repository.find_one(db=db, dto=import_dto)
        if not import_exists:
            data_to_insert.append(import_dto)

    if data_to_insert:
        imports_repository.create_new(db=db, data=data_to_insert)
    else:
        raise Exception(f"The data from the {
                        csv_file_path} file has already been inserted into the database previously..")


def get_nome_material(csv_file_path: str) -> str:
   nome_material = ''
   meta_nome = ""

   if "importacao-espumantes" in csv_file_path:
      nome_material = 'ESPUMANTES'
      meta_nome = 'es_'
   elif "importacao-suco-de-uva" in csv_file_path:
      nome_material = 'SUCO DE UVAS'
      meta_nome = 'su_'
   elif "importacao-uvas-frescas" in csv_file_path:
      nome_material = 'uvas frescas'.upper()
      meta_nome = 'uvsf_'
   elif "importacao-uvas-passas" in csv_file_path:
      nome_material = 'uvas passas'.upper()
      meta_nome = 'uvsp_'
   elif "importacao-vinhos-de-mesa" in csv_file_path:
      nome_material = 'VINHO DE MESA'
      meta_nome = 'vm_'

   return nome_material, meta_nome
