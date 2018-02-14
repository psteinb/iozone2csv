#!/usr/bin/env python3

import pytest

from iozone2csv import iozone_extract

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
