from .core import EmailMasterPT
from .provedores import ProvedorGmail, ProvedorOutlook, ProvedorSMTP
from .agendador import AgendadorEmails

__all__ = ['EmailMasterPT', 'ProvedorGmail', 'ProvedorOutlook', 'ProvedorSMTP', 'AgendadorEmails']
__version__ = '1.0.0'