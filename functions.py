import re
from collections import defaultdict
from typing import DefaultDict, Dict, Optional

from genderdeterminator import GenderDeterminator
gd = GenderDeterminator()

gender_articles = defaultdict(lambda: '') # type: DefaultDict[str, str]
gender_articles.update({'n': 'das', 'm': 'der', 'f': 'die', 'pl': 'die'})

class GermanLanguage:
    def __init__(self) -> None:
        with open('dictionary', 'r') as f:
            dictionary_lines = f.read().splitlines()
            genders = {}
            for line in dictionary_lines:
                word_result = re.findall('^(.*)(?= {)', line)
                gender_result = re.findall('(?<={)\w+(?=})', line)
                if word_result and gender_result:
                    word = re.sub('\W', '', word_result[0].lower())
                    if word in genders:
                        continue
                    gender = gender_articles[gender_result[0]]
                    genders[word] = gender
        self.dictcc = genders
