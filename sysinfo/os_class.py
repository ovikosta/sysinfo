import os
import wmi

import abc_class


class WindowsOS(abc_class.AbstractBaseOS):

    def __init__(self):
        # Connect to WMI local machine
        self.winloc = wmi.WMI()

    def hostname(self):
        # Get hostname
        w32compsystem = self.winloc.Win32_ComputerSystem()
        for i in w32compsystem:
            hostname = i.DNSHostName
        print("Hostname: " + hostname)

    def cpu(self, cpu_arg=None, core_num=None):
        print("Processor info:")
        # Get general system info for number of processors
        w32processor = self.winloc.Win32_Processor()
        if cpu_arg:
            if core_num:
                # Realtime info for core
                w32proc_rt = self.winloc.Win32_PerfFormattedData_PerfOS_Processor()
                for i in w32proc_rt:
                    if core_num == int(i.Name):
                        # Print core name, load and idle in precent for core.
                        core_name = i.Name
                        core_usage = i.PercentProcessorTime
                        core_idle = i.PercentIdleTime
                        print("Core: " + core_name + " PercentUsage: " +
                              core_usage + "%" + " PercentIdle: " + core_idle + "%")
            else:
                for cpu_number, i in enumerate(w32processor):
                    # Print processors name, count core, load in percentage and socket.
                    cpu_name = i.Name
                    cpu_count_core = i.NumberOfCores
                    cpu_usage = i.LoadPercentage
                    cpu_socket = i.SocketDesignation
                    print(cpu_name + "\nSocket: " + cpu_socket + "CpuNumber: " +
                          str(cpu_number) + "\n" "CoreCount: " + str(cpu_count_core) + "\nPercentLoad: " + cpu_usage + "%")
                    print("\nIf you show realtime info about processor \
                            use time, add arguments number of the core.\
                                For example '--cpu 1'")
        else:
            for cpu_number, i in w32processor:
                # Print cpu count and name processors.
                cpu_name = i.Name
                print(str(cpu_number) + cpu_name)
            print("\nYou can show more information about processors,\
                    add arguments '--cpu'")

    def ram(self, ram_arg=None, ram_num=None):
        print("\nMemory info:")
        # Get memory info
        w32phy_mem = self.winloc.Win32_PhysicalMemory()
        if ram_arg:
            # If call with two arguments [--ram 1]
            if ram_num:
                for ram_number, i in enumerate(w32phy_mem):
                    if ram_num == ram_number:
                        # Print memory bank location, capacity, memory name, manufacturer,
                        # memory speed, serial number.
                        mem_locate = i.DeviceLocator
                        mem_cap_mb = int(i.Capacity) // (1024 * 1024)
                        mem_name = i.Name
                        mem_manufac = i.Manufacturer
                        mem_speed = str(i.Speed)
                        mem_sn = i.SerialNumber
                        print(str(ram_number) + " : " + mem_name + " " + mem_manufac + " " + mem_locate +
                              " Capacity: " + str(mem_cap_mb) + "MB" + "\nMemorySpeed: " + mem_speed +
                              "\nMemorySerialNumber: " + mem_sn)
            else:
                mem_total_mb = 0
                for ram_number, i in enumerate(w32phy_mem):
                    # Print memory bank location, capacity, memory name, manufacturer, total memory in MB.
                    mem_locate = i.DeviceLocator
                    mem_cap_mb = int(i.Capacity) // (1024 * 1024)
                    mem_name = i.Name
                    mem_manufac = i.Manufacturer
                    mem_total_mb += mem_cap_mb
                    print(str(ram_number) + " : " + mem_name + " " + mem_manufac + " " + mem_locate +
                          " Capacity: " + str(mem_cap_mb) + "MB")
                    # Real time memory usage
                w32mem_rt = self.winloc.Win32_PerfFormattedData_PerfOS_Memory()
                for mrtu in w32mem_rt:
                    # Print available memory, use memory in percent, use memory in MB.
                    memavail_mb = mrtu.AvailbleMBytes
                    memuse_per = mrtu.PercentCommittedBytesInUse
                    memuse_mb = mem_total_mb - memavail_mb
                    print("MemAvailMB: " + memavail_mb + "MB" + " : MemUseMB: " +
                          memuse_mb + "MB" + " : MemUsePercent: " + memuse_per + "%")
        else:
            for ram_number, i in enumerate(w32phy_mem):
                # Print memory bank location and capacity.
                mem_locate = i.DeviceLocator
                mem_cap_mb = int(i.Capacity) // (1024 * 1024)
                print(str(ram_number) + " : " +
                      mem_locate + str(mem_cap_mb) + "MB")

    def disk(self, disk_arg=None, disk_num=None, part_num=None):
        print("\nDisk info:")
        # Get disk info
        w32disk = self.winloc.Win32_DiskDrive()
        # If add one argument '--disk'
        if disk_arg:
            # If add three argument, e.g. '--disk 1 1'
            if disk_num and part_num:
                w32diskpart = self.winloc.Win32_DiskPartition()
                for i in w32diskpart:
                    if disk_num == i.DiskIndex and part_num == i.Index:
                        # Print part name, partition id in system, size in MB.
                        part_name = i.Name
                        part_id = i.DeviceID
                        part_size_mb = int(i.Size) // (1024 * 1024)
                        print(part_name + "\n" + part_id + "\n" +
                              "PartitionSize: " + part_size_mb + "MB")
            else:
                for i in w32disk:
                    # Print disk number, description, model, serial number,
                    # disk size, partitions count.
                    disk_desc = i.Description
                    disk_model = i.Model
                    disk_part = i.Partitions
                    disk_size_mb = int(i.Size) // (1024 * 1024)
                    disk_number = i.Index
                    disk_sn = i.SerialNumber
                    print(str(disk_number) + " : " + disk_desc + " " + disk_model + "\nSerialNumber: " + disk_sn +
                          "\nDiskSize: " + str(disk_size_mb) + "MB" + "\nDiskPartitions: " + str(disk_part))
        else:
            for i in w32disk:
                # Print disk number and model.
                disk_number = i.Index
                disk_model = i.Model
                print(str(disk_number) + " : Model: " + disk_model)


class LinuxOS(abc_class.AbstractBaseOS):

    def hostname(self):
        pass

    def cpu(self):
        pass

    def ram(self):
        pass

    def disk(self):
        pass

    # # get processors info from /proc/cpuinfo
    # print("Processors info:")
    # with open("/proc/cpuinfo", "r") as f:
    #     info = f.readlines()

    # cpuinfo = [x.strip().split(":")[1] for x in info if "model name" in x]
    # for index, item in enumerate(cpuinfo):
    #     print(str(index) + ":" + item)

    # # get ram info from /proc/meminfo
    # print("\nMemory info:")
    # gchar_ram = ["MemTotal", "MemFree", "MemAvailable"]
    # with open("/proc/meminfo", "r") as f:
    #     info = f.readlines()

    # raminfo = [x.strip().split(":") for x in info]
    # for i, x in raminfo:
    #     if i in gchar_ram:
    #         print(i + ":" + x)
