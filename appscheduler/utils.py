import logging
import schedule

def wrap_pre_execute(func):
    """
    Envolve uma funcao para ser executada dentro do contexto de __pre_execute.

    Args:
        func (callable): A funcao a ser envolvida.

    Returns:
        callable: Uma funcao lambda que chama pre_execute com a funcao fornecida e seus argumentos.
    """
    return lambda *args, **kwargs: __pre_execute(func, *args, **kwargs)


def __pre_execute(function, *args, **kwargs):
    """
    Executa uma funcao recebida por parametro.

    Registra a execução da funcao, incluindo seu nome, argumentos posicionais e argumentos nomeados.
    Se ocorrer uma excecao durante a execução, registra a excecao e cancela a tarefa agendada.

    Por que?
        Quando a biblioteca Schedule executa uma funcao agendada e ocorre uma excecao, todo o processo do eh interrompido.
        Para capturar a excecao, uma possivel solucao, eh criar um mehtodo que envolva a funcao chamada e trate a excecao.

    Args:
        function (callable): A funcao a ser executada.
        *args: Argumentos posicionais a serem passados para a funcao.
        **kwargs: Argumentos nomeados a serem passados para a funcao.

    Returns:
        schedule.CancelJob: Se ocorrer uma excecao, retorna CancelJob para cancelar a tarefa agendada.
    """
    try:
        logging.info(f'Em execução function [{function.__name__}()] com args: {args} e kwargs: {kwargs}')
        function(*args, **kwargs)
    except Exception as e:
        logging.exception("Erro ao executar uma tarefa agendada.")
        return schedule.CancelJob
