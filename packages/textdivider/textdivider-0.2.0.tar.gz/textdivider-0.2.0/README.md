# textdivider

Split long text into chunks without breaking words. Useful for social media, messaging platforms, or UI components with length limits.

## Installation

```bash
pip install textdivider
```

# Features

✅ Split text by max characters, preserving whole words

✅ Optional numbering (e.g. "1/3: ...")

✅ Split text by max number of words

# Usage

```python
from textdivider import split_text, split_by_words

text = "This is a long message that you want to divide into parts without cutting words in the middle."

# Split by character count
chunks = split_text(text, max_length=50)
print(chunks)

# With numbering
numbered = split_text(text, max_length=50, numbered=True)
print(numbered)

# Split by word count
word_chunks = split_by_words(text, max_words=5)
print(word_chunks)

```
