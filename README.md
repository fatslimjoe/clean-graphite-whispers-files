# clean-graphite-whispers-files
Purge stale Whisper’s files with clean-graphite-whisper-files.py

We have developed a new graphite cleaner micro script specifically designed to purge old stale whisper data. The existing community scripts were not well-suited for our environment as they generated some warnings and were written in Python 2. Furthermore, they lacked information about the age of stale graphite files, which could be useful in our case.

Before you begin using the script, please verify the path of your interpreter. Usually, the default path is: `#!/usr/bin/python3`

The script uses standard Python 3 libraries, so there is no need to install additional Python 3 packages.

## IMPORTANT


Before using the script, always make a backup. You will be using the script at your own responsibility. It is recommended to estimate the total size of your stale whisper files. You can use the `--dry-run` option, which will not take any action but will provide a summary of what should be deleted.

If you have a large number of files and the whisper files are not on a separate disk, it may significantly impact the performance of your Graphite server due to high disk I/O. Therefore, it is recommended to execute the script in parts, gradually reducing the number of '--days' parameter each time.

Exercise caution when using the `-l` argument, which enables logging and stores logs in `/var/log/graphite_cleanup_yyyy_mm_dd.log`. This can result in additional disk I/O and potentially affect the performance of your Graphite server and could use a lot of additional storage place.


## Usage

Example,

`./clean-graphite-whispers-files.py -h`

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

More examples:

Without `--dry-run` or `-i` parametar: 
`./clean-graphite-whispers-files.py -d 365 -p /opt/graphite/storage/whisper -s`

```
...
...
...
[2023-05-09 09:23:28] Deleted /opt/graphite/storage/whisper/icinga2/s1_local/host/hostalive/perfdata/rta/warn.wsp! (no_update_days: 1103.4 days, last_update: 2020-04-30 23:10:40)
[2023-05-09 09:23:28] Deleted /opt/graphite/storage/whisper/icinga2/s1_local/host/hostalive/perfdata/rta/value.wsp! (no_update_days: 1103.4 days, last_update: 2020-04-30 23:10:40)
[2023-05-09 09:23:28] Deleted /opt/graphite/storage/whisper/icinga2/s1_local/host/hostalive/perfdata/rta/crit.wsp! (no_update_days: 1103.4 days, last_update: 2020-04-30 23:10:40)
Total Deleted whisper files 2256, Total deleted size: 450.63 MB, Total size of all whisper files: 198.460124 GB, Ratio: 0.22% deleted, Script duration: 0:03:40.065513

```

With `--dry-run` or `-i` parametar 
`./clean-graphite-whispers-files.py -d 365 -p /opt/graphite/storage/whisper -s -i`:

```
...
...
...
[2023-05-09 15:01:41] /opt/graphite/storage/whisper/_tagged/e00/319/e00319b44cb16e60e9c8eaa1213beabce813998bbee8aa328440361d23e75300.wsp (no_update_days: 1336.1 days, last_update: 2019-09-11 12:37:53)
Total old stale whisper files 26975, Total size of old stale whisper files: 5361.13 MB, Total size of all whisper files: 203.220223 GB, Ratio: 2.58% to be deleted, Script duration: 0:05:42.421645
```

### Have Fun! :)
