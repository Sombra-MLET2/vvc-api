import logging

import schedule

from appscheduler.utils import wrap_pre_execute
from scraping.scraping import map_site, download_all_csv


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def configure_scheduler():
    """
    Configura o agendador para executar uma funcao (tarefa) a cada x tempo.
    Tarefas com <.tag("run_on_startup")> sao executadas imediantamente ao inicar a aplicacao.
    """

    func_map_site = wrap_pre_execute(map_site)
    schedule.every(30).minutes.do(func_map_site)

    func_download_all_csv = wrap_pre_execute(download_all_csv)
    schedule.every(30).minutes.do(func_download_all_csv).tag("run_on_startup")
