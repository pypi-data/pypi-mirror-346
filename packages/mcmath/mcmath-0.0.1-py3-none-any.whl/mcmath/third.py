from typing import List, Tuple

def parse_base_number(s: str, base: int) -> float:
    """
    Преобразует строку‑число s в системе с основанием base (целая и дробная часть через '.' или ',')
    в десятичное значение (float).
    """
    s = s.replace(',', '.')
    if '.' in s:
        int_part, frac_part = s.split('.')
    else:
        int_part, frac_part = s, ''
    val_int = int(int_part, base) if int_part else 0
    val_frac = sum(int(d, base) * (base ** -(i+1)) for i, d in enumerate(frac_part))
    return val_int + val_frac

def format_in_base(x: float, base: int, frac_digits: int = 10) -> str:
    """
    Форматирует число x (десятичный float) в строку в системе с основанием base.
    Дробная часть ограничена frac_digits цифрами.
    """
    int_part = int(x)
    frac_part = x - int_part
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if int_part == 0:
        s_int = "0"
    else:
        s = ""
        n = int_part
        while n > 0:
            s = digits[n % base] + s
            n //= base
        s_int = s
    if frac_part == 0:
        return s_int
    s_frac = ""
    f = frac_part
    for _ in range(frac_digits):
        f *= base
        d = int(f)
        s_frac += digits[d]
        f -= d
        if f == 0:
            break
    return f"{s_int}.{s_frac}"

def sum_in_bases(
    terms: List[Tuple[str, int]],
    output_base: int,
    frac_digits: int = 10
) -> str:
    """
    terms: список кортежей (строка_числа, основание_системы_числения)
    output_base: основание системы, в которой нужно получить результат
    возвращает строку‑представление суммы в системе output_base
    """
    total = sum(parse_base_number(s, b) for s, b in terms)
    return format_in_base(total, output_base, frac_digits)
