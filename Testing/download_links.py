from libgen_api import LibgenSearch
import pandas as pd
from icecream import ic
from isbntools.app import isbn_from_words
from isbnlib import meta

# MIRROR_SOURCES = ["GET", "Cloudflare", "IPFS.io", "Infura"]

tf = LibgenSearch()
filters = {
    'Language': 'English',
    'Extension': 'epub',
}

results = tf.search_title_filtered('The art of war sun tzu', filters=filters)
books = pd.DataFrame(results)

# ic(books)

# mirror_list = ['Mirror_1', 'Mirror_2', 'Mirror_3']

books = books[["Title", "Mirror_1", "Mirror_2", "Mirror_3", "Extension"]]
ic(books.head())
isbn = isbn_from_words("The art of war")

ic(meta(isbn))