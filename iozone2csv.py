#!/usr/bin/env python3

import re
import argparse
import os

class iozone_extract:
    """ extract valuable parts of the iozone output """

    def __init__(self, iozone_stdout=""):
        self.stdout = iozone_stdout
        self.splitted = iozone_stdout.split('\n')
        self.header = []
        for ll in self.splitted:
            if ll.lower().count('random')==2 and ll.lower().count('bkwd') and ll.lower().count('record') and ll.lower().count('stride'):
                break
            self.header.append(ll)


    def version(self):

        vline = [ item for item in self.header[:4] if item.lower().count("version") ]
        rex = re.compile('\d\.\d+')
        value = ""
        if vline:
            match = re.search(rex,vline[0])
            if match:
                return vline[0][match.start():match.end()]

        return value

    def build(self):

        vline = [ item for item in self.header[:5] if item.lower().count("build") ]
        if vline:
            return vline[0].split()[-1]
        else:
            return ""

    def output_unit(self):

        vline = [ item for item in self.header[-10:] if item.lower().count("output is in") ]
        if vline:
            return vline[0].split()[-1]
        else:
            return ""

    def time_resolution_seconds(self):

        vline = [ item for item in self.header[-10:] if item.lower().count("time resolution =") ]
        if vline and "seconds." in vline[0].split():
            return vline[0].split()[-2]
        else:
            return ""

    def assumed_cache(self):
        vline1 = [ item for item in self.header[-10:] if item.lower().count("processor cache size set to ") ]
        vline2 = [ item for item in self.header[-10:] if item.lower().count("processor cache line size set to ") ]

        if vline1 and vline2:
            return (int(vline1[0].split()[-2]),int(vline2[0].split()[-2]))
        else:
            return ""

    def file_stride(self):

        vline = [ item for item in self.header[-5:] if item.lower().count("file stride size") ]
        if vline:
            return int(vline[0].split()[-4])
        else:
            return ""

    def table_header(self):

        top = self.splitted[len(self.header)].split()
        bot = self.splitted[len(self.header)+1]

        value = bot.split()
        for idx in range(6,6+len(top)):
            value[idx] = top[idx-6]+value[idx]

        return value

    def experiments(self, nfields = 6):

        digits = re.compile(" [0-9]+ ")

        value = [ item.split() for item in self.splitted[len(self.header)+1:] if len(re.findall(digits, item)) > nfields ]

        return value


def main():

    parser = argparse.ArgumentParser(description='convert iozone stdout (not the excel stuff to ')
    parser.add_argument('files', type=str, nargs='+',
                        help='output files produced by iozone')
    parser.add_argument('-o','--output', type=str, default='iozone.csv',action='store',
                        help='output files produced by iozone')
    parser.add_argument('-s','--separator', type=str, default=',', action='store',
                        help='separator for output file')
    parser.add_argument('-V','--verbose', action='store_true', default=False,
                        help='separator for output file')

    args = parser.parse_args()

    outputlines = []

    hdr_written = False

    for fname in args.files:
        if not os.path.exists(fname):
            print(fname, " does not exist. Skipping it!")
            continue
        ifile = open(fname,'r')
        iozone_stdout = "".join([ item for item in ifile.readlines() ])
        ioz_parsed = iozone_extract(iozone_stdout)
        if args.verbose:
            print(fname, " produced by iozone ", ioz_parsed.version())

        if not hdr_written:
            thdr = ioz_parsed.table_header()
            thdr += "version,build,cachesize_kB,cachelinesize_kB,file_stride,id".split(',')
#            thdr += '\n'

            outputlines.append((args.separator).join(thdr))
            hdr_written = True

        tbl = ioz_parsed.experiments()
        constant = [ ioz_parsed.version(), ioz_parsed.build(), ioz_parsed.assumed_cache()[0], ioz_parsed.assumed_cache()[-1], ioz_parsed.file_stride(), os.path.split(os.path.abspath(fname))[-1] ]

        for row in tbl:
            cline = [ str(item) for item in row ]
            cline += [ str(item) for item in constant ]
#            cline += '\n'


            outputlines.append(str(args.separator).join(cline))

    ofile = open(args.output,'w')
    ofile.writelines("\n".join(outputlines))
    ofile.close()

if __name__ == '__main__':
    main()
