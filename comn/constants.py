from datetime import datetime
from typing import Final
from pathlib import Path


# Diretorio home do usuario.
USER_HOME: Final = Path.home()

# Nome da pasta raiz da aplicacao.
APP_ROOT_FOLDER: Final = "vvc-api"

# Caminho completo do diretorio da aplicacao em u
APP_ROOT_PATH: Final = USER_HOME.joinpath(APP_ROOT_FOLDER)

# Caminho para a pasta de arquivos baixados
PATH_DOWNLOADED_FILES: Final = APP_ROOT_PATH.joinpath("files/downloaded/")

# Caminho para a pasta destino dos arquivos com erro no processamento. 
PATH_ERROR_FILES: Final = APP_ROOT_PATH.joinpath("files/error/")

# Caminho para a pasta de arquivos pos processados
PATH_PROCESSED_FILES: Final = APP_ROOT_PATH.joinpath("files/processed/")

# Caminho para a pasta de arquivos nao reconhecidos pelo parser.
PATH_UNKNOWN_FILES: Final = APP_ROOT_PATH.joinpath("files/unknown/")

# Expressao regular para limpar nomes de arquivos (remove caracteres nao alfanumricos e hifens)
REGEX_FILE_NAME_CLENER = r"[^A-Za-z0-9\-]"

# Cria o nome do arquivo CSV com base no nome e timestamp
CSV_FILE = lambda name, timestamp: f'{name}-{timestamp}.csv'

# Cria o caminho completo para o arquivo CSV baixado
FULL_CSV_FILE_DOWNLOAD_PATH = lambda name, timestamp: PATH_DOWNLOADED_FILES.joinpath(CSV_FILE(name=name, timestamp=timestamp))

# Prefixos dos arquivos CSVs baixados. 
class csvs:
    EXPORTS = "exportacao"
    IMPORTS = "importacao"
    PROCESSING = "processamento"
    PRODUCTION = "producao"
    SALE = "comercializacao"
