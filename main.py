import requests
import os
import time
from book_parser import get_book_info
from pathvalidate import sanitize_filename

def download_txt(url, filename, folder='books/'):

    os.makedirs(folder, exist_ok=True)
    response = requests.get(url)
    if response.ok:
        file_path = os.path.join(folder, sanitize_filename(filename))
        with open(file_path, 'w') as file_data:
            file_data.write(response.text)
        return file_path


def main():

    for num in range(11):
        url = f"http://tululu.org/txt.php?id={num}"
        response = requests.get(url, allow_redirects=False)
        if response.status_code == 200:
            print(download_txt(url, get_book_info(num)))
            time.sleep(1)


if __name__ == "__main__":
    main()
