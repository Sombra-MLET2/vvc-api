import logging
import threading
import time

import schedule

from appscheduler.configure import configure_scheduler as configuration


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Scheduler:
    """
    Classe para gerenciar o scheduler de tarefas.
    """

    def __init__(self, configure_scheduler):
        """
        Inicializa uma nova instância da classe Scheduler.

        Args:
            configure_scheduler (function): Função para configurar o scheduler.
        """
        self.api_running = True
        self.configure_scheduler = configure_scheduler
        logging.info("Scheduler initialized")

    def __run_scheduler(self):
        """
        Mehtodo privado que executa o loop do scheduler enquanto api_running for True.

        Este mehtodo realiza as seguintes acoes:
        1. Executa todos os jobs agendados com a tag 'run_on_startup' imediatamente chamando o mehtodo run_on_startup.
        2. Entra em um loop que continua enquanto api_running for True, executando os jobs pendentes e registrando uma mensagem de debug.
        """
        self.run_on_startup()
        while self.api_running:
            schedule.run_pending()
            time.sleep(1)
            logging.debug("Scheduler running")

    def run_on_startup(self):
        """
        Executa todos os jobs agendados com a tag 'run_on_startup' imediatamente ao iniciar o Scheduler.
        """
        for job in schedule.get_jobs("run_on_startup"):
            logging.info(f'run_on_startup job{job}')
            job.run()

    def start(self):
        """
        Função que:
         - limpa o scheduler antes de iniciar, para evitar lixo de memória. 
         - Configura o scheduler com as tarefas definida no arquivo configure.py.
         - Inicializa o scheduler em uma Thread segregada para que o mesmo possa rodar isolado do FastAPI. 
        """
        schedule.clear()

        self.configure_scheduler()

        self.scheduler_thread = threading.Thread(target=self.__run_scheduler)
        self.scheduler_thread.start()

        logging.info("Scheduler started")

    def stop(self):
        """
        Para o scheduler, definindo api_running como False.
        """
        self.api_running = False

        logging.info("Scheduler stopped")


scheduler = Scheduler(configuration)


def start_scheduler():
    """
    Funcao para iniciar o Scheduler.
    """
    scheduler.start()
    logging.info(f'Tarefas iniciadas {schedule.get_jobs()}')


def stop_scheduler():
    """
    Funcao para parar o Scheduler.
    """
    scheduler.stop()
    logging.info(f'Tarefas paralizadas {schedule.get_jobs()}')

