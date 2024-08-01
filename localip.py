import os

os.system('ipconfig > local_ip.txt')

with open('local_ip.txt', 'r') as f:
    lines = f.readlines()

def YourLocalIp():

    count = len(lines)
    local_ip = ''

    for i in range(count):
        if "IPv4" in lines[i]:
            local_ip = lines[i]
    mas = local_ip.split(' ')

    count = len(mas)

    for i in range(count):
        if "192.168" in mas[i]:
            local_ip = mas[i]

    local_ip = local_ip.split('\n')[0]

    return local_ip

os.remove('local_ip.txt')

LocalIp = YourLocalIp()