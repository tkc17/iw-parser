# iw command output parser

This tools parses the iw command outputs. Please note that `iw` warns about screen scraping, so, please use this tool at your own risk.

## iw dump to CSV

For now, only `iw dump` to CSV output is supported.

```
$ pip3 install .
$ iw-dump-csv -i wlp0s20f3 -o test.csv -t 
```
Note: Please make sure `python` bin directory is in the $PATH.
