#!/bin/env python3
from abc import ABC, abstractmethod, abstractproperty


class AbstractBaseOS(ABC):

    # Get hostname
    @abstractmethod
    def hostname(self):
        pass

    # Get CPU info from OS
    @abstractmethod
    def cpu(self):
        pass

    # Get RAM info from OS
    @abstractmethod
    def ram(self):
        pass

    # Get DISK info from OS
    @abstractmethod
    def disk(self):
        pass
