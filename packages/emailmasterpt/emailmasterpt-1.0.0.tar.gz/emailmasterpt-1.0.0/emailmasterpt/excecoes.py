class ErroEmailMaster(Exception):
    """Exceção base para EmailMasterPT"""
    pass

class ErroEnvioEmail(ErroEmailMaster):
    """Falha ao enviar email"""
    pass

class ErroProvedorInvalido(ErroEmailMaster):
    """Configuração inválida do provedor"""
    pass

class ErroConexao(ErroEmailMaster):
    """Falha na conexão com o servidor de email"""
    pass