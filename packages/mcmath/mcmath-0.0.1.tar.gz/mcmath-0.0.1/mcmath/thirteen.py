from typing import Tuple, List


def analyze_sequence_pairs(
    numbers: List[int],
    k: int
) -> Tuple[int, int]:
    """
    Универсальная функция для задачи на анализ пар в последовательности целых чисел:
      1. Находит N = минимальное число в последовательности, НЕ кратное k.
      2. Определяет все подряд идущие пары (i,i+1), в которых оба элемента кратны N.
      3. Возвращает количество таких пар и максимальную сумму элементов среди этих пар.

    :param numbers: список целых чисел
    :param k:       параметр для поиска N: исключаем числа, кратные k
    :return:        кортеж (count_pairs, max_sum_of_pairs)
    :raises ValueError: если нет числа, не кратного k, или нет подходящих пар
    """
    non_multiples = [x for x in numbers if x % k != 0]
    if not non_multiples:
        raise ValueError(f"В последовательности нет элементов, не кратных {k}")
    N = min(non_multiples)

    count = 0
    max_sum = None
    for a, b in zip(numbers, numbers[1:]):
        if a % N == 0 and b % N == 0:
            pair_sum = a + b
            count += 1
            if max_sum is None or pair_sum > max_sum:
                max_sum = pair_sum

    if count == 0:
        raise ValueError(f"Нет подряд идущих пар, оба элемента которых кратны N={N}")

    return count, max_sum


def process_file(filepath: str, k: int) -> Tuple[int, int]:
    """
    Читает файл с одним целым числом в строке и применяет analyze_sequence_pairs.
    :param filepath: путь к текстовому файлу
    :param k:        параметр k для поиска N
    :return:         результат analyze_sequence_pairs
    """
    with open(filepath, 'r') as f:
        numbers = [int(line.strip()) for line in f if line.strip()]
    return analyze_sequence_pairs(numbers, k)