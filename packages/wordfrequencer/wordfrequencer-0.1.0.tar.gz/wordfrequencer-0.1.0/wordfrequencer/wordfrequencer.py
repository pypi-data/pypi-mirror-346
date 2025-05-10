import re
from collections import Counter
from typing import Union, Dict

def _clean_text(text: str) -> str:
    return re.sub(r'[^a-zA-Z\s]', '', text).lower()

def _count_word_frequency(text: Union[str, bytes]) -> Dict[str, int]:
    if isinstance(text, bytes):
        text = text.decode('utf-8')
    cleaned = _clean_text(text)
    words = cleaned.split()
    return dict(Counter(words))

def _display_table(freq_dict: Dict[str, int], columns: int = 3):
    sorted_items = sorted(freq_dict.items(), key=lambda x: (-x[1], x[0]))

    max_word_len = max(len(word) for word in freq_dict)
    max_freq_len = max(len(str(freq)) for freq in freq_dict.values())

    word_col_width = max(max_word_len, 10) + 2
    freq_col_width = max(max_freq_len, 4) + 2

    header = ""
    for _ in range(columns):
        header += f"\033[1m{'Word':<{word_col_width}}{'Freq':<{freq_col_width}}\033[0m  "
    print(header.strip())

    print("-" * (columns * (word_col_width + freq_col_width + 2)))

    for i in range(0, len(sorted_items), columns):
        row = ""
        for word, freq in sorted_items[i:i+columns]:
            row += f"{word:<{word_col_width}}{freq:<{freq_col_width}}  "
        print(row.strip())

def wordfrequencer(input_data: Union[str, bytes], columns: int = 3) -> None:
    if isinstance(input_data, str) and input_data.endswith('.txt'):  
        with open(input_data, 'r', encoding='utf-8') as f:
            content = f.read()
        freq_dict = _count_word_frequency(content)
    else:  
        if isinstance(input_data, bytes):
            input_data = input_data.decode('utf-8')
        freq_dict = _count_word_frequency(input_data)
    
    _display_table(freq_dict, columns)