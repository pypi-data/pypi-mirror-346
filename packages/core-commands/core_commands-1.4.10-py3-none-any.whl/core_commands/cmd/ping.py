from ..bin.cmd import cmd

def ping(arguments: str|None = None):
    """
    Envía un ping a un host y retorna el resultado.

    Args:
        arguments (str|None): Dirección IP o nombre del host al que se le envía el ping.

    Returns:
        str: Respuesta del ping (ej. "¡Pong!" o un mensaje de error).

    Raises:
        ValueError: Si el host está vacío o el timeout es negativo.
    """
    return cmd(f"ping {arguments}")