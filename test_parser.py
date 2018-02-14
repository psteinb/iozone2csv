#!/usr/bin/env python3

import pytest
import re

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


@pytest.fixture
def full_iozone_stdout():

    with open("iozone.out","r") as inf:
        content = inf.readlines()
        return "".join(content)

def test_fixture(full_iozone_stdout):

    assert len(full_iozone_stdout) != 0
    assert type(full_iozone_stdout) == type(str("foo"))
    assert full_iozone_stdout.count('\n')

def test_definition(full_iozone_stdout):

    ex = iozone_extract(full_iozone_stdout)

    assert len(ex.stdout) != 0

def test_version(full_iozone_stdout):

    ex = iozone_extract(full_iozone_stdout)

    res = ex.version()

    assert type(res) == type("42.2")
    assert ex.version() != 0
    assert float(res) == 3.434


def test_build(full_iozone_stdout):

    ex = iozone_extract(full_iozone_stdout)
    res = ex.build()
    assert type(res) == type("42.2")
    assert res == "linux-AMD64"

def test_unit(full_iozone_stdout):

    ex = iozone_extract(full_iozone_stdout)
    res = ex.output_unit()
    exp = "kBytes/sec"
    assert type(res) == type(exp)
    assert res == exp

def test_timeres(full_iozone_stdout):

    ex = iozone_extract(full_iozone_stdout)
    res = ex.time_resolution_seconds()

    exp = "0.000001"
    assert type(res) == type(exp)
    assert res == exp

def test_cachedetails(full_iozone_stdout):

    ex = iozone_extract(full_iozone_stdout)
    res = ex.assumed_cache()

    exp = (1024,32)

    assert type(res) == type(exp)
    assert res == exp

def test_filestride(full_iozone_stdout):

    ex = iozone_extract(full_iozone_stdout)
    res = ex.file_stride()

    exp = 17

    assert type(res) == type(exp)
    assert res == exp

def test_table_header(full_iozone_stdout):

    ex = iozone_extract(full_iozone_stdout)
    res = ex.table_header()

    exp = ["kB","reclen","write","rewrite","read","reread","randomread","randomwrite","bkwdread","recordrewrite","strideread","fwrite","frewrite","fread","freread"]

    assert type(res) == type(exp)
    assert res == exp

def test_experiments_only(full_iozone_stdout):

    ex = iozone_extract(full_iozone_stdout)
    res = ex.experiments()

    assert type(res) == type([])
    assert len(res) == 8
