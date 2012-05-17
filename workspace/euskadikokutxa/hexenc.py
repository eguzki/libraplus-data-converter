import sys
import os
import codecs

def hexenc(filename, encoding="utf8"):
    """docstring for splitter"""
    file_object = codecs.open(filename, mode = 'r', encoding = encoding)
    for line in file_object.readlines():
        # line object containg new-line chars
        sys.stdout.write("%s" % line)
        for char in line:
            sys.stdout.write("\\u%0.4x" % ord(char))
        sys.stdout.write("\n")

def main():

    if len(sys.argv) != 3:
        sys.stderr.write("help: %s filename encoding\n" % (sys.argv[0]))
        sys.stderr.write("example: %s data.txt latin1\n" % (sys.argv[0]))
        exit(-1)

    filename = sys.argv[1]
    encoding = sys.argv[2]
    hexenc(filename, encoding)

if __name__ == "__main__":
    main()
