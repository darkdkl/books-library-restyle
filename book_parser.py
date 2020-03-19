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
    book_image_path=soup.select_one("#content .bookimage img").get('src')    
    book_image_name = book_image_path.rsplit('/')[-1]
    book_title_author = soup.select_one("#content h1").text   
    book_genres = [description.text for description
                                     in soup.select("#content span.d_book a")]  
    book_comments = [comments.text for comments 
                                     in soup.select("#content .texts .black")]   
    book_name, author = book_title_author.replace('\xa0', "").split('::')
    book_info=(book_name.strip(), author.strip(), urljoin(host_url, 
                book_image_path), book_image_name, book_genres, book_comments)
    return book_info

if __name__ == "__main__":
    print(get_book_info('http://tululu.org/b550/'))
