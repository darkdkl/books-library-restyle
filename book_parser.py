from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin


def get_book_info(book_id):
    host_url = "http://tululu.org"
    response = requests.get(f'{host_url}/b{book_id}/', allow_redirects=False)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    book_content = soup.find('div', id="content")
    book_image_path = book_content.find(
                            'div', class_="bookimage").find('img').get('src')
    book_image_name = book_image_path.rsplit('/')[-1]
    book_info = book_content.find('h1').text
    book_name, author = book_info.replace('\xa0', "").split('::')
    book_title=f"{book_name.strip()} ({author.strip()}).txt"
    return book_title, urljoin(host_url,book_image_path),book_image_name


if __name__ == "__main__":
    print(get_book_info(9))
