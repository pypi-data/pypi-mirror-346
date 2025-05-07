def find_max_d_below(p, q, e, limit):
    """
    Находит наибольшее целое d < limit, удовлетворяющее условию:
        (d * e) % phi == 1,
    где phi = (p-1)*(q-1).

    :param p: простое число p
    :param q: простое число q
    :param e: открытая экспонента e
    :param limit: верхняя граница для d (исключительно)
    :return: наибольшее d < limit, такое что (d*e) mod phi = 1
    :raises ValueError: если такого d нет
    """
    phi = (p - 1) * (q - 1)

    def egcd(a, b):
        if b == 0:
            return (1, 0, a)
        x2, y2, g = egcd(b, a % b)
        x = y2
        y = x2 - (a // b) * y2
        return (x, y, g)

    x, y, g = egcd(e, phi)
    if g != 1:
        raise ValueError(f"e={e} не обратим модуль phi={phi}")
    d0 = x % phi

    import math
    k_max = math.floor((limit - 1 - d0) / phi)

    d_candidate = d0 + k_max * phi
    if d_candidate <= 0:
        raise ValueError(f"Нет решения d < {limit}")
    return d_candidate