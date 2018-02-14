# iozone2csv

Small python script that converts the output of iozone to csv which can then be used to visual individual parts of the data.

## assumed iozone usage

I assume that you have launched iozone for example in the following manner:

``` bash
$ iozone -a -n 1g -g 2g -y 512k -q 4m  -f /tmp/testme
```

Which produces outputs like [iozone.out](iozone.out)
