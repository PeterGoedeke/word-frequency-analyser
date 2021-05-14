from typing import Set, List, Tuple
from collections import Counter
from functools import reduce

class Library:
    def __init__(self, dictionary: Set[str]) -> None:
        self.dictionary = dictionary
        self.resources = [] # type: List['Counter']

    def add_resource(self, r: str) -> None:
        word_counts = Counter(word for word in r.split() if word in self.dictionary)
        self.resources.append(word_counts)

    def get_frequencies(self) -> Counter:
        return reduce(lambda a, c: a.update(c) or a, self.resources)

    def get_ubiquities(self) -> Counter:
        return reduce(lambda a, c: a.update(c.keys()) or a, [Counter()] + self.resources)
