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
    
    def get_article(self, word: str) -> Optional[str]:
        gd_gender = gd.get_gender(word)
        if gd_gender:
            return gender_articles[gd_gender]
        
        word = word.lower()
        if word in self.dictcc:
            return self.dictcc[word]
        else:
            ss_form = word.replace('ß', 'ss')
            if ss_form in self.dictcc:
                return self.dictcc[ss_form]
        return None

    def is_valid_word(self, word: str, pos: str) -> bool:
        if pos == 'NOUN':
            return bool(self.get_article(word))
        return True

class Word:
    def __init__(self, language: 'GermanLanguage', text: str, pos: str, freq: int) -> None:
        self.language = language
        self.text = text
        self.pos = pos
        self.freq = freq

    def to_sheet(self):
        return f'{self.display_form()}\t=GOOGLETRANSLATE("{self.translate_form()}", "de", "en")\t{self.freq}'

    def display_form(self) -> str:
        if self.pos == 'NOUN':
            return f'{self.language.get_article(self.text)} {self.text}'
        return self.text
    
    def translate_form(self) -> str:
        if self.pos == 'NOUN':
            return f'{self.language.get_article(self.text)} {self.text}'
        elif self.pos == 'VERB':
            return f'zu {self.text}'
        return self.text

    def __str__(self) -> str:
        return self.text