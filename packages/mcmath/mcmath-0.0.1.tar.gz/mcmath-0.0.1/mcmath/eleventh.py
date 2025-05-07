from typing import List, Tuple

def find_unknown_digit_solution(
    terms: List[str],
    base: int,
    unknown_symbol: str,
    divisor: int
) -> Tuple[int, int]:
    """
    Универсальная функция для выражений с неизвестной цифрой в системе с основанием `base`.

    :param terms:           список строковых операндов (все соединяются оператором +)
    :param base:            основание системы счисления (напр., 12)
    :param unknown_symbol:  символ, обозначающий неизвестную цифру (напр., 'x')
    :param divisor:         число, на которое должно делиться значение выражения
    :return:                кортеж (значение неизвестной цифры, частное от деления суммы на divisor)
    :raises ValueError:     если не найдено подходящего значения неизвестной цифры
    """
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if base > len(digits):
        raise ValueError(f"Максимальное поддерживаемое основание {len(digits)}")

    for d in range(base):
        ch = digits[d]
        try:
            values = [int(term.replace(unknown_symbol, ch), base) for term in terms]
        except ValueError:
            continue
        total = sum(values)
        if total % divisor == 0:
            return d, total // divisor

    raise ValueError(f"Нет значения {unknown_symbol} < {base}, при котором выражение делится на {divisor}")