import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from .excecoes import ErroEnvioEmail, ErroProvedorInvalido

class EmailMasterPT:
    def __init__(self, provedor):
        """
        Inicializa o EmailMasterPT com um provedor
        
        Args:
            provedor: Instância de um provedor (ProvedorGmail, ProvedorOutlook, ProvedorSMTP)
        """
        self.provedor = provedor
        self.servidor = None
        
    def conectar(self):
        """Conecta ao servidor de email"""
        try:
            self.servidor = smtplib.SMTP(self.provedor.host, self.provedor.porta)
            self.servidor.starttls()
            self.servidor.login(self.provedor.usuario, self.provedor.senha)
        except Exception as e:
            raise ConnectionError(f"Falha ao conectar ao servidor: {str(e)}")
    
    def desconectar(self):
        """Desconecta do servidor"""
        if self.servidor:
            self.servidor.quit()
    
    def enviar_email(self, destinatario, assunto, corpo, anexos=None, cc=None, cco=None):
        """
        Envia um email
        
        Args:
            destinatario (str/list): Email(s) do(s) destinatário(s)
            assunto (str): Assunto do email
            corpo (str): Corpo do email (suporta HTML)
            anexos (list): Lista de caminhos de arquivos para anexar
            cc (str/list): Destinatário(s) em cópia
            cco (str/list): Destinatário(s) em cópia oculta
        """
        if not self.servidor:
            self.conectar()
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.provedor.usuario
            msg['Subject'] = assunto
            
            # Trata destinatários
            if isinstance(destinatario, str):
                msg['To'] = destinatario
                destinatarios = [destinatario]
            else:
                msg['To'] = ', '.join(destinatario)
                destinatarios = destinatario
                
            if cc:
                if isinstance(cc, str):
                    msg['Cc'] = cc
                    destinatarios.append(cc)
                else:
                    msg['Cc'] = ', '.join(cc)
                    destinatarios.extend(cc)
                    
            if cco:
                if isinstance(cco, str):
                    destinatarios.append(cco)
                else:
                    destinatarios.extend(cco)
            
            # Adiciona corpo
            msg.attach(MIMEText(corpo, 'html' if '<html>' in corpo.lower() else 'plain'))
            
            # Adiciona anexos
            if anexos:
                for caminho_arquivo in anexos:
                    try:
                        with open(caminho_arquivo, 'rb') as anexo:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(anexo.read())
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename= {caminho_arquivo.split("/")[-1]}'
                        )
                        msg.attach(part)
                    except Exception as e:
                        raise ValueError(f"Falha ao anexar arquivo {caminho_arquivo}: {str(e)}")
            
            # Envia email
            self.servidor.sendmail(self.provedor.usuario, destinatarios, msg.as_string())
            
        except Exception as e:
            raise ErroEnvioEmail(f"Falha ao enviar email: {str(e)}")
        finally:
            self.desconectar()
            