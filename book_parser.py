from bs4 import BeautifulSoup
import requests


def get_book_info(book_id):
    response = requests.get(f'http://tululu.org/b{book_id}/',
                            allow_redirects=False)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    book_info = soup.find('div', id="content").find('h1').text
    book_name, author = book_info.replace('\xa0', "").split('::')
    return f"{book_name.strip()} ({author.strip()}).txt"


if __name__ == "__main__":
    print(get_book_info(1) )
