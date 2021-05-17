import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

def epub2thtml(epub_path):
    book = epub.read_epub(epub_path)
    chapters = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            chapters.append(item.get_content())
    return chapters

blacklist = [
	'[document]',
	'noscript',
	'header',
	'html',
	'meta',
	'head', 
	'input',
	'script',
	# there may be more elements you don't want, such as "style", etc.
]

def chap2text(chap):
    output = ''
    soup = BeautifulSoup(chap, 'html.parser')
    text = soup.find_all(text=True)
    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)
    return output

def thtml2ttext(thtml):
    Output = []
    for html in thtml:
        text =  chap2text(html)
        Output.append(text)
    return Output

def epub2text(epub_path):
    chapters = epub2thtml(epub_path)
    ttext = thtml2ttext(chapters)
    return ttext

import os

# out = '\n'.join('\n'.join(epub2text(f'/home/peter/Music/6000.German.e-book.Collection.epub/{book}')) for book in os.listdir('/home/peter/Music/6000.German.e-book.Collection.epub')[:50])

books = os.listdir('/home/peter/Music/6000.German.e-book.Collection.epub')[:5]

from library import Library
from typing import List

resource_dir = '/home/peter/Music/6000.German.e-book.Collection.epub'
f = open('de.txt', 'r')
de = set(f.read().split('\n'))

library = Library(de)
l2 = Library(de)

for i, book in enumerate(books):
    try:
        # print(book)
        resource_fragments = epub2text(f'{resource_dir}/{book}')
        resource = '\n'.join(resource_fragments)
        library.add_resource(resource)
        if i == 0:
            l2.add_resource(resource)
            print(resource)
            exit
        if i == 3:
            with open('./yeet.txt', 'w') as f:
                f.write(resource)
            pass
    except KeyError:
        pass

# print(library.get_frequencies().most_common(25))
# print(library.get_ubiquities().most_common(25))

# print(l2.get_frequencies().most_common(25))
# print(l2.get_ubiquities().most_common(25))

# print(library.check_word('drei'))
# print(library.check_word('dann'))
# print(library.check_word('mich'))

l = library.get_weightings()


out = '\n'.join(f'{k}: {round(v, 4)}' for k,v in sorted(list(l.items()), key=lambda t: t[1], reverse=True))
with open('./out.txt', 'w') as file:
    file.write(out)

# tests = [] # type: List['Corpus']
# for book in books:
#     try:
#         tests.append(Corpus('\n'.join(epub2text(f'/home/peter/Music/6000.German.e-book.Collection.epub/{book}')), de))
#         print(book)
#     except KeyError:
#         print('yote')

# c = Corpus(out, de)
# print(c.get_frequency_percentiles())
# print(Corpus.get_ubiquity_percentiles(tests))

# words = out.split()
# filtered_words = [word for word in words if word in de]
# # print(filtered_words)

# word_counter = Counter(filtered_words)

# print('\n'.join([f'{x}: {y}' for x,y in word_counter.most_common(1000)]))
# print(len(word_counter.keys()))


# print(sum([y for x,y in word_counter.most_common(1000)]) / sum([y for x,y in word_counter.most_common()]))