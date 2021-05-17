import os
import spacy
import epub
from typing import List, Dict, DefaultDict
from collections import Counter
from genderdeterminator import GenderDeterminator, Case
gd = GenderDeterminator()
import re
from collections import defaultdict

with open('de.txt', 'r') as f:
    de = set(f.read().split('\n'))

class Word:
    def __init__(self, text, pos) -> None:
        self.text = text
        self.pos = pos
        self.freq = 1
    
    def increment(self) -> None:
        self.freq += 1

def to_spreadsheet(token) -> Dict:
    return {
        'text': token.lemma_,
        'translation': f'=GOOGLETRANSLATE("{token.lemma_}" ,"de", "en")',
    }

en_nlp = spacy.load('en_core_web_sm')
de_nlp = spacy.load('de_core_news_sm')

genders = defaultdict(lambda: '') # type: DefaultDict[str, str]
genders.update({'n': 'das', 'm': 'der', 'f': 'die', 'pl': 'die'})

def wrapper(s: str, line: str) -> str:
    if s not in genders:
        print(line, s)
    return genders[s]

with open('dictionary', 'r') as f:
    de_genders = { 
        re.sub('\W', '', re.findall('^(.*)(?= {)', line)[0].lower()):
        wrapper(re.findall('(?<={)\w+(?=})', line)[0], line)
        for line in f.read().splitlines() if re.findall('(?<={)\w+(?=})', line) and re.findall('^(.*)(?= {)', line)}
    
    print(de_genders['Lieben'])
    # print(de_genders)
    # exit()
# en_nlp.max_length = 4000000

resource_dir = '/home/peter/Music/6000.German.e-book.Collection.epub'
books = os.listdir(resource_dir)[5:6]

# with open('in.txt', 'r') as f:
#     maybe = f.read()

resources = [] # type: List[str]
for i, book in enumerate(books):
    try:
        resource_fragments = epub.epub2text(f'{resource_dir}/{book}')
        resource = '\n'.join(resource_fragments)
        # print(resource)
        resources.append(resource)
    except KeyError:
        pass

def simplify_pos(pos: str) -> str:
    return pos
    # return pos if pos == 'NOUN' or pos == 'VERB' else 'OTHER'

de_doc = de_nlp('\n'.join(resources))
counts = Counter((token.lemma_, simplify_pos(token.pos_)) for token in de_doc if token.is_alpha and not token.is_stop and token.pos_ == 'NOUN')

failures = []
def prepend_de(word: str, pos: str, for_translation=False) -> str:
    if pos == 'NOUN':
        if gd.get_gender(word):
            return 'gd: ' + gd.get(word, Case.NOMINATIVE)

        if word.lower() in de_genders:
            return de_genders[word.lower()] + ' ' + word
        elif word.replace('ß', 'ss').lower() in de_genders:
            return de_genders[word.replace('ß', 'ss').lower()] + ' ' + word
        else:
            failures.append(word)
            return word
        
    elif pos == 'VERB' and for_translation:
        return 'zu ' + word
    return word

with open('deout.txt', 'w') as f:
    f.write(
        '\n'.join(f'{prepend_de(word[0], word[1])}\t=GOOGLETRANSLATE("{prepend_de(word[0], word[1], for_translation=True)}", "de", "en")\t{freq}\t{word[1]}' for word, freq in counts.most_common())
    )

exit()
# doc = en_nlp('\n'.join(resources))
doc = en_nlp(maybe)
# [to_spreadsheet(token) for token in doc if token.is_alpha]

def prepend(word: str, pos: str) -> str:
    prefix = '' if pos == 'OTHER' else ('the ' if pos == 'NOUN' else 'to ')
    return prefix + word

counts = Counter((token.lemma_, simplify_pos(token.pos_)) for token in doc if token.is_alpha and not token.is_stop)

with open('out.txt', 'w') as f:
    f.write(
        '\n'.join(f'{prepend(word[0], word[1])}\t=GOOGLETRANSLATE("{prepend(word[0], word[1])}", "en", "de")\t{freq}' for word, freq in counts.most_common())
    )


