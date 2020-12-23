import os
import setup_dirs
import zipfile


def existing(topdir):
    zip_list = []
    subdirs_list = []

    # Walk through from top directory, looking for subdirectories and zip files:
    for root, dirs, files in os.walk(top=topdir, topdown=True):
        for f in files:
            if f.endswith('.zip'):
                zip_list.append(os.path.join(root, f))

        for d in dirs:
            subdirs_list.append(os.path.join(root, d))

    paired_list = []
    for zf in zip_list:
        if os.path.basename(zf).split('.')[0] in subdirs_list:
            paired_list.append({'Filename': zf, 'Unzipped': True})
        else:
            paired_list.append({'Filename': zf, 'Unzipped': False})

    return paired_list


def unzipper(topdir, children=False, overwrite=False, flatten=False):
    # Get list of zip files and subdirectories of topdir:
    zip_list = existing(topdir=topdir)

    # Create "to unzip" list:
    if overwrite:
        to_unzip_list = zip_list
    else:
        to_unzip_list = [z for z in zip_list if not z['Unzipped']]

    while len(to_unzip_list) > 0:
        # Loop over zip files and extract:
        for zd in to_unzip_list:
            zf = zd['Filename']
            z = zipfile.ZipFile(zf)
            z_filenames = [n.split('.')[0].upper() for n in z.namelist() if not n.endswith('/')]
            z_subdirnms = [n.split('/')[0] for n in z.namelist() if n.endswith('/')]

            if os.path.basename(zf).split(".")[0] in z_subdirnms and len(z_subdirnms) == 1:
                extract_path = os.path.dirname(zf)
                print("Unzipped", os.path.basename(zf), "to", extract_path, ": case 1")
                case = 1
            elif os.path.basename(zf).split(".")[0] not in z_subdirnms \
                    and os.path.basename(zf).split(".")[0] in z_filenames:
                extract_path = os.path.dirname(zf)
                print("Unzipped", os.path.basename(zf), "to", extract_path, ": case 2")
                case = 2
            else:
                extract_path = os.path.join(zf.split(".zip")[0])
                if not os.path.exists(extract_path):
                    os.mkdir(extract_path)
                print("Unzipped", os.path.basename(zf), "to created dir", extract_path, ": case 3")
                case = 3

            if not flatten or case == 3:
                z.extractall(path=extract_path)
            else:
                for sub_zf in [n for n in z.namelist() if not n.endswith('/')]:
                    with open(os.path.join(extract_path, sub_zf.split('/')[-1]), 'wb') as f:
                        f.write(z.read(sub_zf))

        if children:
            print("Looking for children zip files to unzip...", end="")
            # Get list of zip files and subdirectories of topdir:
            all_zip_list = existing(topdir=topdir)
            old_zip_list = zip_list.copy()
            new_zip_list = [zd for zd in all_zip_list if zd not in old_zip_list]
            zip_list = all_zip_list.copy()

            # Create "to unzip" list:
            if overwrite:
                to_unzip_list = [zd for zd in new_zip_list]
            else:
                to_unzip_list = [zd for zd in new_zip_list if not zd['Unzipped']]
            if len(to_unzip_list) == 0:
                print("None left.")
        else:
            to_unzip_list = []

    return


# Preferences:
overwrite_stuff = False

# Load directories and create them if they don't exist:
dir_dict = setup_dirs.def_dirs()
setup_dirs.create_dirs(directory_dict=dir_dict, report=True)

# Define raw data directory:
raw_data_dir = os.path.join(dir_dict['raw_data']['path'], 'IBGE')
if not os.path.exists(raw_data_dir):
    os.mkdir(raw_data_dir)

parent_dir = os.path.join(raw_data_dir, "Censo_2010")
