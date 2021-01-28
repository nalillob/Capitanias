"""Description: This is a utility script that declares and stores important directories in a dict objetct. It is
configured for Python 3.x, but a version for Python 2.x exists with the name setup_dirs_2x.py. """

import os


# function to check whether directories exist:
def check_dirs(directory_dict):
    print('Checking directories...', end=" ")
    checked_dict = directory_dict
    for key in directory_dict.keys():
        dirpath = directory_dict[key]['path']
        status = os.path.exists(dirpath)
        checked_dict[key]['status'] = status
    print("Done.")
    return checked_dict


# function to create missing directories:
def create_dirs(directory_dict, report=False):
    checked_dict = check_dirs(directory_dict)

    # list of statuses:
    status_list = [checked_dict[key]['status'] for key in checked_dict.keys()]

    while all(status_list) is False:
        for key in directory_dict.keys():
            dirpath = checked_dict[key]['path']
            status = checked_dict[key]['status']
            if not status and os.path.exists(os.path.dirname(dirpath)):
                os.mkdir(dirpath)
                if report:
                    print('Created', dirpath)
            elif status and os.path.exists(os.path.dirname(dirpath)):
                if report:
                    print(dirpath, 'already exists.')
            elif not status and not os.path.exists(os.path.dirname(dirpath)):
                if report:
                    print("{0}'s".format(dirpath), "base directory does not exist. No new directory created.")

        # update status list:
        checked_dict = check_dirs(directory_dict)
        status_list = [checked_dict[key]['status'] for key in checked_dict.keys()]
    return


# define dictionary with directories:
def def_dirs():
    dir_py = os.getcwd()
    dir_main = os.path.split(dir_py)[0]
    dir_data = os.path.join(dir_main, 'data')
    dir_rawdata = os.path.join(dir_data, 'raw')
    dir_dtadata = os.path.join(dir_data, 'dta')
    dir_gisdata = os.path.join(dir_data, 'gis')
    dir_results = os.path.join(dir_main, 'results')
    dir_docs = os.path.join(dir_main, 'docs')
    dir_dict = {'main': {'path': dir_main},
                'data': {'path': dir_data},
                'pyfiles': {'path': dir_py},
                'raw_data': {'path': dir_rawdata},
                'dta_data': {'path': dir_dtadata},
                'gis_data': {'path': dir_gisdata},
                'docs': {'path': dir_docs},
                'results': {'path': dir_results}}
    return dir_dict
