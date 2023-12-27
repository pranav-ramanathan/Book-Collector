from book_manager import BookManager
from dotenv import load_dotenv
import os

def main():

    load_dotenv()

    book_manager = BookManager(
        from_email=os.getenv('GMAIL'),
        to_email=os.getenv('KINDLE_EMAIL'),
    )

    book_manager.main()




if __name__ == '__main__':
    main()