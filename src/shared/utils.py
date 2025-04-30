from datetime import datetime

def get_timestamp() -> str:
    """
    Genera un timestamp en formato legible.
    Returns:
        str: Fecha y hora actual en formato 'YYYY-MM-DD HH:MM:SS'.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")