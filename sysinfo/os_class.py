import os

import abc_class

if os.uname() == "Windows":
    import wmi


class WindowsOS(abc_class.AbstractBaseOS):

    def __init__(self):
        # Connect to WMI local machine
        self.winloc = wmi.WMI()

    def hostname(self):
        # Get hostname
        w32compsystem = self.winloc.Win32_ComputerSystem()
        for i in w32compsystem:
            hostname = i.DNSHostName
        print("Hostname: {:s}".format(hostname))

    def cpu(self, cpu_arg=None, core_num=None):
        print("Processor info:")
        # Get general system info for number of processors
        w32processor = self.winloc.Win32_Processor()
        if cpu_arg:
            if core_num:
                # Realtime info for core
                wql = "SELECT * FROM Win32_PerfFormattedData_PerfOS_Processor WHERE Name <> '_Total'"
                for i in self.winloc.query(wql):
                    if core_num == int(i.Name):
                        # Print core name, load and idle in precent for core.
                        core_name = i.Name
                        core_usage = i.PercentProcessorTime
                        core_idle = i.PercentIdleTime
                        print("Core: {:s} PercentUsage: {:s}% PercentIdle: {:s}%".format(
                            core_name, core_usage, core_idle))
                        break
                else:
                    print("CoreNum {:d} does not exist!".format(core_num))
            else:
                for cpu_number, i in enumerate(w32processor):
                    # Print processors name, count core, load in percentage and socket.
                    cpu_name = i.Name
                    cpu_count_core = i.NumberOfCores
                    cpu_usage = i.LoadPercentage
                    cpu_socket = i.SocketDesignation
                    print("{:s}\nSocket: {:s} CpuNumber: {:d}\nCoreCount: {:d}\nPercentLoad: {:d}%".format(
                        cpu_name, cpu_socket, cpu_number, cpu_count_core, cpu_usage))
                print("\nIf you show realtime info about processor use time, add arguments number of the core. For example '--cpu 1'")
        else:
            for cpu_number, i in enumerate(w32processor):
                # Print cpu count and name processors.
                cpu_name = i.Name
                print("{:d} : {:s}".format(cpu_number, cpu_name))
            print("\nYou can show more information about processors, add arguments '--cpu'\n ----------------")

    def ram(self, ram_arg=None, ram_num=None):
        print("\nMemory info:")
        # Get memory info
        w32phy_mem = self.winloc.Win32_PhysicalMemory()
        if ram_arg:
            # If call with two arguments [--ram 1]
            if isinstance(ram_num, int):
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
                        print("{:d} : {:s} {:s} {:s} Capacity: {:d}MB\nMemorySpeed: {:s}\nMemorySerialNumber: {:s}".format(
                            ram_number, mem_name, mem_manufac, mem_locate, mem_cap_mb, mem_speed, mem_sn))
                        break
                else:
                    print("RamNumber: {:d} does not exist!".format(ram_num))
            else:
                mem_total_mb = 0
                for ram_number, i in enumerate(w32phy_mem):
                    # Print memory bank location, capacity, memory name, manufacturer, total memory in MB.
                    mem_locate = i.DeviceLocator
                    mem_cap_mb = int(i.Capacity) // (1024 * 1024)
                    mem_name = i.Name
                    mem_manufac = i.Manufacturer
                    mem_total_mb += mem_cap_mb
                    print("{:d} : {:s} {:s} {:s} Capacity: {:d}MB".format(
                        ram_number, mem_name, mem_manufac, mem_locate, mem_cap_mb))
                    # Real time memory usage
                w32mem_rt = self.winloc.Win32_PerfFormattedData_PerfOS_Memory()
                for mrtu in w32mem_rt:
                    # Print available memory, use memory in percent, use memory in MB.
                    memavail_mb = mrtu.AvailableMBytes
                    memuse_per = str(mrtu.PercentCommittedBytesInUse)
                    memuse_mb = str(mem_total_mb - int(memavail_mb))
                    print("MemAvailMB: {:s}MB : MemUseMB: {:s}MB : MemUsePercent: {:s}%".format(
                        memavail_mb, memuse_mb, memuse_per))
        else:
            for ram_number, i in enumerate(w32phy_mem):
                # Print memory bank location and capacity.
                mem_locate = i.DeviceLocator
                mem_cap_mb = int(i.Capacity) // (1024 * 1024)
                print("{:d} : {:s} {:d}MB".format(ram_number, mem_locate, mem_cap_mb))
            print("\nYou can show more information about ram, add arguments '--ram'\n ----------------")

    def disk(self, disk_arg=None, disk_num=None, part_num=None):
        print("\nDisk info:")
        # Get disk info
        w32disk = self.winloc.Win32_DiskDrive()
        # If add one argument '--disk'
        if disk_arg:
            # If add three argument, e.g. '--disk 1 1'
            if isinstance(disk_num, int) and isinstance(part_num, int):
                w32diskpart = self.winloc.Win32_DiskPartition()
                for i in w32diskpart:
                    if disk_num == int(i.DiskIndex) and part_num == int(i.Index):
                        # Print part name, partition id in system, size in MB.
                        part_name = i.Name
                        part_id = i.DeviceID
                        part_size_mb = int(i.Size) // (1024 * 1024)
                        print("{:s}\n{:s}\nPartitionSize: {:d}MB".format(part_name, part_id, part_size_mb))
                        break
                else:
                    print("DiskNumber {:d} or PartNumber {:d} does not exist!".format(disk_num, part_num))
            # If add two arguments, e.g. '--disk 1'
            elif isinstance(disk_num, int):
                for i in w32disk:
                    # Print disk number, description, model, serial number,
                    # disk size, partitions count.
                    if disk_num == i.Index:
                        disk_desc = i.Description
                        disk_model = i.Model
                        disk_part = i.Partitions
                        disk_size_mb = int(i.Size) // (1024 * 1024)
                        disk_number = i.Index
                        disk_sn = i.SerialNumber
                        print("{:d} : {:s} {:s}\nSerialNumber: {:s}\nDiskSize: {:d}MB\nDiskPartitions: {:d}\n".format(
                            disk_number, disk_desc, disk_model, disk_sn, disk_size_mb, disk_part))
                        break
            else:
                for i in w32disk:
                    # Print disk number, description, model, serial number,
                    # disk size, partitions count for all disk in system.
                    disk_desc = i.Description
                    disk_model = i.Model
                    disk_part = i.Partitions
                    disk_size_mb = int(i.Size) // (1024 * 1024)
                    disk_number = i.Index
                    disk_sn = i.SerialNumber
                    print("{:d} : {:s} {:s}\nSerialNumber: {:s}\nDiskSize: {:d}MB\nDiskPartitions: {:d}\n".format(
                        disk_number, disk_desc, disk_model, disk_sn, disk_size_mb, disk_part))
        else:
            for i in w32disk:
                # Print disk number and model.
                disk_number = i.Index
                disk_model = i.Model
                print("{:d} : Model: {:s}".format(disk_number, disk_model))
            print("\nYou can show more information about disk, add arguments '--disk'\n ----------------")


class LinuxOS(abc_class.AbstractBaseOS):


    def hostname(self):
        print(os.uname().nodename)

    def cpu(self, cpu_arg=None, core_num=None):
        # Get processors info from /proc/cpuinfo
        print("Processors info:")
        with open("/proc/cpuinfo", "r") as f:
            cpu_file = f.readlines()
        cpuinfo_list = [x.strip().split(":") for x in cpu_file if not x.isspace()]
        cpuinfo_dos = {x[0].strip():set() for x in cpuinfo_list}
        # Add element to dict of set
        for i in cpuinfo_list:
            cpuinfo_dos[i[0].strip()].add(i[1].strip())
        # Check in system with two processors!!!
        if len(cpuinfo_dos["physical id"]) > 1:
            for phy_id in cpuinfo_dos["physical id"]:
                if len(cpuinfo_dos["model name"]) > 1:
                    cpu_model = cpuinfo_dos["model name"].pop()
                elif len(cpuinfo_dos["model name"]) != 0:
                    cpu_model = cpuinfo_dos["model name"].pop()
                print("{:d} : {:s}\nCoreCount: {:d}".format(phy_id, cpu_model, int(cpuinfo_dos["cpu cores"])))
        else:
            print("{:s} : {:s}\nCoreCount: {:s}".format(
                cpuinfo_dos["physical id"].pop(), cpuinfo_dos["model name"].pop(),
                cpuinfo_dos["cpu cores"].pop()))
            print("\nYou can show more information about processors, add arguments '--cpu'\n ----------------")


        # print("{:s}\nSocket: {:s} CpuNumber: {:d}\nCoreCount: {:d}\nPercentLoad: {:d}%".format(
        #                 cpu_name, cpu_socket, cpu_number, cpu_count_core, cpu_usage))
        #         print("\nIf you show realtime info about processor use time, add arguments number of the core. For example '--cpu 1'")



    def ram(self, ram_arg=None, ram_num=None):
        pass

    def disk(self, disk_arg=None, disk_num=None, part_num=None):
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
