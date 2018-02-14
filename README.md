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

