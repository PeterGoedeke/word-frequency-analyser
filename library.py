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
        freqs = reduce(lambda a, c: a.update(c) or a, self.resources)
        # self.combine_cases(freqs)
        return freqs

    def get_ubiquities(self) -> Counter:
        ubiqs = reduce(lambda a, c: a.update(c.keys()) or a, [Counter()] + self.resources) # type: Counter
        # self.combine_cases(ubiqs)
        return ubiqs

    def get_frequency_weightings(self) -> Dict[str, float]:
        freqs = self.get_frequencies()
        return { c[0]: 1 - i / len(freqs) for i, c in enumerate(freqs.most_common())}

    def get_ubiquity_weightings(self) -> Dict[str, float]:
        ubiqs = self.get_ubiquities()
        num_buckets = ubiqs.most_common(1)[0][1]
        buckets = [[] for _ in range(num_buckets)] # type: List[List[str]]
        for key in ubiqs:
            val = ubiqs[key]
            buckets[num_buckets - (val - 1) - 1].append(key)

        return dict(reduce(lambda a, c: a + c,
            [[(e, 1 - i / len(buckets)) for e in l] for i, l in enumerate(buckets)]
        ))

    def get_weightings(self) -> Dict[str, float]:
        freq_weightings = self.get_frequency_weightings()
        ubiq_weightings = self.get_ubiquity_weightings()

        # print(freq_weightings['sie'])
        # print(ubiq_weightings['sie'])

        return { key: (freq_weightings[key] + ubiq_weightings[key]) / 2 for key in freq_weightings }