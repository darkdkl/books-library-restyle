import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import time

def get_books_urls(genre_id="l55", start_page=1, end_page=2):

    genre_id += "/"
    host_url = "http://tululu.org/"
    url = host_url+genre_id

    for page in range(start_page, end_page+1):
        response_for_test = requests.get(urljoin(url, str(page)),
                                         allow_redirects=False)
        time.sleep(1)
        if response_for_test.status_code == 200:
            response = requests.get(urljoin(url, str(page)))
            soup = BeautifulSoup(response.text, 'lxml')
            books_content = soup.find('div', id="content").find_all('table',
                                                                class_="d_book")
            book_ids = [
                book.find_all('a')[1].get('href') for book in books_content
            ]
            return [(urljoin(host_url, book_id)) for book_id in book_ids]

        else:
            break


if __name__ == "__main__":
    print(get_books_urls())
