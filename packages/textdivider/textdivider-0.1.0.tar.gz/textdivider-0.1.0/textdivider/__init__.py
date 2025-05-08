def split_text(text: str, max_length: int = 280) -> list[str]:
    """
    Divide un texto largo en partes sin cortar palabras, con un máximo de caracteres por parte.

    Args:
        text (str): Texto a dividir.
        max_length (int): Número máximo de caracteres por fragmento.

    Returns:
        list[str]: Lista de fragmentos de texto.
    """
    if len(text) <= max_length:
        return [text]

    words = text.split()
    parts = []
    current = ""

    for word in words:
        if len(current) + len(word) + 1 <= max_length:
            current += (" " if current else "") + word
        else:
            parts.append(current)
            current = word
    if current:
        parts.append(current)

    return parts
