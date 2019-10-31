import os
import wmi

import abc_class


class WindowsOS(abc_class.AbstractBaseOS):

    def __init__(self):
        # Connect to WMI local machine
        self.winloc = wmi.WMI()

    def cpu(self, cpu_arg=None, cpu_num=None):
        print("Processor info:")
        # Get general system info
        w32compsystem = self.winloc.Win32_ComputerSystem()
        for i in w32compsystem:
            cpu_num = i.NumberOfProcessors
            hostname = i.DNSHostName
        print("Hostname: " + hostname)

        # Get processor info
        w32processor = self.winloc.Win32_Processor()
        for i in w32processor:
            cpu_name = i.Name
            cpu_count_core = i.NumberOfCores
            print(cpu_name + "\n" + "CpuNumber: " +
                  str(cpu_num) + "\n" "CoreCount: " + str(cpu_count_core))

        if cpu_arg and cpu_num:
            pass
