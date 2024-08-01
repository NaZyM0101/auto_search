import os

__requirements = ["wmi", "py-cpuinfo", "psycopg2", "psutil", "requests", "pyarmor"]

for __requirement in __requirements:
    os.system(f"pip install {__requirement} -q")