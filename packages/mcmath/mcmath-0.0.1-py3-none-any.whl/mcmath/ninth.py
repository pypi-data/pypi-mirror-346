import math

def max_count_identifiers(
    id_length: int,
    digit_count: int,
    special_count: int,
    total_storage_bytes: int
) -> int:
    """
    Вычисляет максимальное количество идентификаторов, которое можно хранить,
    если каждый идентификатор состоит из id_length символов,
    допускаются digit_count десятичных цифр и special_count специальных символов,
    все символы кодируются одинаковым минимальным количеством бит,
    и суммарно доступно total_storage_bytes байт.

    :param id_length: число символов в одном идентификаторе
    :param digit_count: количество десятичных цифр (0–9) в алфавите
    :param special_count: количество специальных символов в алфавите
    :param total_storage_bytes: общий объём памяти в байтах
    :return: максимальное число идентификаторов (пользователей)
    """
    alphabet_size = digit_count + special_count
    bits_per_symbol = math.ceil(math.log2(alphabet_size))

    bits_per_id = bits_per_symbol * id_length
    bytes_per_id = math.ceil(bits_per_id / 8)

    return total_storage_bytes // bytes_per_id