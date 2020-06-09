#!/usr/bin/env python3

import os

class FilesList:

    def __init__(self, path, extension):
        self.flist = []
        self.ext = extension
        for file in os.listdir(path):
            fname, ext = os.path.splitext(file)
            if extension in ext[1:]:
                self.flist.append(fname)

    def __getitem__(self, index):
        return '.'.join((self.flist[index], self.ext))

    def __contains__(self, target):
        return target in self.flist

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index == len(self.flist): raise StopIteration
        item = '.'.join((self.flist[self.index], self.ext))
        self.index += 1
        return item

    def get_extension(self):
        return self.ext

    def set_extension(self, extension):
        self.ext = extension

    def get_new_extension_list(self, extension):
        flist = []
        for item in self.flist:
            flist.append('.'.join((item, extension)))
        return flist

if __name__ == '__main__':
    pass
