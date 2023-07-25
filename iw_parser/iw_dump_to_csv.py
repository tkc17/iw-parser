#!/usr/bin/env python3
# Convert below output to CSV
# keys are heading, values are rows

# $ iw dev wlp0s20f3 station dump
# Station c8:7f:54:38:0c:0c (on wlp0s20f3)
# 	inactive time:	8 ms
# 	rx bytes:	27240
# 	rx packets:	101
# 	tx bytes:	15478
# 	tx packets:	94
# 	tx retries:	3
# 	tx failed:	0
# 	beacon loss:	23
# 	beacon rx:	60
# 	rx drop misc:	26
# 	signal:  	-62 [-62, -71] dBm
# 	signal avg:	-61 dBm
# 	tx bitrate:	245.0 MBit/s 80MHz HE-MCS 3 HE-NSS 2 HE-GI 2 HE-DCM 0
# 	tx duration:	0 us
# 	rx bitrate:	648.5 MBit/s 80MHz HE-MCS 6 HE-NSS 2 HE-GI 0 HE-DCM 0
# 	rx duration:	0 us
# 	authorized:	yes
# 	authenticated:	yes
# 	associated:	yes
# 	preamble:	long
# 	WMM/WME:	yes
# 	MFP:		no
# 	TDLS peer:	no
# 	DTIM period:	1
# 	beacon interval:100
# 	short slot time:yes
# 	connected time:	8 seconds
# 	associated at [boottime]:	20013.925s
# 	associated at:	1690312565425 ms
# 	current time:	1690312573478 ms

# Note: Import to CSV without `space` as a delimiter

import subprocess
import csv
import sys
import time
import datetime
import argparse
import signal

from typing import Optional, Dict


def get_iw_dump(iface: str) -> Optional[str]:
    try:
        iw_dump = subprocess.run(
            ["iw", "dev", iface, "station", "dump"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(e.stderr.decode("utf-8"))
        return None
    iw_dump_str = iw_dump.stdout.decode("utf-8")
    return iw_dump_str


# First line is special to get BSSID
# Next lines are key value pairs with ":" as delimiter
def parse_iw_dump(iw_dump: str) -> Dict[str, str]:
    iw_dump_list = iw_dump.split("\n")
    iw_dump_output = {}
    try:
        bssid = iw_dump_list[0].split(" ")[1]
        iw_dump_rest = iw_dump_list[1:]
        iwd = [x.split(":") for x in iw_dump_rest]
        iw_dump_output = {x[0].strip(): x[1].strip() for x in iwd if len(x) == 2}
        iw_dump_output["BSSID"] = bssid
    except Exception:
        # disconnected, write an empty row
        iw_dump_output["BSSID"] = "Disconnected"
    return iw_dump_output


def get_iw_dump_to_csv(iface: str) -> Optional[Dict[str, str]]:
    iw_dump = get_iw_dump(iface)
    if iw_dump is None:
        return None
    return parse_iw_dump(iw_dump)


def write_csv_header(csv_file: str, header: list):
    with open(csv_file, "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(header)


def write_csv_row(csv_file: str, row: list):
    with open(csv_file, "a", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(row)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", help="Interface to monitor", required=True)
    parser.add_argument("-o", "--output", help="Output CSV file", required=True)
    parser.add_argument("-t", "--time", help="Time interval in secs", required=False, default=2)
    args = parser.parse_args()
    return args


def signal_handler(sig: int, frame: object):
    print("Exiting...")
    sys.exit(0)


def main() -> None:
    args = parse_args()
    iface = args.interface
    csv_file = args.output
    header = [
        "Timestamp",
        "BSSID",
        "inactive time",
        "rx bytes",
        "rx packets",
        "tx bytes",
        "tx packets",
        "tx retries",
        "tx failed",
        "beacon loss",
        "beacon rx",
        "rx drop misc",
        "signal",
        "signal avg",
        "tx bitrate",
        "tx duration",
        "rx bitrate",
        "rx duration",
        "authorized",
        "authenticated",
        "associated",
        "preamble",
        "WMM/WME",
        "MFP",
        "TDLS peer",
        "DTIM period",
        "beacon interval",
        "short slot time",
        "connected time",
        "associated at [boottime]",
        "associated at",
        "current time",
    ]
    write_csv_header(csv_file, header)
    signal.signal(signal.SIGINT, signal_handler)
    while True:
        iw_dump = get_iw_dump_to_csv(iface)
        if iw_dump is None:
            time.sleep(int(args.time))
            continue
        timestamp = datetime.datetime.now()
        row = [str(timestamp)]
        for key in header[1:]:
            row.append(iw_dump[key] if key in iw_dump else "")
        write_csv_row(csv_file, row)
        time.sleep(int(args.time))


if __name__ == "__main__":
    main()
