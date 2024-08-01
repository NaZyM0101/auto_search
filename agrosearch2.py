# -*- coding: utf-8 -*-

from agrosettings import aws, sendMessage, countDown
from awssettings import others
import os, time
from localip import LocalIp
import socket
from threading import Thread
from database2 import postgresql
from database2 import blockIpList, workIpList

def __checkIp(ip):

    juice = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    juice.bind((LocalIp, 0))
    timenow = time.time()

    try:

        juice.connect((ip, 22))
        juice.close()

        return True
    
    except:

        juice.close()
        timelate = time.time()

        period = timelate - timenow   

        if period > 21 and period < 22:
            
            return True
        
        elif period > 23:

            print("Нестабильная сеть")
            return __checkIp(ip)
        
        elif period < 20.9:

            return False


def __startSearch(account_name, access_key, secret_key, region, ip_count):

    awsdata = aws(access_key, secret_key, region)
    work_ip_list = []

    while True:

        for ip in range(5 - len(awsdata.getip())):
            
            while True:

                try:

                    awsdata.allocateip()
                    break

                except:
                    pass

        ip_list = awsdata.getip()

        for ip in ip_list:

            if ip in blockIpList():

                ip_count[2] += 1
                ip_count[1] += 1
                awsdata.delip(awsdata.getip().get(ip))
                continue

            elif ip in workIpList():

                if not(ip in work_ip_list):

                    work_ip_list.append(ip)

                continue
            
            else:

                ip_count[2] += 1
                
                if __searchwithblackset in ['Да', '1', 'да']:

                    for subset in other_setting.getblocksubset():

                        if ip.startswith(subset):

                            other_setting.putblockip(f"{ip}")

                if __searchwithwhiteset in ['Да', '1', 'да']:
                    
                    for subset in other_setting.getwhitesubset():

                        if ip.startswith(subset):

                            ip_count[0] += 1
                            other_setting.putworkip(f"{ip}")
                            message = f'Найден рабочий IP-адрес: {ip}\nРегион: {region}\nАккаунт: {account_name}\nAccessKey ID: {access_key}\nSecret AccessKey: {secret_key}'
                            sendMessage(aws_data[0][4], aws_data[0][3], message)
                            break

                    if not(ip in workIpList()):

                        awsdata.delip(awsdata.getip().get(ip))

                elif __checkIp(ip) == True:

                    ip_count[0] += 1
                    other_setting.putworkip(f"{ip}")
                    message = f'Найден рабочий IP-адрес: {ip}\nРегион: {region}\nАккаунт: {account_name}\nAccessKey ID: {access_key}\nSecret AccessKey: {secret_key}'
                    sendMessage(aws_data[0][4], aws_data[0][3], message)

                else:

                    ip_count[1] += 1
                    other_setting.putblockip(ip)
                    awsdata.delip(awsdata.getip().get(ip))
                            

        if len(work_ip_list) == 5:

            finish_message = (f"Поиск успешно заверешен на регионе {region}\nДанные от аккаунта: {access_key}, {secret_key}")
            sendMessage(aws_data[0][4], aws_data[0][3], finish_message)
            break

        time.sleep(60)

aws_data = postgresql.getdata('mainsetting', 'default')

other_setting = others()
time_sleep_list = ['1. 5 минут', '2. 10 минут', '3. 30 минут', '4. 1 час', '5. 3 часа', '6. 6 часов', '7. 12 часов', '8. 1 день']
ip_count = [0, 0, 0]
connection = [0]

try:
    other_setting.verif()
except:
    print("Поверьте сеть на наличие VPN")
    exit()

if len(postgresql.getdata('agrosettings', 'default')) == 0:
    
    other_setting.putagrosetting()

for times in time_sleep_list:
    print(times)

time_sleep = int(input('--> '))

if len(other_setting.getwhitesubset()) != 0:
    __searchwithwhiteset = input('Включить поиск по белым подсетям?\n')
else:
    __searchwithwhiteset = 0

if len(other_setting.getblocksubset()) != 0:
    __searchwithblackset = input('Включить исключение черных подсетей?\n')
else:
    __searchwithblackset = 0

accounts = postgresql.getdata('agrosettings', 'default')

os.system('cls')
regions = 0

for account in accounts:

    sendMessage(aws_data[0][4], aws_data[0][3], f'Автопоиск успешно запущен на аккаунте {account[1]}')

    for region in other_setting.regionlist():

        try:

            Thread(target=__startSearch, args=(account[1], account[2], account[3], region, ip_count)).start()
            regions += 1

        except:

            print(f"При запуске автопоиска на регионе {region} возникла ошибка\nОбратитесь к создателю")

    print(f"\033[32mАвтопоиск успешно запущен на аккаунте {account[1]} и на {len(other_setting.regionlist())} регионах\033[0m")

countDown(time_sleep, ip_count, regions)


