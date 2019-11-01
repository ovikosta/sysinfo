from setuptools import setup

setup(name="sysinfo",
      version="0.1",
      description="Print system information(cpu, disk, ram) Windows/Linux.",
      url="https://github.com/ovikosta/sysinfo",
      author="OviKosta",
      author_email="ovikosta@gmail.com",
      license="MIT",
      packages=["sysinfo"],
      zip_safe=False,
      scripts=["bin/getsysinfo"])
