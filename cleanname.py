import re
import string
import time
import unicodedata

KEEP_CHARS_SAME = set(string.ascii_lowercase).union(set(string.digits))
CHANGE_TO_LOWERCASE = set(string.ascii_uppercase)
MAP_TO_SPACE = set(string.punctuation).union(set(string.whitespace))
MAP_TO_SPACE.remove("'")


def normalise(text: str) -> str:
    """
    Replace accented characters with non-accented ones in given text if
    possible or remove if not. Also strip whitespace from start and end, make
    lowercase and replace punctuation with spaces except for ' which is
    replaced with blank.

    Args:
        text (str): Text to normalise

    Returns:
        str: Normalised text
    """
    chars = []
    space = False
    for chr in unicodedata.normalize("NFD", text):
        if chr in KEEP_CHARS_SAME:
            chars.append(chr)
            space = False
        elif chr in CHANGE_TO_LOWERCASE:
            chars.append(chr.lower())
            space = False
        elif chr in MAP_TO_SPACE:
            if space:
                continue
            chars.append(" ")
            space = True
    return "".join(chars).strip()


notwanted = re.compile(r"[^'a-zA-Z0-9\s]")
spaces = re.compile(r" +")
def normalise2(text: str) -> str:
    """
    Replace accented characters with non-accented ones in given text if
    possible or remove if not. Also strip whitespace from start and end, make
    lowercase and replace punctuation with spaces except for ' which is
    replaced with blank.

    Args:
        text (str): Text to normalise

    Returns:
        str: Normalised text
    """
    text = unicodedata.normalize("NFD", text)
    text_clean = notwanted.sub(" ", text)
    text_clean = spaces.sub(" ", text_clean)
    return text_clean.strip()

text = "£^*& ()+-[]<>?|\\ Al DhaleZ'eÉ / الضالع,,..1234''#~~### "
start = time.perf_counter()
for i in range(100):
    normalise(text)
print(normalise(text))
end = time.perf_counter()
elapsed = end - start
print(f'Time taken: {elapsed:.6f} seconds')

start = time.perf_counter()
for i in range(100):
    normalise2(text)
print(normalise2(text))
end = time.perf_counter()
elapsed = end - start
print(f'Time taken: {elapsed:.6f} seconds')
