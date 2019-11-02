#!/bin/env python3

import sys
import platform
import argparse

from os_class import WindowsOS

# view list disk with size
# info about cpu and ram with general characteristics

def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("device", nargs="?")
    parser.add_argument("dev_num1", nargs="?", type=int)
    parser.add_argument("dev_num2", nargs="?", type=int)
    return parser

if __name__ == "__main__":
    parser = create_arg_parser()
    namespace = parser.parse_args(sys.argv[1:])

    if platform.system() == "Windows":
        windows = WindowsOS()
        if namespace.device == "--cpu":
            windows.cpu(cpu_arg=namespace.device, core_num=namespace.dev_num1)
        elif namespace.device:
            pass
    # if platform.system() == "Linux":
    #     pass

    # if platform.system() == "Windows":
    #     windows = WindowsOS()
    #     if sys.argv[1] and sys.argv == "--cpu":
    #         try:
    #             if sys.argv[2] and isinstance(sys.argv[2], int):
    #                 windows.cpu(cpu_arg="--cpu", core_num=sys.argv[2])
    #         except Exception as e:
    #             print(e)
    #         else:
    #             windows.cpu(cpu_arg="--cpu")
        # windows.hostname()
        # print(sys.argv[1])

        # windows.ram(ram_arg="--ram", ram_num="1")
        # windows.disk(disk_arg="--disk", disk_num="1", part_num="0")
