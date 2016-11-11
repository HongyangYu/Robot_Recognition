#!/usr/bin/env python
import re
import sys
import os.path

# This is a tiny script to help you creating a CSV file from a face
# database with a similar hierarchie:
#
#  philipp@mango:~/facerec/data/at$ tree
#  .
#  |-- README
#  |-- s1
#  |   |-- 1.pgm
#  |   |-- ...
#  |   |-- 10.pgm
#  |-- s2
#  |   |-- 1.pgm
#  |   |-- ...
#  |   |-- 10.pgm
#  ...
#  |-- s40
#  |   |-- 1.pgm
#  |   |-- ...
#  |   |-- 10.pgm
#

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print "usage: create_csv <base_path> <output_filename>"
        sys.exit(1)

    BASE_PATH=sys.argv[1]
    fh = open( sys.argv[2], 'w' )
    SEPARATOR=";"

    for dirname, dirnames, filenames in os.walk(BASE_PATH):
        for subdirname in dirnames:
            label = re.findall('[0-9]+', subdirname)[-1]
            label = int(label)-1
            subject_path = os.path.join(dirname, subdirname)
            for filename in os.listdir(subject_path):
                abs_path = "%s/%s" % (subject_path, filename)
                #print "%s%s%d" % (abs_path, SEPARATOR, label)
                fh.write("%s%s%d\n" % (abs_path, SEPARATOR, label))
    fh.close()
