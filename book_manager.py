from mail_service import MailService
from book_scraper import BookScraper
import pandas as pd
import os
from icecream import ic
from pathlib import Path
import shutil

class BookManager:
    """
    A class that manages the collection and processing of books.

    Attributes:
        BOOK_DIRECTORY (str): The directory where the books are stored.
        from_email (str): The email address from which the books will be sent.
        to_email (str): The email address to which the books will be sent.
        mail_service (MailService): An instance of the MailService class for sending emails.
        scraper (BookScraper): An instance of the BookScraper class for scraping books.
        choice_to_function (dict): A dictionary mapping user choices to corresponding functions.
    """

    BOOK_DIRECTORY = 'Books/'

    def __init__(self, from_email, to_email):
        """
        Initializes a new instance of the BookManager class.

        Args:
            from_email (str): The email address from which the books will be sent.
            to_email (str): The email address to which the books will be sent.
        """
        self.from_email = from_email
        self.to_email = to_email
        self.mail_service = None
        self.scraper = None
        self.choice_to_function = {}

    def _get_book_data_from_csv(self):
        """
        Retrieves book data from a CSV file.

        Returns:
            A generator that yields tuples containing the book title and mirror URLs.
        """
        file_location = input('Enter the location of the CSV file: ')
        books_csv = pd.read_csv(file_location)
        for _, row in books_csv.iterrows():
            yield row['Title'], row[['Mirror_1', 'Mirror_2', 'Mirror_3']]

    def _get_book_data_manually(self):
        """
        Prompt the user to enter the name of the book and yield the book name.
        """

        book_name = input('Enter the name of the book: ')
        yield book_name

    def _get_book_data_with_link(self):
            """
            Prompt the user to enter the name and download link of a book.
            
            Returns:
                A generator that yields a tuple containing the book name and download link.
            """
            
            book_name = input('Enter the name of the book: ')
            download_link = input('Enter the download link of the book: ')
            yield book_name, download_link

    def _send_books_to_email(self):
            """
            Sends books to the specified email address as attachments.

            This method iterates over the files in the BOOK_DIRECTORY and sends each file as an attachment
            to the specified email address using the MailService class. The email includes a subject, 
            a body in HTML format, and the book file as an attachment.

            Args:
                self (BookManager): The BookManager instance.
            
            Returns:
                None
            """
            
            self.mail_service = MailService()
            for filename in os.listdir(self.BOOK_DIRECTORY):
                book_path = os.path.join(self.BOOK_DIRECTORY, filename)
                self.mail_service.send_email_with_attachment(
                    from_email=self.from_email,
                    to_email=self.to_email,
                    file_path=book_path,
                    file_name=filename,
                    subject='Sending books to Kindle',
                    html_content='<h1>Here is your book!</h1>',
                )

    def _clear_folder(self, folder_path):
            """
            Clears all the contents of a folder.

            Args:
                folder_path (str): The path to the folder.

            Returns:
                None
            """
            folder = Path(folder_path)
            for item in folder.iterdir():
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()


    def main(self):
        """
        Main method for the book manager.
        Allows the user to choose different options for getting book data and scraping books.
        """
        self.choice_to_function = {
            '1': self._get_book_data_from_csv,
            '2': self._get_book_data_manually,
            '3': self._get_book_data_with_link,
        }
        while True:
            choice = input('Enter 1 to read from a CSV file, 2 to enter the book name manually, or 3 to provide the book name and download link: ')
            get_book_data = self.choice_to_function.get(choice)

            if get_book_data is None:
                ic('Invalid choice. Please enter 1, 2, or 3.')
                return

            self.scraper = BookScraper()
            for book_data in get_book_data():
                if choice == '1':
                    book_name, download_links = book_data
                    self.scraper.scrape_book(book_name, download_links=download_links)
                elif choice == '2':
                    book_name = book_data
                    self.scraper.scrape_book(book_name)
                elif choice == '3':
                    book_name, download_link = book_data
                    self.scraper.scrape_book(book_name, download_link=download_link)
            user_input = input('Do you want to scrape another book? (y/n): ')
            if user_input.lower() != 'y':
                break
        
        send_books = input('Do you want to send the books to your email? (y/n): ')
        clear_books = input('Do you want to clear the books folder? (y/n): ')
        
        has_epub_files = any(file.suffix == '.epub' for file in Path(self.BOOK_DIRECTORY).iterdir())

        if has_epub_files:
            if send_books.lower() == 'y':
                self._send_books_to_email()
            if clear_books.lower() == 'y':
                self._clear_folder(self.BOOK_DIRECTORY)
        else:
            ic('No books to send or clear.')