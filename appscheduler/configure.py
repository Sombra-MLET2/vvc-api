import logging

import schedule

from appscheduler.utils import wrap_pre_execute
from dataprocessing import start_parser_files
from scraping.scraping import map_site, download_all_csv


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


RUN_ON_STARTUP: str = "run_on_startup"


def configure_scheduler():
    """
    Configura o agendador para executar uma funcao (tarefa) a cada x tempo.
    Tarefas com <.tag("run_on_startup")> sao executadas imediantamente ao inicar a aplicacao.
    """

    func_map_site = wrap_pre_execute(map_site)
    schedule.every(30).minutes.do(func_map_site)

    func_download_all_csv = wrap_pre_execute(download_all_csv)
    schedule.every(30).minutes.do(func_download_all_csv).tag(RUN_ON_STARTUP)

    func_start_parser_files = wrap_pre_execute(start_parser_files)
    schedule.every(30).minutes.do(func_start_parser_files).tag(RUN_ON_STARTUP)