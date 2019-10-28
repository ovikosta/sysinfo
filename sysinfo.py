#!/bin/env python3

import platform


#view list disk with size
#info about cpu and ram with general characteristics
if platform.system() == "Linux":
    #get processors info from /proc/cpuinfo
    print("Processors info:")
    with open("/proc/cpuinfo", "r") as f:
        info = f.readlines()

    cpuinfo = [x.strip().split(":")[1] for x in info if "model name" in x]
    for index, item in enumerate(cpuinfo):
        print(str(index) + ":" + item)
    
    #ger ram info from /proc/meminfo
    print("\nMemory info:")
    gchar_ram = ["MemTotal", "MemFree", "MemAvailable"]
    with open("/proc/meminfo", "r") as f:
        info = f.readlines()

    raminfo = [x.strip().split(":") for x in info]
    for i, x in raminfo:
        if i in gchar_ram:
            print(i + ":" + x)

