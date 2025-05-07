from itertools import product
from typing import Callable, Iterable, Tuple

def find_first_word_index(
    alphabet: Iterable[str],
    length: int,
    predicate: Callable[[str], bool],
    start_index: int = 1
) -> Tuple[int, str]:
    """
    Перебирает в лексикографическом порядке все слова заданной длины над данным алфавитом,
    нумеруя их от start_index, и возвращает кортеж (index, word) для первого слова,
    на котором predicate(word) == True.

    :param alphabet:     последовательность символов в лексикографическом порядке
    :param length:       длина слов
    :param predicate:    функция [word: str] -> bool, задающая условие
    :param start_index:  с какого номера начинать нумерацию (по умолчанию 1)
    :return:             (номер слова в списке, само слово)
    """
    for idx, letters in enumerate(product(alphabet, repeat=length), start_index):
        word = ''.join(letters)
        if predicate(word):
            return idx, word
    raise ValueError("Нет ни одного слова, удовлетворяющего условию.")