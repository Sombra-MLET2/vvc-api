import logging
from pathlib import Path

from sqlalchemy.orm import Session

from comn import constants
from dataprocessing.parsears import exports_parser, imports_parser, processing_parser, production_parser, sale_parser
from infra.database.database import get_db
from utils.os_utils import move_file


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

running: bool = False

csv_parsing_router = {
    constants.csvs.EXPORTS: exports_parser,
    constants.csvs.IMPORTS: imports_parser,
    constants.csvs.PROCESSING: processing_parser,
    constants.csvs.PRODUCTION: production_parser,
    constants.csvs.SALE: sale_parser
}


def _forward_to_parser(csv_file: Path):
    csv_file_prefix = csv_file.name.split("-")[0]

    parser_router = csv_parsing_router.get(csv_file_prefix, None)
    if parser_router:
        try:
            session_db: Session = get_db()
            parser_router.process_file(csv_file_path=str(csv_file), db=next(session_db))
            _move_processed_file(constants.PATH_PROCESSED_FILES, csv_file)
        except Exception as e:
            logger.exception(f"Erro no processamento do arquivo [{csv_file.name}].", e)
            _move_processed_file(constants.PATH_ERROR_FILES, csv_file)
    else:
        logger.error(f"Arquivo [{csv_file.name}], nao reconhecido para parser.")
        _move_processed_file(constants.PATH_UNKNOWN_FILES, csv_file)


def _move_processed_file(path_parent: Path, csv_file: Path):
    destination_file = Path(path_parent).joinpath(csv_file.name)
    move_file(origin_path=csv_file, destination_path=destination_file)


def start_parser_files():
    logger.info("Start data processing...")
    
    global running
    if running:
        logger.info("Data processing is running.")
        return
    else:
        running = True        

    path_files = Path(constants.PATH_DOWNLOADED_FILES)
    only_csv_files = list(path_files.glob('*.csv'))

    for csv_file in only_csv_files:
        _forward_to_parser(csv_file)

    logger.info("End data processing.")

