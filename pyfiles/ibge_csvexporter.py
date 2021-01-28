"""Description: This script is a utility that contains a function called fc2csv that exports a feature class's data
to a .csv file. """

# NOTE: since this script uses arcpy, make sure that the Python interpreter is Python 2.x

import os
import arcpy
import unicodecsv as csv
from datetime import datetime


def fc2csv(fc, out_path=None):
    # Parse inputs:
    if out_path is not None and os.path.isdir(out_path):
        outcsv = os.path.join(out_path, "{0}.csv".format(fc))
    else:
        outcsv = os.path.join(os.getcwd(), "{0}.csv".format(fc))

    # Get column names from feature class:
    fields = arcpy.ListFields(fc)
    fnames = [field.name for field in fields]

    try:
        with open(outcsv, 'wb') as f:
            dw = csv.DictWriter(f, fnames)
            # --write all field names to the output file
            dw.writeheader()
            # --now we make the search cursor that will iterate through the rows of the table
            # noinspection PyUnresolvedReferences
            with arcpy.da.SearchCursor(fc, fnames) as cursor:
                for row in cursor:
                    dw.writerow(dict(zip(fnames, row)))
        print 'Table data of Feature Class {0} exported as {0}.csv at {1}'.format(fc, str(datetime.now()))
    except arcpy.ExecuteError:
        print 'ExecuteError: could not export Table data of Feature Class {0} ' \
              'as csv at {1}'.format(fc, str(datetime.now()))

    return
