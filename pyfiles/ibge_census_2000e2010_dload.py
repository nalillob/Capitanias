import os
import setup_dirs
import requests
import requests_cache
from bs4 import BeautifulSoup
import time
import urllib.request as request
from tqdm import tqdm


# Classes and functions:
class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def download_url(url, output_path):
    with DownloadProgressBar(unit='B', unit_scale=True, miniters=1, desc=url.split('/')[-1]) as t:
        request.urlretrieve(url, filename=output_path, reporthook=t.update_to)


# Preferences:
overwrite_stuff = False

# Load directories and create them if they don't exist:
dir_dict = setup_dirs.def_dirs()
setup_dirs.create_dirs(directory_dict=dir_dict, report=True)

# Set requests to keep in cache:
requests_cache.install_cache('demo_cache')

# Define urls
top_url = "https://www.ibge.gov.br/estatisticas/sociais/trabalho/9662-censo-demografico-2010.html?=&t=microdados"

base_url_2010 = "ftp://ftp.ibge.gov.br/Censos/Censo_Demografico_2010/Resultados_Gerais_da_Amostra/Microdados/"

base_url_2000 = "ftp://ftp.ibge.gov.br/Censos/Censo_Demografico_2000/Microdados/"

# Request page:
page = requests.get(url=top_url)

# Soupify:
soup = BeautifulSoup(page.content, features="lxml")

# Construct download lists:
download_list_2000 = [link.get('href') for link in soup.find_all('a') if str(link.get('href')).find(base_url_2000) == 0]
download_list_2010 = [link.get('href') for link in soup.find_all('a') if str(link.get('href')).find(base_url_2010) == 0]

# Define destination directories (and create them if they don't exist):
raw_data_dir = os.path.join(dir_dict['raw_data']['path'], 'IBGE')
if not os.path.exists(raw_data_dir):
    os.mkdir(raw_data_dir)

destin_dir_2000 = os.path.join(raw_data_dir, 'Censo_2000')
destin_dir_2010 = os.path.join(raw_data_dir, 'Censo_2010')

if not os.path.exists(destin_dir_2000):
    os.mkdir(destin_dir_2000)

if not os.path.exists(destin_dir_2010):
    os.mkdir(destin_dir_2010)

# Create list of existing files:
existing_2000 = [file for file in os.listdir(path=destin_dir_2000) if os.path.isfile(file) and file.endswith('.zip')]
existing_2010 = [file for file in os.listdir(path=destin_dir_2010) if os.path.isfile(file) and file.endswith('.zip')]

# List of items to download (depends on overwriting preferences set at the start):
if overwrite_stuff:
    to_process_2000 = download_list_2000
    to_process_2010 = download_list_2010
else:
    to_process_2000 = [url for url in download_list_2000 if
                       str(url.split(sep='/')[-1]).endswith('.zip') and url.split(sep='/')[-1] not in existing_2000]
    to_process_2010 = [url for url in download_list_2010 if
                       str(url.split(sep='/')[-1]).endswith('.zip') and url.split(sep='/')[-1] not in existing_2010]


# Download zips for year 2000:
for ftp_url in to_process_2000:
    fileout = os.path.join(destin_dir_2000, ftp_url.split('/')[-1])
    download_url(url=ftp_url, output_path=fileout)
    time.sleep(5)

# Download zips for year 2010:
for ftp_url in to_process_2010:
    fileout = os.path.join(destin_dir_2010, ftp_url.split('/')[-1])
    download_url(url=ftp_url, output_path=fileout)
    time.sleep(5)
