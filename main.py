import requests
import os
import time
from book_parser import get_book_info
from pathvalidate import sanitize_filename
from urllib.parse import urlparse
from parse_book_urls import get_books_urls
from progressbar import render_progressbar
import json



def get_norm_file_path(folder, filename):
    return os.path.join(folder, sanitize_filename(filename))


def download_txt(url, book_title, book_author, folder='books/'):
    filename = f"{book_title} ({book_author}).txt"
    os.makedirs(folder, exist_ok=True)
    response = requests.get(url)
    if response.ok:
        file_path = get_norm_file_path(folder, filename)
        with open(file_path, 'w') as file_data:
            file_data.write(response.text)
        return file_path


def download_image(url, filename, folder='img/'):
    os.makedirs(folder, exist_ok=True)
    response = requests.get(url)
    if response.ok:
        file_path = get_norm_file_path(folder, filename)
        with open(file_path, 'wb') as img_file:
            img_file.write(response.content)
        return file_path


def save_json(books_info):
    with open("books_info.json", "w", encoding='utf-8') as file:
        json.dump(books_info, file, ensure_ascii=False)


def main():
    books_info_summary = []
    start_page=1
    end_page=1
    books_urls = get_books_urls(start_page,end_page)
    count=len(books_urls)
    print()
    for url in books_urls:        
        response = requests.get(url, allow_redirects=False)
        if response.status_code == 200:
            title, author, img_url,img_name,genres,comments = get_book_info(url)
            img_src = download_image(img_url, img_name)
            book_path = download_txt(url, title, author)
            time.sleep(1)
            books_info_summary.append({
                "title": title,
                "author": author,
                "img_src": img_src,
                "book_path": book_path,
                "comments": comments,
                "genres": genres,
            })
            count-=1
            print('\u001b[1A',render_progressbar(count+1,1),
                        f'книга : {title}({author})                       ' )
            
    save_json(books_info_summary)

if __name__ == "__main__":
    main()
