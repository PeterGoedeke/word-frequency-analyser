import re
from collections import defaultdict
from typing import DefaultDict, Dict, List, Optional, Tuple
from enum import Enum

from genderdeterminator import GenderDeterminator
gd = GenderDeterminator()
import enchant
english_dict = enchant.Dict('en_US')
german_dict = enchant.Dict('de_DE')

gender_articles = defaultdict(lambda: '') # type: DefaultDict[str, str]
gender_articles.update({'n': 'das', 'm': 'der', 'f': 'die', 'pl': 'die'})

def simplify_pos(pos: str) -> str:
    return pos if pos == 'NOUN' or pos == 'VERB' else 'OTHER'

def fix_text_casing(text: str, pos: str) -> str:
    return text if pos == 'NOUN' else text.lower()

def token_to_word_tuple(token) -> Tuple[str, str]:
    pos = simplify_pos(token.pos_)
    text = fix_text_casing(token.lemma_, token.pos_)
    return (text, pos)

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
        return german_dict.check(word)

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

class WarningLevel(Enum):
    CLEAR = 0
    FAILURE = 1
    SPELLING = 2

articles = { 'der ', 'die ', 'das ' }
class Translation:
    def __init__(self, source: str, dest: str, freq: int, pos: str) -> None:
        self.source = source
        self.dest = dest
        self.freq = freq
        self.pos = pos
    
    @staticmethod
    def from_sheet(line: str) -> 'Translation':
        source, dest, freq, pos = line.split('\t')
        return Translation(source, dest, int(freq), pos)

    def get_root_source(self) -> str:
        if self.source.lower().startswith('zu '):
            return self.source[3:]
        elif self.source.lower()[:4] in articles:
            return self.source[4:]
        return self.source.lower()

    def get_root_dest(self) -> str:
        if self.dest.lower().startswith('to '):
            return self.dest[3:]
        elif self.dest.lower().startswith('the '):
            return self.dest[4:]
        return self.dest.lower()

    # change the dictionary here to enchant
    def get_warning_category(self) -> 'WarningLevel':
        if self.get_root_dest() == self.get_root_source():
            return WarningLevel.FAILURE
        if not english_dict.check(self.get_root_dest()):
            return WarningLevel.SPELLING
        return WarningLevel.CLEAR

def partition_warnings(ts: List['Translation']) -> Dict['WarningLevel', List['Translation']]:
    output = defaultdict(lambda: [])
    for t in ts:
        output[t.get_warning_category()].append(t)
    return output