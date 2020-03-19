import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from itertools import count
import time

def get_books_urls(start_page=1, end_page=3,genre_id="l55"):
    genre_id += "/"
    host_url = "http://tululu.org/"
    url = host_url+genre_id
    books_urls = []
    iterator= range(start_page, end_page+1) if end_page else count(start_page)
    for page in iterator:
        response_for_test = requests.get(urljoin(url, str(page)),
                                         allow_redirects=False)
        time.sleep(1)
        if response_for_test.status_code == 200:
            response = requests.get(urljoin(url, str(page)))
            soup = BeautifulSoup(response.text, 'lxml')                        
            book_ids  = [book.get("href") for book in soup.select(
                                        "#content table.d_book .bookimage a")]
            books_urls+= [(urljoin(host_url, book_id)) for book_id in book_ids]            
        else:
            break
    return books_urls

if __name__ == "__main__":
    print(get_books_urls())
