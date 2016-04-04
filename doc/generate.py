#!/usr/bin/env python
from __future__ import print_function

from os.path import join, dirname

try:
    from robot.libdoc import libdoc
except:
    def main():
        print("""Robot Framework 2.7 or later required for generating documentation""")
else:
    def main():
        libdoc(join(dirname(__file__), '..', 'src', 'TestToolsMK'), join(dirname(__file__), 'TestToolsMK.html'))

if __name__ == '__main__':
    main()
