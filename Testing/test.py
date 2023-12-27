import os
from ..zlibrary import Zlibrary
from dotenv import load_dotenv
import pandas as pd
from icecream import ic
import os

# Load environment variables
def download_book(book_name):
    load_dotenv()
    # Create Zlibrary object and login
    Z = Zlibrary(
        email=os.getenv("ZLIBRARY_EMAIL"),
        password=os.getenv("ZLIBRARY_PASSWORD")
    )

    # Get most popular books
    results = Z.search(message=book_name, languages=["English"], extensions="epub")["books"]
    books = pd.DataFrame(results)

    epub_books = books[(books["extension"] == "epub") & (books["language"] == "English") & (books["title"].str.lower().str.contains(book_name.lower()))]

    epub_books = epub_books.sort_values("year", ascending=False)

    book_to_download = epub_books.iloc[0].to_dict()
    title = book_to_download["title"]

    filename, content = Z.downloadBook(book=book_to_download)
    ic(filename)

    with open(f"books/{title}", "wb") as f:
        f.write(content)


# download_book("Choose Your Enemies Wisely: Business Planning for the Audacious Few")
load_dotenv()
Z = Zlibrary(
        email=os.getenv("ZLIBRARY_EMAIL_TEST"),
        password=os.getenv("ZLIBRARY_PASSWORD")
    )

books = pd.DataFrame(Z.getUserDownloaded()["books"])
ic(books.columns)

