from typing import Set, List, Tuple
from collections import Counter


class Corpus:
    def __init__(self, body: str, dictionary: Set[str]) -> None:
        self.counts = Counter(word for word in body.split() if word in dictionary)
        # self.counts = Counter({ k: v for k, v in self.counts.items() if v > 1})
        self.dictionary = dictionary

    def update(self, c: 'Corpus') -> None:
        self.counts.update(c.counts)
    
    def get_frequency_percentiles(self) -> List[Tuple[str, float]]:
        l = len(self.counts)
        return [(c[0], 1 - i / l) for i, c in enumerate(self.counts.most_common(100))]

    @staticmethod
    def get_ubiquity_percentiles(cs: List['Corpus']) -> List[Tuple[str, float]]:
        counter = Counter() # type: 'Counter'
        for c in cs:
            counter.update(c.counts.keys())
        l = len(counter)
        
        print(l)
        print(counter.most_common(100))
        print(l)

        return [(c[0], 1 - i / l) for i, c in enumerate(counter.most_common(100))]