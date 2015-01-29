#!/usr/bin/python

import json
import sys
import subprocess

if __name__ == '__main__':
    if sys.version_info < (2, 7, 0):
    	# Workaround for python 2.6
    	process = subprocess.Popen(['cat','/proc/diskstats', ], stdout=subprocess.PIPE)
        out,err = process.communicate()
        disks = list()
        for line in out.split("\n"):
                if line:
                     disk = line.split()[2]
                     if not (disk.startswith('ram') or disk.startswith('loop') or disk.startswith('sr')): disks.append(disk)
        output = "\n".join(disks)
    else:
    	output = subprocess.check_output("cat /proc/diskstats | awk '{print $3}' | grep -v 'ram\|loop\|sr'", shell=True)
    data = list()
    for line in output.split("\n"):
        if line:
	        data.append({"{#DEVICE}": line, "{#DEVICENAME}": line.replace("/dev/", "")})

    print(json.dumps({"data": data}, indent=4))
