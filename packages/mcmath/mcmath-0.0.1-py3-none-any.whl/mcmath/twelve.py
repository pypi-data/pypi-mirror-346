def to_twos_complement(n: int, bits: int) -> str:
    """
    Возвращает двоичную строку длины bits, представляющую целое n в дополнительном коде (two's complement).

    :param n:    целое число (может быть отрицательным или положительным)
    :param bits: число бит в представлении (например, 8 для 8‑битного)
    :return:     строка из '0' и '1' длины bits
    :raises ValueError: если n не влазит в заданное количество бит
    """
    min_val = - (1 << (bits - 1))
    max_val = (1 << (bits - 1)) - 1
    if not (min_val <= n <= max_val):
        raise ValueError(f"Число {n} не помещается в {bits}-битном дополнительном коде")

    mask = (1 << bits) - 1
    tc = n & mask
    return format(tc, f'0{bits}b')