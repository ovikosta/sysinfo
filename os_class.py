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

    def cpu(self, cpu_arg=None, cpu_num=None, core_num=None):
        print("Processor info:")
        # Get general system info for number of processors
        w32processor = self.winloc.Win32_Processor()
        if cpu_arg:
            if cpu_num and core_num:
                #Realtime info for core
                pass
            for cpu_number, i in enumerate(w32processor):
                cpu_name = i.Name
                cpu_count_core = i.NumberOfCores
                #Add socket info
                print(cpu_name + "\n" + "CpuNumber: " +
                      str(cpu_number) + "\n" "CoreCount: " + str(cpu_count_core))
                print("\nIf you show realtime info about processor \
                         use time, add arguments number of cpu and core.\
                             For example '--cpu 1 1'")
        else:
            for cpu_number, i in w32processor:
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
                        mem_locate = i.DeviceLocator
                        mem_cap_mb = int(i.Capacity) // (1024 * 1024)
                        mem_name = i.Name
                        mem_manufac = i.Manufacturer
                        print(str(ram_number) + " : " + mem_name + " " + mem_manufac + " " + mem_locate +
                                " Capacity: " + str(mem_cap_mb) + "MB")
            for ram_number, i in enumerate(w32phy_mem):
                mem_locate = i.DeviceLocator
                mem_cap_mb = int(i.Capacity) // (1024 * 1024)
                mem_name = i.Name
                mem_manufac = i.Manufacturer
                print(str(ram_number) + " : " + mem_name + " " + mem_manufac + " " + mem_locate +
                        " Capacity: " + str(mem_cap_mb) + "MB")
        else:
            for ram_number, i in enumerate(w32phy_mem):
                mem_locate = i.DeviceLocator
                mem_cap_mb = int(i.Capacity) // (1024 * 1024)
                print(str(ram_number) + " : " + mem_locate + str(mem_cap_mb) + "MB")

    def disk(self, disk_arg=None, disk_num=None, part_num=None):
        print("\nDisk info:")
        # Get disk info
        w32disk = self.winloc.Win32_DiskDrive()
        if disk_arg:
            if disk_num and part_num:
                for disk_number, i in enumerate(w32disk):
                    if disk_num == disk_number and part_num == i.Partitions:
                        pass
            for disk_number, i in enumerate(w32disk):
                disk_desc = i.Description
                disk_model = i.Model
                disk_part = i.Partitions
                disk_size_mb = int(i.Size) // (1024 * 1024)
                print(str(disk_number) + " : " + disk_desc + " " + disk_model + "\nDiskSize: " +
                        str(disk_size_mb) + "MB" + "\nDiskPartitions: " + str(disk_part))
        else:
            pass
