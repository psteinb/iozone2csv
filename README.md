# iozone2csv

Small python script that converts the output of iozone to csv which can then be used to visual individual parts of the data.

## assumed iozone usage

I assume that you have launched iozone for example in the following manner:

``` bash
$ iozone -a -n 1g -g 2g -y 512k -q 4m  -f /tmp/testme
```

Which produces outputs like [iozone.out](iozone.out) to your terminal. To capture this to a file (e.g. `iozone.out`, do the following:

``` bash
$ iozone -a -n 1g -g 2g -y 512k -q 4m  -f /tmp/testme > iozone.out
```

## using the converter

In it's simplest form, the following

``` bash
$ python3 ./iozone2csv.py iozone.out
```

will produce `iozone.csv` which contains the tabular fields from the iozone output as csv fields. The tool also supports multiple input files:

``` bash
$ python3 ./iozone2csv.py iozone1.out iozone2.out iozone3.out 
```

This will concatenate the tables into `iozone.csv` and assign each entry the respective file name as `id`.

More feedback on the code is highly welcome!
