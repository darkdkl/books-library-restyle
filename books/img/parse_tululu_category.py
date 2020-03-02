import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from itertools import count
import time


def get_books_url(genre_id= "l55"):
   
    genre_id += "/"
    host_url="http://tululu.org/"
    url = host_url+genre_id
    for page in range(1,10):
    # for page in count(1):
        response_for_test = requests.get(urljoin(url,str(page)), 
                                                        allow_redirects=False)
        time.sleep(1)
        if response_for_test.status_code == 200:
            response = requests.get(urljoin(url,str(page)))
            soup = BeautifulSoup(response.text,'lxml')
            books_content = soup.find('div', id="content").find_all('table', 
                                                                class_="d_book")
            book_ids = [
                    book.find_all('a')[1].get('href') for book in books_content
                       ]
            for id in book_ids:
                print(urljoin(host_url,id))
        else:
            break


if __name__ == "__main__":
    get_books_url()
    

