# -*- coding: utf-8 -*-



import os, botocore
from awssettings import aws, others, regions_list
from database2 import createDB, postgresql
from localip import LocalIp
from agrosettings import sendMessage

def menu():

    print(  f'Access Key: {aws_data[0][1]}',
            f'Secret Access Key: {aws_data[0][2]}',
            f'Region: {aws_data[0][5]}',
            '---------------------------',
            '1 -> Выпустить IP-адрес',
            '2 -> Удалить IP-адрес',
            '3 -> Привязать IP-адрес',
            '4 -> Отвязать IP-адрес',
            '5 -> Проверить IP-адрес',
            '6 -> Список IP-адресов',
            '---------------------------',
            '7 -> Создать машину',
            '8 -> Удалить машину',
            '9 -> Запустить машину',
            '10 -> Остановить машину',
            '11 -> Перезапустить машину',
            '12 -> Список машин',
            '---------------------------',
            '13 -> Настройка',
            '14 -> Настройка агро поиска',
            '15 -> Настройка подсетей',
            '16 -> Настройка региона',
            '17 -> Запустить агро поиск',
            '---------------------------',
            '0 -> Выход',
            '---------------------------',
            sep='\n', end='\n')

def __checkIp(ip):

    import time, socket

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

        if timelate - timenow > 20:
            
            return True
        
        else:

            return False

createDB()
__other_setting = others()

try:
    __other_setting.verif()
except:
    print("Поверьте сеть на наличие VPN")
    exit()

if len(postgresql.getdata('mainsetting', 'default')) == 0:
    
    __other_setting.putsetting()
    
aws_data = postgresql.getdata('mainsetting', 'default')

while True:

    try:
        
        os.system('cls')
        
        menu()
        choose_menu = int(input('--> '))

        os.system('cls')

        if choose_menu == 1:

            __aws_setting = aws(aws_data[0][1], aws_data[0][2], aws_data[0][5])
            print(__aws_setting.allocateip())

        elif choose_menu == 2:

            __aws_setting = aws(aws_data[0][1], aws_data[0][2], aws_data[0][5])
            __aws_setting.delip()

        elif choose_menu == 3:

            __aws_setting = aws(aws_data[0][1], aws_data[0][2], aws_data[0][5])
            __aws_setting.associateip()

        elif choose_menu == 4:

            __aws_setting = aws(aws_data[0][1], aws_data[0][2], aws_data[0][5])
            __aws_setting.disassociateip()

        elif choose_menu == 5:

            ip_address = input("Введите IP-адрес: ")
            
            if __checkIp(ip_address) == True:

                print(f'IP-адрес {ip_address} работает')

            else:

                print(f'IP-адрес {ip_address} не работает')

        elif choose_menu == 6:


            aws_setting = aws(aws_data[0][1], aws_data[0][2], aws_data[0][5])
            count = 1

            ips = aws_setting.getip()

            for ip in ips:

                print(f'{count}. {ip}')
                count += 1

        elif choose_menu == 7:

            __aws_setting = aws(aws_data[0][1], aws_data[0][2], aws_data[0][5])
            __aws_setting.createInstance()

        elif choose_menu == 8:

            __aws_setting = aws(aws_data[0][1], aws_data[0][2], aws_data[0][5])
            __aws_setting.terminateInstances()

        elif choose_menu == 9:

            __aws_setting = aws(aws_data[0][1], aws_data[0][2], aws_data[0][5])
            __aws_setting.startInstance()

        elif choose_menu == 10:

            __aws_setting = aws(aws_data[0][1], aws_data[0][2], aws_data[0][5])
            __aws_setting.stopInstance()

        elif choose_menu == 11:

            __aws_setting = aws(aws_data[0][1], aws_data[0][2], aws_data[0][5])
            __aws_setting.rebootInstance()

        elif choose_menu == 12:

            __aws_setting = aws(aws_data[0][1], aws_data[0][2], aws_data[0][5])
            count = 1

            for instance in __aws_setting.instanceslist():

                print(
                    f'Instance №{count}',
                    f'Instance Name: {instance[1]}',
                    f'Instance ID: {instance[2]}',
                    f'Instance Public IP: {instance[3]}',
                    f'Instance Private IP: {instance[4]}',
                    f'Instance Subnet ID: {instance[5]}',
                    f'Instance Security Group ID: {instance[6]}',
                    f'Instance Key Pair: {instance[7]}',
                    f'Instance State: {instance[8]}',
                    sep='\n', end='\n'
                    )

                count += 1

        elif choose_menu == 13:

            __other_setting.updatesetting()
            aws_data = postgresql.getdata('mainsetting', 'default')

        elif choose_menu == 14:

            __other_setting.agrosetting()

        elif choose_menu == 15:
    
            print(
                '1. Работа с белыми подсетями',
                '2. Работа с черными подсетями',
                sep='\n', end='\n'
            )

            __choose_set_main_menu = int(input('--> '))

            os.system('cls')

            if __choose_set_main_menu == 1:

                print(
                    '1. Добавить подсеть',
                    '2. Удалить подсеть',
                    '3. Просмотреть все подсети',
                    sep='\n', end='\n'
                )

                __choose_white_set_menu = int(input('--> '))

                if __choose_white_set_menu == 1:

                    os.system('cls')
                    
                    __other_setting.putwhiteset(input('Введите значение: '))

                elif __choose_white_set_menu == 2:

                    os.system('cls')

                    for subset in __other_setting.getwhitesubset():

                        print(subset)

                    __other_setting.deletewhiteset(input('Введите значение: '))

                elif __choose_white_set_menu == 3:

                    os.system('cls')

                    for subset in __other_setting.getwhitesubset():

                        print(subset)

            elif __choose_set_main_menu == 2:

                print(
                    '1. Добавить подсеть',
                    '2. Удалить подсеть',
                    '3. Просмотреть все подсети',
                    sep='\n', end='\n'
                )

                __choose_black_set_menu = int(input('--> '))

                if __choose_black_set_menu == 1:

                    __other_setting.putblockset(input('Введите значение: '))

                elif __choose_black_set_menu == 2:

                    for subset in __other_setting.getblocksubset():

                        print(subset)

                    __other_setting.deleteblockset(input('Введите значение: '))

                elif __choose_black_set_menu == 3:

                    for subset in __other_setting.getblocksubset():

                        print(subset)

        elif choose_menu == 16:

            print('1. Просмотр регионов',
                  '2. Добавить регион',
                  '3. Удалить регион',
                  sep='\n', end='\n')
            
            __choose_region_menu = int(input(">>> "))
            countRegion = 1

            if __choose_region_menu == 1:

                os.system('cls')

                for region in __other_setting.regionlist():

                    print(f'{countRegion}. {regions_list.get(region)}: {region}')
                    countRegion += 1

            elif __choose_region_menu == 2:
                
                os.system('cls')
                __other_setting.addregion(aws_data)

            elif __choose_region_menu == 3:

                os.system('cls')
                __other_setting.dropregion()

        elif choose_menu == 17:

            os.system('python agrosearch2.py')

        elif choose_menu == 18:

            other_settings_tools = ['1. Удалить VPC', '2. Удалить Security Group', '3. Удалить Subnet', '4. Удалить Key Pair']

            for setting in other_settings_tools:

                print(setting)

            __aws_setting = aws(aws_data[0][1], aws_data[0][2], aws_data[0][5])

            choose_stools = int(input('>> '))

            os.system('cls')

            if choose_stools == 1:

                __aws_setting.delete_vpc()

            elif choose_stools == 2:

                __aws_setting.delete_scgroup()

            elif choose_stools == 3:

                __aws_setting.delete_subnet()

            elif choose_stools == 4:

                __aws_setting.delete_keypair()

        elif choose_menu == 0:

            os.system('cls')
            break

        os.system('pause')
    
    except botocore.exceptions.ClientError as error:
        
        if error.response['Error']['Code'] == 'AuthFailure':
                
                print('Ваш аккаунт заблокирован или токены введены неверно')
                os.system('pause')

        elif error.response['Error']['Code'] == 'Blocked':

            print('Ваш аккаунт был заблокирован. Возможности были ограничены со стороны Amazon')
            os.system('pause')

        else:
                print('Возникла ошибка, обратитесь к админу')
                os.system('pause')

    except Exception as error: 

        if "Invalid literal" in str(error):
                
            sendMessage("xxx", "xxx", str(error))
            print("Внутрення ошибка скрипта. Обратитесь к администратору")
            os.system('pause')
    