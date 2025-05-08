from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import time
from .core import EmailMasterPT

class AgendadorEmails:
    def __init__(self):
        self.agendador = BackgroundScheduler()
        self.agendador.start()
        self.tarefas = {}
        
    def agendar_email(self, email_master, data_envio, destinatario, assunto, corpo, anexos=None, cc=None, cco=None, id_tarefa=None):
        """
        Agenda um email para ser enviado em um horário específico
        
        Args:
            email_master (EmailMasterPT): Instância do EmailMasterPT
            data_envio (datetime): Quando enviar o email
            destinatario (str/list): Email(s) do(s) destinatário(s)
            assunto (str): Assunto do email
            corpo (str): Corpo do email
            anexos (list): Lista de caminhos de arquivos
            cc (str/list): Destinatários em cópia
            cco (str/list): Destinatários em cópia oculta
            id_tarefa (str): Identificador opcional da tarefa
            
        Returns:
            str: ID da tarefa
        """
        if not isinstance(data_envio, datetime):
            raise ValueError("data_envio deve ser um objeto datetime")
            
        if not id_tarefa:
            id_tarefa = f"email_{int(time.time())}"
            
        tarefa = self.agendador.add_job(
            email_master.enviar_email,
            'date',
            run_date=data_envio,
            args=[destinatario, assunto, corpo],
            kwargs={'anexos': anexos, 'cc': cc, 'cco': cco},
            id=id_tarefa
        )
        
        self.tarefas[id_tarefa] = tarefa
        return id_tarefa
        
    def cancelar_email(self, id_tarefa):
        """Cancela um email agendado"""
        if id_tarefa in self.tarefas:
            self.tarefas[id_tarefa].remove()
            del self.tarefas[id_tarefa]
            
    def listar_emails_agendados(self):
        """Lista todos os emails agendados"""
        return [{
            'id': tarefa.id,
            'proximo_envio': tarefa.next_run_time,
            'destinatarios': tarefa.args[0] if len(tarefa.args) > 0 else None
        } for tarefa in self.tarefas.values()]
        
    def encerrar(self):
        """Encerra o agendador"""
        self.agendador.shutdown()