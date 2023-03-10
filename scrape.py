import requests
from bs4 import BeautifulSoup
from rotate_ip import get_ip, get_random_proxy
import PyPDF2
from urllib.parse import urljoin
from urllib.parse import urlparse
import docx2txt
import time
import os

proxy_list = get_ip("https://free-proxy-list.net/")

def get_pdf(response, filename):
    print(f'Downloading {filename}...')
    with open(os.path.join(directory, filename+'.pdf'), 'wb') as f:
        f.write(response.content)
    # Open the downloaded file in binary mode and extract its text
    with open(os.path.join(directory, filename+'.pdf'), 'rb') as f:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfFileReader(f)
        # Extract the text from each page of the PDF file
        with open(os.path.join(directory, filename+'.txt'), 'w') as text_file:
            for page_num in range(pdf_reader.numPages):
                page = pdf_reader.getPage(page_num)
                text = page.extractText()
                text_file.write(text)

def get_doc(response, filename):
    print(f'Downloading {filename}...')
    with open(os.path.join(directory, filename + '.doc'), 'wb') as f:
        f.write(response.content)

    text = docx2txt.process(filename + '.doc')

    with open(os.path.join(directory, filename + '.txt'), 'w') as f:
        f.write(text)

# Function to download a file
def download_file(url, proxy):
    response = requests.get(url, proxies=proxy)
    file_name = url.split('/')[-2] + url.split('/')[-1]

    if response.status_code == 200:
        # Get the file name from the URL
        content_type = response.headers.get('Content-Type')
        if 'pdf' in content_type:
            print(f'Downloading PDF from {url}')
            get_pdf(response, file_name)
            time.sleep(0.5)
        elif 'msword' in content_type:
            print(f'Downloading DOC from {url}')
            get_doc(response, file_name)
            time.sleep(0.5)
        # Save the file to disk
    else:
        print(f"Error downloading {url}: status code {response.status_code}")

seen = set()
def scrape(url, proxy):
    print(url)
    seen.add(url)
    response = requests.get(url, proxies=proxy)
    type = response.headers.get('Content-Type')

    if 'pdf' in type or 'msword' in type:
        print('here')
        try:
            download_file(url, get_random_proxy(proxy_list))
        except Exception as e:
            print('Cannot download this file', e)
        return
    else:
        soup = BeautifulSoup(response.content, 'html.parser')
        all_links = soup.find_all('a')
        if not all_links: return

        for link in all_links:
            href = link.get('href')
            if href in seen:
                continue
            else:
                link_base_url = urlparse(href).netloc
                url_base_url = urlparse(url).netloc
                if link_base_url != '' and link_base_url == url_base_url:
                    cur_url = urljoin(url_base_url, link.get('href'))
                    scrape(cur_url, get_random_proxy(proxy_list))

url = 'https://mining.ca/resources/reports/facts-figures-2021/'

if __name__ == "__main__":
    # create folder for current website
    directory = url.split('/')[2]
    if not os.path.exists(directory):
        os.makedirs(directory)

    scrape(url, get_random_proxy(proxy_list))


    