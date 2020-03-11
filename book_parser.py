from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from urllib.parse import urlparse


def get_book_info(book_url):

    parsed_url = urlparse(book_url)
    host_url = f'{parsed_url.scheme}://{parsed_url.netloc}/'
    response = requests.get(book_url, allow_redirects=False)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    book_content = soup.find('div', id="content")
    book_image_path = book_content.find(
        'div', class_="bookimage").find('img').get('src')
    book_image_name = book_image_path.rsplit('/')[-1]
    book_title_author = book_content.find('h1').text
    book_genres = [
        genre.text for genre in book_content.find('span',
                                                  class_="d_book").find_all('a')
    ]
    book_comments = [
        comment.find('span', class_="black").text
        for comment in book_content.find_all('div', class_="texts")
    ]
    book_name, author = book_title_author.replace('\xa0', "").split('::')
    book_info=(book_name.strip(), author.strip(), urljoin(host_url, 
                book_image_path), book_image_name, book_genres, book_comments)
    return book_info

if __name__ == "__main__":
    print(get_book_info('http://tululu.org/b550/'))
