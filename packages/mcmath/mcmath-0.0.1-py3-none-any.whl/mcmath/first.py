from collections import Counter, deque, namedtuple
from typing import List, Dict, Tuple


class PrefixTreeNode:
    __slots__ = ('left', 'right', 'is_leaf')

    def __init__(self):
        self.left = None
        self.right = None
        self.is_leaf = False


def fano_encode_length(
    alphabet: List[str],
    known_codes: Dict[str, str],
    word: str
) -> Tuple[int, Dict[str, str]]:
    """
    Возвращает (total_bits, codes), где
      total_bits — минимальное число бит для кодирования word,
      codes      — полный префиксный код.
    """
    for a, ca in known_codes.items():
        for b, cb in known_codes.items():
            if a != b and (ca.startswith(cb) or cb.startswith(ca)):
                raise ValueError(f"Конфликт префиксных кодов: '{a}->{ca}' и '{b}->{cb}'")

    root = PrefixTreeNode()
    for sym, code in known_codes.items():
        node = root
        for bit in code:
            if bit == '0':
                if node.left is None:
                    node.left = PrefixTreeNode()
                node = node.left
            else:
                if node.right is None:
                    node.right = PrefixTreeNode()
                node = node.right
        node.is_leaf = True

    FreeCode = namedtuple('FreeCode', ['code', 'length'])
    free: List[FreeCode] = []
    q = deque([(root, "")])
    while q:
        node, path = q.popleft()
        if node.is_leaf:
            continue

        if node.left is None and node.right is None:
            free.append(FreeCode(path, len(path)))
            continue

        if node.left is None:
            free.append(FreeCode(path + '0', len(path) + 1))
        else:
            q.append((node.left, path + '0'))

        if node.right is None:
            free.append(FreeCode(path + '1', len(path) + 1))
        else:
            q.append((node.right, path + '1'))

    free.sort(key=lambda fc: (fc.length, fc.code))

    unknown_syms = [s for s in alphabet if s not in known_codes]
    freq = Counter(word)
    unknown_syms.sort(key=lambda s: (-freq[s], s))

    codes = dict(known_codes)
    for sym, fc in zip(unknown_syms, free):
        codes[sym] = fc.code

    total_bits = sum(freq[s] * len(codes[s]) for s in freq)
    return total_bits, codes
