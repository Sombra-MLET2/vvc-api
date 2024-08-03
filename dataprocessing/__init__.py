import logging
from pathlib import Path

from comn import constants
from dataprocessing.parsears import exports_parser, imports_parser, processing_parser, production_parser, sale_parser
from utils.os_utils import move_file

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
            parser_router.process_file(csv_file.name)
            _move_processed_file(constants.PATH_PROCESSED_FILES, csv_file)
        except Exception as e:
            logger.exception(f"Erro no processamento do arquivo [{csv_file.name}].", str(e))
            _move_processed_file(constants.PATH_ERROR_FILES, csv_file)
    else:
        logger.error(f"Arquivo [{csv_file.name}], nao reconhecido para parser.")
        _move_processed_file(constants.PATH_UNKNOWN_FILES, csv_file)


def _move_processed_file(path_parent: Path, csv_file: Path):
    destination_file = Path(path_parent).joinpath(csv_file.name)
    move_file(origin_path=csv_file, destination_path=destination_file)


def start_parser_files():
    path_files = Path(constants.PATH_DOWNLOADED_FILES)
    only_csv_files = list(path_files.glob('*.csv'))

    for csv_file in only_csv_files:
        _forward_to_parser(csv_file)


