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

if platform.system() == "Windows":
    import os
    import wmi

    print("Processors info:")
    #connect to WMI local machine
    winloc = wmi.WMI()
    #show wmi class
    # for classname in winloc.classes:
    #     if "Processor" in classname:
    #         print(classname)

    #get processor info
    w32processor = winloc.Win32_Processor()
    for i in w32processor:
        cpu_name = i.Name
        cpu_count_core = i.NumberOfCores
        print(cpu_name + "\n" + "CoreCount: " + str(cpu_count_core))
        print(i)

    #general system info
    w32compsystem = winloc.Win32_ComputerSystem()
    for i in w32compsystem:
        print(i)

    print("Memory info:")
    w32phy_mem = winloc.Win32_PhysicalMemory()
    for i in w32phy_mem:
        mem_locate = i.DeviceLocator
        capacity_mb = int(i.Capacity) // (1024 * 1024)
        name = i.Name
        manufac = i.Manufacturer
        print(name + " " + manufac + " " + mem_locate + " Capacity: " + str(capacity_mb) + "MB")
