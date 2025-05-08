def validar_email(email):
    """Validação básica de email"""
    if '@' not in email or '.' not in email.split('@')[-1]:
        return False
    return True

def formatar_destinatarios(destinatarios):
    """Formata destinatários para envio de email"""
    if isinstance(destinatarios, str):
        return [destinatarios.strip()]
    return [d.strip() for d in destinatarios]