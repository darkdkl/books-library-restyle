import requests
import os
import time
import argparse
import json
from book_parser import get_book_info
from pathvalidate import sanitize_filename
from urllib.parse import urlparse,urljoin
from parse_book_urls import get_books_urls
from tqdm import tqdm

def download_txt(url, book_title, book_author, folder_path):
    filename = f"{book_title}_({book_author}).txt"
    os.makedirs(folder_path, exist_ok=True)
    response = requests.get(url)
    book_text_file = os.path.join(folder_path, sanitize_filename(filename))
    if response.ok:        
        with open(book_text_file, 'w') as file_data:
            file_data.write(response.text)
    return book_text_file

def download_image(url, filename, folder_path):
    os.makedirs(folder_path, exist_ok=True)
    response = requests.get(url)
    book_image_file = os.path.join(folder_path, sanitize_filename(filename))
    if response.ok:        
        with open(book_image_file, 'wb') as img_file:
            img_file.write(response.content)
    return book_image_file

def save_json(books_info,json_path):
    os.makedirs(json_path, exist_ok=True)
    json_file = os.path.join(json_path,"books_info.json")
    with open(json_file,"w", encoding='utf-8') as file:
        json.dump(books_info, file, ensure_ascii=False)

def main():
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
        os.makedirs(args.dest_folder, exist_ok=True)
        books_info_summary = []  
        books_urls = get_books_urls(args.start_page,args.end_page)        
        pbar_and_urls= tqdm(books_urls)
        for url in pbar_and_urls:                 
            response = requests.get(url, allow_redirects=False)
            if response.status_code == 200:
                title, author,text_path,img_path,img_name,genres,comments = get_book_info(url)
                text_url = urljoin(url,text_path)
                img_url = urljoin(url,img_path)
                book_folder_name=f"{title}({author})"
                folder_path=os.path.join(args.dest_folder,book_folder_name)                
                img_src = book_path = None
                if not args.skip_imgs:
                    img_src = download_image(img_url, img_name,folder_path)
                if not args.skip_txt:
                    book_path = download_txt(text_url, title, author,folder_path)
                # time.sleep(0.5)
                books_info_summary.append({
                    "title": title,
                    "author": author,
                    "img_src": img_src,
                    "book_path": book_path,
                    "comments": comments,
                    "genres": genres,
                })                          
                if args.show_url:
                    pbar_and_urls.set_description(f'  {url} ')
            
        save_json(books_info_summary,args.json_path)

    except KeyboardInterrupt:
        print("программа прервана")

if __name__ == "__main__":
    main()   
    
    