def split_text(text: str, max_length: int = 280, numbered: bool = False) -> list[str]:
    """
    Split a long string into chunks without cutting words, optionally numbered.

    Args:
        text (str): The input text to split.
        max_length (int): Maximum length per chunk (default 280).
        numbered (bool): Whether to prefix parts with "1/3:", etc.

    Returns:
        list[str]: List of text chunks.
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

    if numbered:
        total = len(parts)
        parts = [f"{i+1}/{total}: {part}" for i, part in enumerate(parts)]

    return parts


def split_by_words(text: str, max_words: int = 50) -> list[str]:
    """
    Split a text into parts with a maximum number of words.

    Args:
        text (str): The input text.
        max_words (int): Max number of words per part.

    Returns:
        list[str]: List of text parts.
    """
    words = text.split()
    return [" ".join(words[i : i + max_words]) for i in range(0, len(words), max_words)]


__help__ = """
textdivider - Split long text into chunks without breaking words.

Functions:
  - split_text(text, max_length=280, numbered=False)
      → Split text into character-limited chunks, optionally numbered.

  - split_by_words(text, max_words=50)
      → Split text into chunks of max N words.

Example:
  >>> from textdivider import split_text
  >>> split_text("This is a long text", max_length=10)
  ['This is a', 'long text']

  >>> split_text("This is a long text", max_length=10, numbered=True)
  ['1/2: This is a', '2/2: long text']
"""
