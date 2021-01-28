"""DESCRIPTION: This script is step 01 in the processing of IBGE geographical data. This script downloads the raw
shapefiles for all Brazilian political-administrative divisions between 1872 and 1991 from the IBGE FTP server.

Requirements:
setup_dirs.py has to be in the same folder as this script.
"""

import os
import setup_dirs
import urllib.request as request
from bs4 import BeautifulSoup
from tqdm import tqdm
import time


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

# Define raw data directory:
raw_data_dir = os.path.join(dir_dict['raw_data']['path'], 'IBGE')
if not os.path.exists(raw_data_dir):
    os.mkdir(raw_data_dir)

# Define top url:
top_url = "https://geoftp.ibge.gov.br/organizacao_do_territorio/estrutura_territorial" \
          "/evolucao_da_divisao_territorial_do_brasil/evolucao_da_divisao_territorial_do_brasil_1872_2010" \
          "/municipios_1872_1991/divisao_territorial_1872_1991/"

# Define top destination directory:
dir_destin_top = os.path.join(raw_data_dir, top_url.split('/')[-2])
if not os.path.exists(dir_destin_top):
    os.mkdir(dir_destin_top)

# Request top page:
top_page = request.urlopen(url=top_url)

# Soupify:
top_soup = BeautifulSoup(top_page, features="lxml")

# Create list of dictionary items with source url and destination path:
full_list = []
for link in top_soup.find_all('a'):
    try:
        year = int(link.get('href').replace('/', ''))
    except ValueError:
        print('Link is not a year')
        continue

    sub_url = top_url + link.get('href')
    sub_page = request.urlopen(url=sub_url)
    sub_soup = BeautifulSoup(sub_page, features="lxml")
    sub_dir = os.path.join(dir_destin_top, str(year))
    if not os.path.exists(sub_dir):
        os.mkdir(sub_dir)

    for sub_link in [subsub_link for subsub_link in sub_soup.find_all('a') if subsub_link.get('href').endswith('.zip')]:
        file_url = sub_url + sub_link.get('href')
        file_path = os.path.join(sub_dir, sub_link.get('href'))
        full_list.append({'source_url': file_url, 'destin_path': file_path})

# Create list of destination paths of existing files:
existing = []
for root, dirs, files in os.walk(dir_destin_top, topdown=True):
    for fname in [f for f in files if f.endswith('.zip')]:
        existing.append(os.path.join(root, fname))

# List of items to process (depends on overwriting preferences set at the start):
if overwrite_stuff:
    to_process = full_list
else:
    to_process = [item for item in full_list if item['destin_path'] not in existing]

# Download:
for item in to_process:
    # Unpack:
    source_url = item['source_url']
    destin_path = item['destin_path']

    download_url(url=source_url, output_path=destin_path)
    time.sleep(5)
