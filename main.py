import requests
import os
import time
from book_parser import get_book_info
from pathvalidate import sanitize_filename
from urllib.parse import urlparse

def get_norm_file_path(folder,filename):
    return os.path.join(folder, sanitize_filename(filename))

def download_txt(url, filename, folder='books/'):

    os.makedirs(folder, exist_ok=True)
    response = requests.get(url)
    if response.ok:
        file_path = get_norm_file_path(folder,filename)
        with open(file_path, 'w') as file_data:
            file_data.write(response.text)
        return file_path

def download_image(url, filename,folder='books/img'):
    os.makedirs(folder, exist_ok=True)
    response=requests.get(url)
    if response.ok:
        file_path = get_norm_file_path(folder,filename)
        with open (file_path,'wb') as img_file:
            img_file.write(response.content)


    

def main():

    for num in range(11):
        url = f"http://tululu.org/txt.php?id={num}"

        response = requests.get(url, allow_redirects=False)
        if response.status_code == 200:
            txt_name, img_url,book_image_name =  get_book_info(num)
            download_image(img_url,book_image_name)
            # print(download_txt(url, get_book_info(txt_name)))
            time.sleep(1)


if __name__ == "__main__":
    main()
