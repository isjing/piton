from getopt import getopt
from sys import argv

import os
import fnmatch
from os.path import splitext
from pyparsing import Word, alphas, quotedString

import es

keywords = object
verbose = False


def translate(string, location, token):
    if token[0] in keywords.tokens:
        return keywords.tokens[token[0]]

    return token


def usage():
    print ''
    print 'Usage:'
    print ''
    print 'piton [-hv] -s <source>'
    print ''
    print ''
    print '-s\tSource file (*.pi)'
    print '-h\tThis help'
    print '-v\tVerbose'
    print ''


def main(argv):
    global verbose, keywords

    lang = es
    keywords = lang.Keywords()

    opts, args = getopt(argv, 's:hv', ['source=', 'help', 'verbose'])
    for opt, arg in opts:
        if opt in ['-s', '--source']:
            source = arg
        elif opt in ['-h', '--help']:
            # show usage
            usage()
            exit()
        elif opt in ['-v', '--verbose']:
            verbose = True

    try:
        if source:
            pass
    except:
        print('The source is not defined')
        usage()
        if verbose:
            print('exit')
        exit()

    # translation settings
    w = Word(alphas)
    w.ignore(quotedString)
    w.setParseAction(translate)

    # get all pi files inside root directory
    for root, dirs, files in os.walk(os.getcwd()):
        piFiles = fnmatch.filter(files, lang.FILE_PATTERN)

        if piFiles:
            for piFile in piFiles:
                # read pi file
                piCode = open(root + '/' + piFile, 'r').read()

                # translate pi file
                pyCode = w.transformString(piCode)

                # create python file
                fpy = open(root + '/' + splitext(piFile)[0] + '.py', 'w')
                fpy.write(pyCode)
                fpy.close()

    # read python file
    pythonCode = open(splitext(source)[0] + '.py', 'r').read()

    # exec python code
    exec pythonCode in {'__name__': '__main__', '__doc__': None}, {}


if __name__ == '__main__':
    main(argv[1:])