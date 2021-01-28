"""DESCRIPTION: This script is step 02 in the processing of IBGE geographical data. This script downloads the raw
shapefiles for all Brazilian political-administrative divisions for 2000 and 2010 from the IBGE FTP server.

Requirements:
setup_dirs.py has to be in the same folder as this script.
"""

import ftptool
import os
import setup_dirs
import urllib.request as request
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

# Define top destination directory:
dir_destin_top = os.path.join(raw_data_dir, 'malhas_municipais')
if not os.path.exists(dir_destin_top):
    os.mkdir(dir_destin_top)

# FTP settings:
ibgeftp = "geoftp.ibge.gov.br"

top_ftp_2000 = "/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2000"
top_ftp_2010 = "/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2010"

# Connect to ftp:
connection = ftptool.FTPHost.connect(host=ibgeftp)
connection.ftp_obj.login()

# List of files (2000):
list_2000 = []
for (dirname, subdirs, files) in connection.walk(top_ftp_2000):
    for file in files:
        file_url = "http://" + ibgeftp + '/'.join([dirname, file])
        destin_path = os.path.join(dir_destin_top, dirname.replace("/organizacao_do_territorio/malhas_territoriais"
                                                                   "/malhas_municipais/", '').replace('/', '\\'))
        destin_path = os.path.join(destin_path, file)
        list_2000.append({'source_url': file_url, 'destin_path': destin_path})

# List of files (2010):
list_2010 = []
for (dirname, subdirs, files) in connection.walk(top_ftp_2010):
    for file in files:
        file_url = "http://" + ibgeftp + '/'.join([dirname, file])
        destin_path = os.path.join(dir_destin_top, dirname.replace("/organizacao_do_territorio/malhas_territoriais"
                                                                   "/malhas_municipais/", '').replace('/', '\\'))
        destin_path = os.path.join(destin_path, file)
        list_2010.append({'source_url': file_url, 'destin_path': destin_path})

# Create list of destination paths of existing files:
existing = []
for root, dirs, files in os.walk(dir_destin_top, topdown=True):
    for fname in files:
        existing.append(os.path.join(root, fname))

# List of items to process (depends on overwriting preferences set at the start):
if overwrite_stuff:
    to_process_2000 = list_2000
    to_process_2010 = list_2010
else:
    to_process_2000 = [item for item in list_2000 if item['destin_path'] not in existing]
    to_process_2010 = [item for item in list_2010 if item['destin_path'] not in existing]


# Download files (2000)
for item in to_process_2000:
    source_url = item['source_url']
    destin_path = item['destin_path']
    split_path = destin_path.split('\\')
    for i, subdir in enumerate(split_path[:-1]):
        if not os.path.exists('\\'.join(split_path[:i+1])):
            print("Path", '\\'.join(split_path[:i+1]), "does not exist: creating...")
            os.mkdir(os.path.join('\\'.join(split_path[:i+1])))

    connection.ftp_obj.voidcmd("NOOP")
    download_url(url=source_url, output_path=destin_path)
    time.sleep(3)


# Download files (2010)
for item in to_process_2010:
    source_url = item['source_url']
    destin_path = item['destin_path']
    split_path = destin_path.split('\\')
    for i, subdir in enumerate(split_path[:-1]):
        if not os.path.exists('\\'.join(split_path[:i+1])):
            print("Path", '\\'.join(split_path[:i+1]), "does not exist: creating...")
            os.mkdir('\\'.join(split_path[:i+1]))

    connection.ftp_obj.voidcmd("NOOP")
    download_url(url=source_url, output_path=destin_path)
    time.sleep(3)
