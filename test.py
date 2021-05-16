import os
import spacy
import epub
from typing import List, Dict
from collections import Counter

en_nlp = spacy.load('en_core_web_sm')
de_nlp = spacy.load('de_core_news_sm')
# en_nlp.max_length = 4000000

resource_dir = '/home/peter/Music/6000.German.e-book.Collection.epub'
# books = os.listdir(resource_dir)[:1]

# with open('de.txt', 'r') as f:
#     de = set(f.read().split('\n'))

with open('in.txt', 'r') as f:
    maybe = f.read()

# resources = [] # type: List[str]
# for i, book in enumerate(books):
#     try:
#         resource_fragments = epub.epub2text(f'{resource_dir}/{book}')
#         resource = '\n'.join(resource_fragments)
#         print(resource)
#         resources.append(resource)
#     except KeyError:
#         pass

# doc = en_nlp('\n'.join(resources))
doc = en_nlp(maybe)
# [to_spreadsheet(token) for token in doc if token.is_alpha]

def simplify_pos(pos: str) -> str:
    return pos if pos == 'NOUN' or pos == 'VERB' else 'OTHER'

def prepend(word: str, pos: str) -> str:
    prefix = '' if pos == 'OTHER' else ('the ' if pos == 'NOUN' else 'to ')
    return prefix + word

counts = Counter((token.lemma_, simplify_pos(token.pos_)) for token in doc if token.is_alpha and not token.is_stop)

with open('out.txt', 'w') as f:
    f.write(
        '\n'.join(f'{prepend(word[0], word[1])}\t=GOOGLETRANSLATE("{prepend(word[0], word[1])}", "en", "de")\t{freq}' for word, freq in counts.most_common())
    )
