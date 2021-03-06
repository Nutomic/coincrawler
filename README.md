Coincrawler
===========

Coincrawler is a network crawler for multiple Bitcoin-based cryptocurrencies.
At the moment, it includes configurations for Bitcoin, Bitcoin Cash, Dash
and Litecoin. The project is forked from
[Bitnodes](https://github.com/ayeowch/bitnodes).

The development of this project was sponsored by Alexey Eromenko "Technologov".

Usage
-----

See the [installation instructions](INSTALL.md) for steps on setting up a
machine to run Coincrawler.

After installation, simply run `./start-coin.sh bitcoin|bitcoincash|dash|litecoin`.
Or run `./start-all.sh` to start crawls for all coins.

There is currently no easy way to stop the crawl. You can kill each process
manually, or run `killall python2`. Be careful, this will also kill all other
Python programs running on the system.

Files and folders generated by the crawler:
```
data/crawl/  # Internal, temporary files.
data/export/ # Outputs from the crawl. See the next section for explanation.
data/export/ # SQLite databases with historical crawl results. Used to calculate
             # the node uptimes.
log/         # Log and error outputs from the various components.
```

The folders `data/crawl/`, `data/export/` and `log/` can be safely deleted while
the crawler is stopped.

Output format
-------------

Crawl outputs are stored in `data/export/*coinname*/`. Each result is stored
as .csv, and as .txt. Both contain the same data, the only difference is that
one uses commas as seperators, and one uses spaces. Each line contains
information about one node:

```
"123.123.123.123:9999", # IP address:port
"50.00%",               # uptime percentage (last 2 hours)
"11.25%",               # uptime percentage (last 8 hours)
"12.62%",               # uptime percentage (last 24 hours)
"12.62%",               # uptime percentage (last 7 days)
"12.62%",               # uptime percentage (last 30 days)
935794,                 # last block
70210,                  # protocol version
"/Dash Core:0.12.3.2/", # client version
"US",                   # country
"America/New_York",     # city
"DigitalOcean, LLC",    # ISP cloud
1,                      # 1 if the node's block height is at most 12 different
                        # from the median (see config value max_block_height_difference)
1                       # 1 for Dash masternodes, 0 otherwise (only for Dash)

```

Uptime is calculated in the following way: For each interval (2 hours,
8 hours, 1 day etc), we take the total number of crawls during that
time as `all_scans_in_interval`. We also check when we first
encountered the particular node as `node_first_encountered`, and the total
number of times we encountered the node in this interval, as
`node_times_encountered`. The uptime percentage for a particular node and
time interval is then (in Python):

```python
scans_since_first_encounter = \
        filter(lambda scan_time: scan_time >= node_first_encountered, all_scans_in_interval)
uptime_percentage = node_times_encountered / len(scans_since_first_encounter)
```

For example, if we first encountered a node 1 hour ago, and we reached it in
every subsequent scan, it would be listed with an uptime of 100% across all
intervals. But if the node was only reachable during 1 out of 5 scans in the
last hour, it would have an uptime of 4 / 5 = 80%. The same uptime would
also be shown for all other intervals, because we don't have enough data
for them. Note that values for longer intervals only
become meaningful after running the crawler for at least this interval. For
example, after running the crawler for 5 days, the uptime percentage
for 7 days and 30 days will by definition be the same.

Development
-----------

The [Redis Data](redis-data.md) document contains the list of keys and their
associated values that are written by the scripts in this project.

License
-------

The project is licensed under the [MIT license](LICENSE).
