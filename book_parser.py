from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from urllib.parse import urlparse

def get_html(url):
    response = requests.get(url, allow_redirects=False)
    response.raise_for_status()
    return response.text

def parse_book_info(html):
    soup = BeautifulSoup(html, 'lxml')
    book_image_path = soup.select_one("#content .bookimage img").get('src')
    book_image_name = book_image_path.rsplit('/')[-1]
    book_title_author = soup.select_one("#content h1").text
    book_genres = [description.text for description
                   in soup.select("#content span.d_book a")]
    book_comments = [comments.text for comments
                     in soup.select("#content .texts .black")]
    book_name, author = book_title_author.replace('\xa0', "").split('::')
    book_text_path = [path.get("href") for path
                      in soup.select("#content table.d_book td a")][-3]
    book_info = (book_name.strip(), author.strip(), book_text_path,
                 book_image_path, book_image_name, book_genres,
                 book_comments)
    return book_info

def get_book_info(url):
    return parse_book_info(get_html(url))

if __name__ == "__main__":
    print(get_book_info('http://tululu.org/b550/'))
