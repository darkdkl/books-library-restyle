import requests
import os
import time
import argparse
import json
from book_parser import get_book_info
from pathvalidate import sanitize_filename
from urllib.parse import urlparse
from parse_book_urls import get_books_urls
from progressbar import render_progressbar


def get_norm_file_path(folder, filename):
    return os.path.join(folder, sanitize_filename(filename))

def download_txt(url, book_title, book_author, file_path):
    filename = f"{book_title} ({book_author}).txt"
    os.makedirs(file_path, exist_ok=True)
    response = requests.get(url)
    if response.ok:        
        with open(get_norm_file_path(file_path, filename), 'w') as file_data:
            file_data.write(response.text)
        return file_path

def download_image(url, filename, file_path):
    os.makedirs(file_path, exist_ok=True)
    response = requests.get(url)
    if response.ok:        
        with open(get_norm_file_path(file_path, filename), 'wb') as img_file:
            img_file.write(response.content)
        return file_path

def save_json(books_info,json_path):
    os.makedirs(json_path, exist_ok=True)
    with open(get_norm_file_path(json_path,"/books_info.json"),
                                                 "w", encoding='utf-8') as file:
        json.dump(books_info, file, ensure_ascii=False)

def main(start_page,end_page,folder,json_path,skip_imgs,skip_txt,show_url):
    os.makedirs(folder, exist_ok=True)
    books_info_summary = []  
    books_urls = get_books_urls(start_page,end_page)
    count=len(books_urls)
    if not show_url:print()
    for url in books_urls:        
        response = requests.get(url, allow_redirects=False)
        if response.status_code == 200:
            title, author,text_url,img_url,img_name,genres,comments = get_book_info(url)
            book_folder_name=f"/{title}({author})/"
            file_path=folder+book_folder_name
            img_src = book_path = None
            if not skip_imgs:
                img_src = download_image(img_url, img_name,file_path)
            if not skip_txt:
                book_path = download_txt(text_url, title, author,file_path)
            # time.sleep(0.5)
            books_info_summary.append({
                "title": title,
                "author": author,
                "img_src": img_src,
                "book_path": book_path,
                "comments": comments,
                "genres": genres,
            })
            count-=1            
            if show_url:
                print(url)
            else:
                
                print('\u001b[1A',render_progressbar(count+1,1),
                        f'книга : {title}({author})                          ')

    save_json(books_info_summary,json_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--start_page',default=1,
                            help='Начальная страница каталога книг',type=int)
    parser.add_argument('--end_page', 
                            help='Последняя страница каталога книг',type=int)
    parser.add_argument('--dest_folder', default ='books',
                            help='Каталог для данных')
    parser.add_argument('--json_path', default ='books',
                            help='Каталог для JSON данных')
    parser.add_argument('--skip_imgs', action='store_true',
                            help='Не загружать изображения')
    parser.add_argument('--skip_txt', action='store_true',
                            help='Не загружать текст')
    parser.add_argument('--show_url', action='store_true',
                            help='Отображать только url книги')
    args = parser.parse_args()  
    try:        
        main(args.start_page,args.end_page,args.dest_folder,args.json_path,
                                    args.skip_imgs,args.skip_txt,args.show_url)
    except KeyboardInterrupt:
        print("программа прервана")
    
    