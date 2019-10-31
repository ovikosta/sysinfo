#!/bin/env python3

import platform


# view list disk with size
# info about cpu and ram with general characteristics
if platform.system() == "Linux":
    # get processors info from /proc/cpuinfo
    print("Processors info:")
    with open("/proc/cpuinfo", "r") as f:
        info = f.readlines()

    cpuinfo = [x.strip().split(":")[1] for x in info if "model name" in x]
    for index, item in enumerate(cpuinfo):
        print(str(index) + ":" + item)

    # ger ram info from /proc/meminfo
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

    # connect to WMI local machine
    winloc = wmi.WMI()
    # get general system info
    w32compsystem = winloc.Win32_ComputerSystem()
    for i in w32compsystem:
        cpu_num = i.NumberOfProcessors
        hostname = i.DNSHostName
    print("Hostname: " + hostname)

    print("\nProcessors info:")

    # get processor info
    w32processor = winloc.Win32_Processor()
    for i in w32processor:
        cpu_name = i.Name
        cpu_count_core = i.NumberOfCores
        print(cpu_name + "\n" + "CpuNumber: " +
              str(cpu_num) + "\n" "CoreCount: " + str(cpu_count_core))

    print("\nMemory info:")
    # get memory info
    w32phy_mem = winloc.Win32_PhysicalMemory()
    for i in w32phy_mem:
        mem_locate = i.DeviceLocator
        mem_cap_mb = int(i.Capacity) // (1024 * 1024)
        mem_name = i.Name
        mem_manufac = i.Manufacturer
        print(mem_name + " " + mem_manufac + " " + mem_locate +
              " Capacity: " + str(mem_cap_mb) + "MB")

    print("\nDisk info:")
    # get disk info
    w32disk = winloc.Win32_DiskDrive()
    for i in w32disk:
        disk_desc = i.Description
        disk_model = i.Model
        disk_part = i.Partitions
        disk_size_mb = int(i.Size) // (1024 * 1024)
        print(disk_desc + " " + disk_model + "\nDiskSize: " +
              str(disk_size_mb) + "MB" + "\nDiskPartitions: " + str(disk_part))
