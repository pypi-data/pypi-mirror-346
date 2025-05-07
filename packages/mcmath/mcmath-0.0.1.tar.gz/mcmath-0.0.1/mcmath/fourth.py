from typing import Tuple

def max_colors_for_image(
    width: int,
    height: int,
    memory_kb: int,
    transparency_bits: int
) -> Tuple[int, int]:
    """
    Вычисляет максимально возможное количество цветовых оттенков (без учёта прозрачности)
    для растрового изображения заданного размера и объёма памяти.

    :param width:              ширина изображения в пикселях
    :param height:             высота изображения в пикселях
    :param memory_kb:          объём памяти под растровые данные в килобайтах
    :param transparency_bits:  число бит на хранение степени прозрачности каждого пикселя
    :return:                   кортеж (color_bits, max_colors), где
                                color_bits  — число бит на цвет,
                                max_colors  — максимально возможное число цветов
    """
    pixels = width * height
    total_bits = memory_kb * 1024 * 8
    bits_per_pixel = total_bits // pixels
    if bits_per_pixel <= transparency_bits:
        raise ValueError("Недостаточно бит для хранения цвета при заданных параметрах.")
    color_bits = bits_per_pixel - transparency_bits
    max_colors = 2 ** color_bits
    return color_bits, max_colors