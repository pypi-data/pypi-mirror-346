import argparse
from .counter import count_words, count_chars

def main():
    parser = argparse.ArgumentParser(description="Считает слова и символы в тексте.")
    parser.add_argument("text", help="Текст для анализа")
    parser.add_argument("--no-spaces", action="store_true", help="Игнорировать пробелы")
    
    args = parser.parse_args()
    
    print(f"Слов: {count_words(args.text)}")
    print(f"Символов: {count_chars(args.text, not args.no_spaces)}")

if __name__ == "__main__":
    main()