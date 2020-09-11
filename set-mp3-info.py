#!/usr/bin/env python3

import re
import sys
import csv
import os
from mutagen.mp3 import EasyMP3 as MP3
# from mutagen.mp3 import EasyMP3

## Overriding csv.DictReader to strip whitespace and ignore case
class MyDictReader(csv.DictReader, object):
    @property
    def fieldnames(self):
        return [field.strip() for field in super(MyDictReader,
            self).fieldnames]

# Read csv file
def csv_dict_reader(infile):
    reader = MyDictReader(open(infile), delimiter=',',skipinitialspace=True)
    return reader

# Check the existence of files
def checkfiles(files_passed):

    for key, ifile in files_passed.items():
        # If variable for the file is passed
        if ifile:
            if not os.path.exists(ifile):
                sys.exit("Required file '%s' not found. Aborting." % ifile)
        else:
        # If the requried variable is not passed
            sys.exit("Required '%s' file not supplied. Aborting." % key)


def helptext(scriptname):
    print("Script to set mp3 information from csv file.")
    print("Usage: %s [options] file.csv" % scriptname)
    print("") 
    print("Options:")
    print("-h|--help        Show this help and exit.")
    return 


if __name__ == '__main__':

    csvfile = None

    scriptname = os.path.basename(sys.argv[0])
    author = 'Anjishnu Sarkar'
    version = '0.1'

    # Number of arguments supplied via cli
    numargv = len(sys.argv)-1
    # Argument count
    iargv = 1

    # Parse cli options
    while iargv <= numargv:

        if sys.argv[iargv] == '-h' or sys.argv[iargv] == '--help':
            helptext(scriptname)
            sys.exit(0)

        elif re.search('.csv$',sys.argv[iargv]):
            csvfile = sys.argv[iargv]

        else:
            sys.exit("%s: Unspecified option %s. Aborting." 
                % (scriptname, sys.argv[iargv]))
        iargv += 1 

    # Check the existence of the csvfile
    allfiles = {'csv': csvfile}
    checkfiles(allfiles)

    # Read csv and store as dictionary
    dict_reader = csv_dict_reader(csvfile)
    headers = dict_reader.fieldnames

    # Write the metadata
    for row_line in dict_reader:

        # If the file doesn't exists then omit it and continue
        mp3file = row_line['file']
        if not os.path.exists(mp3file):
            print("File '%s' not found. Moving on..." % mp3file)
            continue ;
        
        audio = MP3(mp3file)
        for hdr in headers:

            if hdr == 'file':
                print("%s: %s" %(hdr, row_line[hdr]))
            else:
                try:
                    audio[hdr] = row_line[hdr]
                    print("%s: %s" %(hdr, row_line[hdr]))
                except:
                    print("Warning: Key '%s' not found." % hdr)
        
        print("")

        audio.pprint()
        audio.save()

