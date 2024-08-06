from sqlalchemy.orm import Session

from dataprocessing import utils
from dataprocessing.parsears import common_parser
from dtos import ImportDTO
from repositories import imports_repository


def process_file(csv_file_path: str, db: Session):
   
   nome_material = get_nome_material(csv_file_path)
   
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
   
   assert utils.validate_numeric_column(df_import, 'year', 'quantity') == True

   data_to_insert: list = []

   for _, row in df_import.iterrows():
      category_id = common_parser.get_category(db=db, meta_name=str(row['category']))
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
      raise Exception(f"The data from the {csv_file_path} file has already been inserted into the database previously..")


def get_nome_material(csv_file_path: str) -> str:
   material = ';'
   if "importacao-espumantes" in csv_file_path:
      material = 'espumantes'.upper()
   elif "importacao-suco-de-uva" in csv_file_path:
        material = 'suco de uva'.upper()
   elif "importacao-uvas-frescas" in csv_file_path:
        material = 'uvas frescas'.upper()
   elif "importacao-uvas-passas" in csv_file_path:
        material = 'uvas frescas'.upper()                        
   elif "importacao-vinhos-de-mesa" in csv_file_path:
        material = 'vinhos de mesa'.upper()            
   return material

