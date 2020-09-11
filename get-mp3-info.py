#!/usr/bin/env python3

import re
import sys
import csv
import os
from mutagen.mp3 import EasyMP3 as MP3
from glob import glob

# Check the input and output files
def checkfiles(outfile = None):
   
    # Check if variable outfile has been supplied or not
    if ( not outfile ):
        print("No output csv file has been supplied. Aborting.")
        sys.exit(1)


def helptext(scriptname):
    print("Script to get mp3 information.")
    print("Usage: %s [options] file1.mp3 [file2.mp3] [...] info.csv")
    print("") 
    print("Options:")
    print("-h|--help        Show this help and exit.")
    return


if __name__ == '__main__':

    mp3list = []
    outcsvfile = None
    csv_headers = (['tracknumber', 'file', 'title', 'artist', 'album', 
        'genre', 'date'])

    scriptname = os.path.basename(sys.argv[0]) 

    # Number of arguments supplied via cli
    numargv = len(sys.argv)-1
    # Argument count
    iargv = 1

    # Parse cli options
    while iargv <= numargv:

        if sys.argv[iargv] == "-h" or sys.argv[iargv] == "--help":
            helptext(scriptname)
            sys.exit()

        elif re.search(".mp3$",sys.argv[iargv]):
            mp3list.extend(glob(sys.argv[iargv]))

        elif re.search(".csv$",sys.argv[iargv]):
            outcsvfile = sys.argv[iargv]

        else:
            print ("%s: Unspecified option: '%s'. Aborting." 
                % (scriptname, sys.argv[iargv]))
            sys.exit(1)

        iargv += 1 


    # Check the existence of the supplied file
    checkfiles(outcsvfile)

    writer = csv.DictWriter(open(outcsvfile, 'w'), fieldnames = csv_headers)
    writer.writeheader()

    for mp3file in mp3list:

        info = {}
        info['file'] = mp3file

        tags = MP3(mp3file)
        for hdr in csv_headers:

            if hdr == 'file':
                pass
            else:
                try:
                    info[hdr] = tags[hdr][0]
                except KeyError:
                    info[hdr] = ''
            
        writer.writerow(info)                       
