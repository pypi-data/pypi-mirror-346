class ProvedorBase:
    def __init__(self, usuario, senha, host=None, porta=None):
        self.usuario = usuario
        self.senha = senha
        self.host = host
        self.porta = porta

class ProvedorGmail(ProvedorBase):
    def __init__(self, usuario, senha):
        super().__init__(usuario, senha, 'smtp.gmail.com', 587)

class ProvedorOutlook(ProvedorBase):
    def __init__(self, usuario, senha):
        super().__init__(usuario, senha, 'smtp.office365.com', 587)

class ProvedorSMTP(ProvedorBase):
    def __init__(self, usuario, senha, host, porta):
        super().__init__(usuario, senha, host, porta)