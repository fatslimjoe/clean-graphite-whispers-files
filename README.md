# clean-graphite-whispers-files
Purge stale Whisper’s files with clean-graphite-whisper-files.py

We have developed a new graphite cleaner micro script specifically designed to purge old stale whisper data. The existing community scripts were not well-suited for our environment as they generated some warnings and were written in Python 2. Furthermore, they lacked information about the age of stale graphite files, which could be useful in our case.

Before you begin using the script, please verify the path of your interpreter. Usually, the default path is: `#!/usr/bin/python3`

## IMPORTANT


Before using the script, it is recommended to estimate the total size of your stale whisper files. You can use the --dry-run option, which will not take any action but will provide a summary of what should be deleted.

If you have a large number of files and the whisper files are not on a separate disk, it may significantly impact the performance of your Graphite server due to high disk I/O. Therefore, it is recommended to execute the script in parts, gradually reducing the number of '--days' parameter each time.

Exercise caution when using the -l argument, which enables logging and stores logs in /var/log/graphite_cleanup_yyyy_mm_dd.log. This can result in additional disk I/O and potentially affect the performance of your Graphite server and could use a lot of additional storage place.


## Usage

Example,

`./clean-graphite-whispers-files.py -s -p /opt/graphite/storage/whisper --dry-run`

To find more option, you can use -h argument:

```
./clean-graphite-whispers-files.py -h
usage: clean-graphite-whispers-files.py [-h] -d DAYS [-i] -p PATH [-l] [-s]

Retrieve old obsolete whisper files and delete them!

optional arguments:
  -h, --help            show this help message and exit
  -d DAYS, --days DAYS  Older then, number of days, default is 365 days
  -i, --dry-run         Show me only what it could be deleted, without delete
                        action!
  -p PATH, --path PATH  Path/location of whisper files, dafault:
                        /opt/graphite/storage/whisper
  -l, --log             Enable logging, dafault:
                        /var/log/graphite_cleanup_yyyy_mm_dd.log
  -s, --show            Show me output of each deleted file!
```

Example output:

```
...
...
...
[2023-05-08 15:08:54] /opt/graphite/storage/whisper/_tagged/109/009/1090094f75a9b7612088c2be04b0ac3fc2ec930f5072c4597e8def34e638f449.wsp (age: 576.9 days, last update: 2021-10-08 14:36:40)
[2023-05-08 15:08:54] Deleted /opt/graphite/storage/whisper/_tagged/109/009/1090094f75a9b7612088c2be04b0ac3fc2ec930f5072c4597e8def34e638f449.wsp!
[2023-05-08 15:08:54] /opt/graphite/storage/whisper/_tagged/109/2c6/1092c64ca4d605d7737d68d1a7d1cf3f600778799174c9d1185e7b505c17e184.wsp (age: 563.2 days, last update: 2021-10-22 08:58:35)
[2023-05-08 15:08:54] Deleted /opt/graphite/storage/whisper/_tagged/109/2c6/1092c64ca4d605d7737d68d1a7d1cf3f600778799174c9d1185e7b505c17e184.wsp!
[2023-05-08 15:08:54] /opt/graphite/storage/whisper/_tagged/109/9dd/1099dd0f05ae6ac4a20c915bf4f52abf57b6666d34e356edd8257cdfbc59a6ab.wsp (age: 563.0 days, last update: 2021-10-22 12:29:35)
[2023-05-08 15:08:54] Deleted /opt/graphite/storage/whisper/_tagged/109/9dd/1099dd0f05ae6ac4a20c915bf4f52abf57b6666d34e356edd8257cdfbc59a6ab.wsp!

-----------------------------------------------------------------------------------------------------------------------------------------
Total Deleted whisper files 733655, Total deleted size: 146764.98 MB, Total size of all whisper files: 203.113675 GB, Ratio: 70.56% deleted
```
### Have Fun! :)
