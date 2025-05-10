def count_words(text):
    return len(text.split())

def count_chars(text, include_spaces=True):
    if not include_spaces:
        text = text.replace(" ", "")
    return len(text)