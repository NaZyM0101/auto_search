# -*- coding: utf-8 -*-

import boto3
from localip import LocalIp
import os
from database2 import datasetting

class aws:

    # Подключение 

    def __init__(self, access_key, secret_key, region):

        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region

        session = boto3.session.Session(aws_access_key_id=access_key, aws_secret_access_key=secret_key,region_name=region)
        self.ec2 = session.client('ec2')

    # Работа с IP-адресом

    def getip(self):

        ipinf = {}

        response = self.ec2.describe_addresses()

        for address in response['Addresses']:
            
            elastic_ip = address['PublicIp']
            elastic_id = address['AllocationId']

            ipinf.update({elastic_ip: elastic_id})
            
        return ipinf

    def delip(self):

        count, ip_list = 1, []
        ips = self.getip()

        os.system('cls')

        for ip in ips:

            print(f'{count}. {ip}')
            count += 1
            ip_list.append(ips.get(ip))

        ip_number = int(input("Введите номер IP-адреса: "))

        self.ec2.release_address(AllocationId = ip_list[ip_number - 1])

    def allocateip(self):

        response = self.ec2.allocate_address(Domain='vpc')

        return response['PublicIp']

    def associateip(self):

        count = 1
        ip_list = []

        os.system('cls')

        for ip in self.getip():

            print(f'{count}. {ip}')
            count += 1
            ip_list.append(ip)

        ip_number = int(input("Введите номер IP-адреса: "))

        os.system('cls')

        count = 1

        for instance in self.instanceslist():

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
            
        instance_count = int(input('Введите номер машины: '))

        self.ec2.associate_address(InstanceId = self.instanceslist()[instance_count - 1][2], PublicIp = ip_list[ip_number - 1])

    def disassociateip(self):

        count = 1
        association_id_list = []

        os.system('cls')

        response = self.ec2.describe_addresses()

        for address in response['Addresses']:
            print(f'{count}. Public IP:', address['PublicIp'])
            association_id_list.append(address.get('AssociationId'))
            count += 1

        ip_number = int(input("Введите номер IP-адреса: "))

        os.system('cls')

        self.ec2.disassociate_address(AssociationId=association_id_list[ip_number-1])
        
    # Дополнительные настройки

    def delete_vpc(self):
    
        vpc_list = []

        vpcs = self.ec2.describe_vpcs()
        for vpc in vpcs['Vpcs']:
            print('VPC ID:', vpc['VpcId'])
            vpc_list.append(vpc['VpcId'])

        print("\nУдалить все(-1)")
        choose = int(input('>> '))
        if choose == -1:
            for vpcs in vpc_list:
                try:
                    self.ec2.delete_vpc(VpcId=vpcs)
                except:
                    print("Возможно данный элемент используется")
        else:
            try:
                self.ec2.delete_vpc(VpcId=vpc_list[choose-1])
            except:
                print("Возможно данный элемент используется")

    def delete_scgroup(self):
    
        scgroup_list = []

        security_groups = self.ec2.describe_security_groups()
        for sg in security_groups['SecurityGroups']:
            print('Security Group ID:', sg['GroupId'])
            scgroup_list.append(sg['GroupId'])
            
        print("\nУдалить все(-1)")
        choose = int(input('>> '))
        if choose == -1:
            for scgroup in scgroup_list:
                try:
                    self.ec2.delete_security_group(GroupId=scgroup)
                except:
                    print("Возможно данный элемент используется")
        else:
            try:
                self.ec2.delete_security_group(GroupId=scgroup_list[choose-1])
            except:
                print("Возможно данный элемент используется")

    def delete_keypair(self):

        key_pair_list = []

        key_pairs = self.ec2.describe_key_pairs()
        for key_pair in key_pairs['KeyPairs']:
            print('Key Pair Name:', key_pair['KeyName'])
            key_pair_list.append(key_pair['KeyName'])

        print("\nУдалить все(-1)")
        choose = int(input('>> '))
        if choose == -1:
            for key_pair in key_pair_list:
                try:
                    self.ec2.delete_key_pair(KeyName=key_pair)
                except:
                    print("Возможно данный элемент используется")
        else:
            try:
                self.ec2.delete_key_pair(KeyName=key_pair_list[choose-1])
            except:
                print("Возможно данный элемент используется")

    def delete_subnet(self):

        subnet_list = []

        subnets = self.ec2.describe_subnets()
        for subnet in subnets['Subnets']:
            print('Subnet ID:', subnet['SubnetId'])
            subnet_list.append(subnet['SubnetId'])

        print("\nУдалить все(-1)")
        choose = int(input('>> '))
        if choose == -1:
            for subnet in subnet_list:
                try:
                    self.ec2.delete_subnet(SubnetId=subnet)
                except:
                    pass
        else:
            try:
                self.ec2.delete_subnet(SubnetId=subnet_list[choose-1])
            except:
                print("Возможно данный элемент используется")

# Работа с машинами

    def instanceslist(self):

        instance_list = []
        count = 1

        instances = self.ec2.describe_instances()

        for instance in instances['Reservations']:
            instance_info = instance['Instances'][0]
            try:
                instance_name = instance_info['Tags'][0]['Value']
            except:
                instance_name = None

            instance_id = instance_info['InstanceId']
            try:
                instance_public_ip = instance_info['PublicIpAddress']
            except:
                instance_public_ip = None
            try:
                instance_private_ip = instance_info['PrivateIpAddress']
            except:
                instance_private_ip = None
            try:
                instance_subnet_id = instance_info['SubnetId']
            except:
                instance_subnet_id = None
            try:
                instance_sg_id = instance_info['SecurityGroups'][0]['GroupId']
            except:
                instance_sg_id = None
            try:
                instance_key = instance_info['KeyName']
            except:
                instance_key = None
            try:
                instance_state = instance_info['State']['Name']
            except:
                instance_state = None

            instance_list.append([count, instance_name, instance_id, instance_public_ip, instance_private_ip, instance_subnet_id, instance_sg_id, instance_key, instance_state])

        return instance_list
                
    def imagesID(self):

        response = self.ec2.describe_images(

            Filters=[
                {
                    'Name': 'name',
                    'Values': ['ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*']
                },
                {
                    'Name': 'architecture',
                    'Values': ['x86_64']
                },
                {
                    'Name': 'root-device-type',
                    'Values': ['ebs']
                },
            ],
            Owners=['xxx']  
        )

        image_id = response['Images'][0]['ImageId']

        return image_id
    
    def createSecurityGroup(self):
            
        vpc = self.ec2.create_vpc(CidrBlock='192.168.0.0/16')
        vpc_id = vpc['Vpc']['VpcId']

        self.ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsHostnames={'Value': True})
        self.ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsSupport={'Value': True})

        print(f'Ваш VPC Id: {vpc_id}')

        internet_gateway = self.ec2.create_internet_gateway()
        internet_gateway_id = internet_gateway['InternetGateway']['InternetGatewayId']

        print(f'Ваш Internet Gateway Id: {internet_gateway_id}')

        self.ec2.attach_internet_gateway(InternetGatewayId=internet_gateway_id, VpcId=vpc_id)

        response = self.ec2.describe_route_tables(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
        route_table_id = response['RouteTables'][0]['RouteTableId']
        self.ec2.create_route(RouteTableId=route_table_id, DestinationCidrBlock='0.0.0.0/0', GatewayId=internet_gateway_id)

        subnet = self.ec2.create_subnet(VpcId=vpc_id, CidrBlock='192.168.0.0/24', AvailabilityZone=f"{self.region}a")
        subnet_id = subnet['Subnet']['SubnetId']

        print(f'Ваш subnet: {subnet_id}')

        self.ec2.modify_subnet_attribute(
            MapPublicIpOnLaunch={
                'Value': True
            },
            SubnetId=subnet_id
        )

        security_group = self.ec2.create_security_group(
            GroupName='MySecurityGroup',
            Description='My Security Group with All Traffic',
            VpcId=vpc_id
        )

        security_group_id = security_group['GroupId']

        print(f'Успешно создан Security Group Id: {security_group_id}')

        self.ec2.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {
                    'IpProtocol': '-1',
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                }
            ]
        )

        sg_and_sn = [subnet_id, security_group_id]

        return sg_and_sn

    def createKeyPair(self):

        import random
        import string

        alphabet = string.ascii_lowercase
        new_key_name = ''.join(random.choice(alphabet) for _ in range(8))

        response = self.ec2.create_key_pair(KeyName=new_key_name)

        private_key = response['KeyMaterial']

        if not os.path.exists("Keys"):
            os.makedirs("Keys")

        with open(f"Keys/{new_key_name}.pem", 'w') as file:
            file.write(private_key)

        return new_key_name

    def createInstance(self):

        sg_and_sn = self.createSecurityGroup()
        instance_name = input("Введите имя машины: ")

        response = self.ec2.run_instances(
            ImageId=f'{self.imagesID()}',
            InstanceType='t2.micro',
            SubnetId=sg_and_sn[0],
            SecurityGroupIds=[sg_and_sn[1]],
            KeyName=self.createKeyPair(),
            MinCount=1,
            MaxCount=1,
            TagSpecifications=[{
                'ResourceType': 'instance',
                'Tags': [{
                'Key': 'Name',
                'Value': instance_name},]
                },]
            )
        
        instance = response['Instances'][0]
        instance_id = instance['InstanceId']
        instance_state = instance['State']['Name']
        print(f'Instance Id: {instance_id}')
        print(f'Instance State: {instance_state}')

    def rebootInstance(self):

        count = 1

        for instance in self.instanceslist():

            print(
                f'Instance №{count}',
                f'Instance ID: {instance[1]}',
                f'IP-address: {instance[2]}',
                f'Instance State: {instance[3]}',
                f'Instance Key: {instance[4]}', sep='\n', end='\n'
                )
            
            count += 1

        choose = int(input('Введите номер машины: '))

        self.ec2.reboot_instances(InstanceIds=[self.instanceslist()[choose-1][1]])
        
    def terminateInstances(self):

        count = 1

        for instance in self.instanceslist():

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

        choose = int(input('Введите номер машины: '))
            
        self.ec2.terminate_instances(InstanceIds=[self.instanceslist()[choose-1][2]])
         
    def stopInstance(self):

        count = 1

        for instance in self.instanceslist():

            print(
                f'Instance №{count}',
                f'Instance ID: {instance[1]}',
                f'IP-address: {instance[2]}',
                f'Instance State: {instance[3]}',
                f'Instance Key: {instance[4]}', sep='\n', end='\n'
                )
            
            count += 1

        choose = int(input('Введите номер машины: '))
                
        self.ec2.stop_instances(InstanceIds=[self.instanceslist()[choose-1][1]])

    def startInstance(self):
        
        count = 1

        for instance in self.instanceslist():

            print(
                f'Instance №{count}',
                f'Instance ID: {instance[1]}',
                f'IP-address: {instance[2]}',
                f'Instance State: {instance[3]}',
                f'Instance Key: {instance[4]}', sep='\n', end='\n'
                )
            
            count += 1

        choose = int(input('Введите номер машины: '))
        
        self.ec2.start_instances(InstanceIds=[self.instanceslist()[choose-1][1]])

class others:

    def __init__(self):
        
        self.database = datasetting('settings', 'localhost', '5432', 'postgres', 'postgres')

    # Основные настройки

    def putsetting(self):

        access_key = input('Введите Access Key: ')
        secret_key = input('Введите Secret Access Key: ')
        tgid = input('Введите Telegram ID: ')
        bottoken = input('Введите Telegram Bot Token: ')

        self.database.insertdata('mainsetting', 'id, accesskey, secretkey, tgid, bottoken, region', f"DEFAULT, '{access_key}', '{secret_key}', '{tgid}', '{bottoken}', 'eu-central-1'")

    def getsetting(self):

        aws_data = []

        os.system('cls')

        for datas in self.database.getdata('mainsetting', 'default'):

            for data in datas:

                aws_data.append(data)

            print(
            f'Access Key: {aws_data[1]}',
            f'Secret Access Key: {aws_data[2]}',
            f'Telegrad ID: {aws_data[3]}',
            f'Telegram Bot Token: {aws_data[4]}',
            f'Region: {aws_data[5]}',
            sep='\n', end='\n___________________________________________________________________\n'
            )

    def updatesetting(self):

        if len(self.database.getdata('mainsetting', 'default')) == 0:

            self.putsetting()

        self.getsetting()

        print(
            '1. Изменить Access Key',
            '2. Изменить Secret Access Key',
            '3. Изменить Telegram ID',
            '4. Изменить Telegram Bot Token',
            '5. Изменить регион',
            '___________________________________________________________________',
            'Примечание: Введите "0" для выхода',
            sep='\n', end='\n'
            )
        
        your_choose = int(input('# '))

        choose_list = ['accesskey', 'secretkey', 'tgid', 'bottoken', 'region']

        if your_choose != 0:

            os.system('cls')

            if choose_list[your_choose-1] == 'region':
                
                count = 1
                regions = []

                for region in regions_list:

                    print(f'{count}. {regions_list.get(region)}')
                    count += 1
                    regions.append(region)

                choose_region = int(input('# '))
                
                new_data = regions[choose_region - 1]

            else:

                new_data = input("Введите новое значение: ")

            self.database.updatedata('mainsetting', choose_list[your_choose - 1], f"{new_data}")
            
            return self.updatesetting()

        else:

            pass

    # Настройки агропоиска

    def getagrosetting(self):

        aws_data = []

        os.system('cls')

        for datas in self.database.getdata('agrosettings', 'default'):

            for data in datas:

                aws_data.append(data)

            print(
            f'Name: {aws_data[1]}',
            f'Access Key: {aws_data[2]}',
            f'Secret Access Key: {aws_data[3]}',
            f'Region: {", ".join(regions)}',
            sep='\n', end='\n___________________________________________________________________\n'
            )

            aws_data = []

    def putagrosetting(self):

        name = input('Введите пользовательское имя: ')
        access_key = input('Введите Access Key: ')
        secret_key = input('Введите Secret Access Key: ')
        
        self.database.insertdata('agrosettings', 'id, name, accesskey, secretkey', f"DEFAULT, '{name}', '{access_key}', '{secret_key}'")

    def dropagrosetting(self, drop_data):

        self.database.deldata('agrosettings', 'accesskey', f"{drop_data}")

    def updateagrosetting(self):

        print(
            '1. Изменить Access Key',
            '2. Изменить Secret Access Key',
            '3. Изменить имя аккаунта',
            sep='\n', end='\n'
        )

        choose_menu = int(input(">>> "))

        if choose_menu != 0:

            os.system('cls')
            self.getagrosetting()
            new_data = input('Введите новое значение: ')

            update_data = ['accesskey', 'secretkey', 'name']

            self.database.updatedata('agrosettings', update_data[choose_menu-1], new_data)

        else:

            exit()

    def agrosetting(self):

        if len(self.database.getdata('mainsetting', 'default')) == 0:

            self.putagrosetting()

        self.getagrosetting()

        print(
            '1. Добавить аккаунт',
            '2. Удалить аккаунт',
            '3. Изменить данные аккаунта',
            '___________________________________________________________________',
            'Примечание: Введите "0" для выхода',
            sep='\n', end='\n')
        
        your_choose = int(input('# '))

        if your_choose != 0:

            os.system('cls')

            if your_choose == 1:

                self.putagrosetting()

            elif your_choose == 2:

                self.getagrosetting()

                accesskey = input('Введите Access Key аккаунта: ')

                self.dropagrosetting(accesskey)

            elif your_choose == 3:

                self.updateagrosetting()

        else:

            pass

    # Отправка сообщение в бота Telegram

    def sendMessage(self, token, chat_id, text):

        import requests

        url = f"https://api.telegram.org/bot{token}/sendMessage"
        params = {"chat_id": chat_id, "text": text}
        response = requests.get(url, params=params)
        return response.json()

    # Характеристика компьютера

    def machineInformation(self, account_name):

        import psutil, wmi, cpuinfo

        w = wmi.WMI()
        model = w.Win32_ComputerSystem()[0].Model
        mac = w.Win32_NetworkAdapterConfiguration(IPEnabled = True)[0].MACAddress
        cpu = cpuinfo.get_cpu_info()
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        state_list = [
            f"Имя покупателя: {account_name}",
            f"Модель компьютера: {model}",
            f"MAC-адрес: {mac}",
            f"Модель ЦПУ: {cpu['brand_raw']}",
            f"Частота ЦПУ: {cpu['hz_actual']}",
            f"Количество ядер ЦПУ: {cpu['count']}",
            f"Общая ОЗУ: {(((ram.total//1024)//1024))//1024} Гбайт",
            f"Доступная ОЗУ: {((ram.available//1024)//1024)//1024} Гбайт",
            f"Используемая ОЗУ: {((ram.used//1024)//1024)//1024} Гбайт",
            f"Общая память: {((disk.total//1024)//1024)//1024} Гбайт",
            f"Свободная память: {((disk.free//1024)//1024)//1024} Гбайт",
            f"Используемая память: {((disk.used//1024)//1024)//1024} Гбайт"
            ]
        
        message = ''

        for mess in state_list:
            message += mess + '\n'

        token = 'xxx' # AAA TOKEN
        chat_id = 'xxx' # AAA CHAT_ID

        self.sendMessage(token, chat_id, message)

    # Разрешение на использование 

    def verif(self):

        import psycopg2, uuid

        conn = psycopg2.connect(dbname='accountdata',
                    user = 'xxx', # AAA USER
                    password = 'xxx', # AAA PASSWORD
                    host = 'xxx', # AAA HOST
                    port = '5432')
        
        token = 'xxx' # AAA TOKEN
        chat_id = 'xxx' # AAA CHAT_ID
        cursor = conn.cursor()

        if len(self.database.getdata('accountdata', 'default')) <= 0:

            mac_uuid = str(uuid.uuid1()).title()
            login = input('Введите имя пользователя: ')
            password = input('Введите пароль: ')
            print(f'Ваш ID: {mac_uuid}')

            message = f'Новый пользователь: {login}, {mac_uuid}'

            self.sendMessage(token, chat_id, message)

            print('Запросите доступ у администратора и после нажмите Enter')

            os.system('pause')
            cursor.execute('SELECT * FROM account')
            data = cursor.fetchall()

            if (login, password, mac_uuid) in data:

                self.database.insertdata('accountdata', 'id, login, password, uid', f"DEFAULT, '{login}', '{password}', '{mac_uuid}'")
        
                print('Доступ разрешён')
            
            else:

                print("Доступ запрещён")
                exit()

        cursor.execute('SELECT * FROM account')
        data = cursor.fetchall()

        if self.database.getdata('accountdata', '*') in data:

            return True

    # Работа с IP-адресами и подсетями

# Работа с блокнутыми IP

    def putworkip(self, ip):

        self.database.insertdata('workipsinfo', 'workip', f"'{ip}'")

    def getworkip(self):

        ips = []

        for data in self.database.getdata('workipsinfo', 'workip'):

            if not(data[0] == None):
                ips.append(data[0])

        return ips
    
    def putwhiteset(self, subset):

        self.database.insertdata('workipsinfo', 'workset', f"'{subset}'")

    def getwhitesubset(self):

        subset_list = []

        for data in self.database.getdata('workipsinfo', 'workset'):

            if not(data[0] == None):
                subset_list.append(data[0])

        return subset_list

    def deletewhiteset(self, subset):

        self.database.deldata('workipsinfo', 'workset', subset)
    
# Работа с блокнутыми IP

    def putblockip(self, ip):

        self.database.insertdata('blockipsinfo', 'blockip', f"'{ip}'")

    def getblockip(self):

        ips = []

        for data in self.database.getdata('blockipsinfo', 'blockip'):

            if not(data[0] == None):
                ips.append(data[0])

        return ips

    def putblockset(self, subset):

        self.database.insertdata('blockipsinfo', 'blocksubset', f'{subset}')

    def getblocksubset(self):

        subset_list = []

        for data in self.database.getdata('blockipsinfo', 'blocksubset'):

            if not(data[0] == None):
                subset_list.append(data[0])

        return subset_list
    
    def deleteblockip(self, ip):

        self.database.deldata('blockipsinfo', 'blockip', ip)

    def deleteblockset(self, subset):

        self.database.deldata('blockipsinfo', 'blocksubset', subset)

# Работа с регионами

    def regionlist(self):

        region_mas = []

        for data in self.database.getdata('regions', 'default'):

            if not(data[1] == None):
                region_mas.append(data[1])

        if len(region_mas) == 0:

            for region in regions:
                
                self.database.insertdata('regions', 'regionuser', f"'{region}'")

        return region_mas

    def dropregion(self):

        count = 1
        regions_id = []

        print("Удаление региона:")

        for region in self.regionlist():
            
            print(f'{count}. {regions_list.get(region)}:  {region}')
            count += 1
            regions_id.append(region)

        choose_del_region = int(input(">>> "))

        if not(choose_del_region == 0):

            self.database.deldata('regions', 'regionuser', f"{regions_id[choose_del_region-1]}")

    def addregion(self, aws_data):

        session = boto3.session.Session(aws_access_key_id=aws_data[0][1], aws_secret_access_key=aws_data[0][2],region_name = 'eu-central-1')
        ec2 = session.client('ec2')

        all_regions = ec2.describe_regions(AllRegions=True)
        open_regions = ec2.describe_regions(AllRegions=False)
        all_region_list = []
        open_region_list = []
        parametrs = ''
        count = 1

        for region in all_regions['Regions']:
            all_region_list.append(region['RegionName'])

        for region in open_regions['Regions']:
            open_region_list.append(region['RegionName'])

        print("Добавление регионов:")
        for region in all_region_list:

            if region in open_region_list:

                parametrs += '[Открыт]'

            if region in self.regionlist():

                    parametrs += '[Добавлен]'

            print(f"{count}. {regions_list.get(region)} {region} {parametrs}")

            parametrs = ''
            count += 1

        choose_add_region = int(input(">>> "))
        
        if not(choose_add_region == 0):

            if all_region_list[choose_add_region-1] in self.regionlist():

                print("Данный регион уже списке")
                
            else:

                self.database.insertdata('regions', 'regionuser', f"'{all_region_list[choose_add_region-1]}'")
                print('Регион успешно добавлен')

regions_list = {'us-east-1': 'N. Virginia',
           'us-east-2': 'Ohio',
           'us-west-1': 'N. California',
           'us-west-2': 'Oregon',
           'ap-east-1': 'Hong Kong',
           'ap-south-1': 'Mumbai',
           'ap-northeast-3': 'Osaka',
           'ap-northeast-2': 'Seoul',
           'ap-southeast-1': 'Singapore',
           'ap-southeast-2': 'Sydney',
           'ap-northeast-1': 'Tokyo',
           'ca-central-1': 'Canada',
           'cn-north-1': 'Beijing',
           'cn-northwest-1': 'Ningxia',
           'eu-central-1': 'Frankfurt',
           'eu-west-1': 'Ireland',
           'eu-west-2': 'London',
           'eu-west-3': 'Paris',
           'eu-north-1': 'Stockholm',
           'sa-east-1': 'São Paulo',
           'af-south-1': 'Cape Town',
           'ap-south-2': 'Hyderabad',
           'ap-southeast-3': 'Jakarta',
           'eu-south-1': 'Milan',
           'eu-west-4': 'Netherlands',
           'me-south-1': 'Bahrain', 
           'me-central-1': 'UAE'}

regions = ['us-east-1',
                'us-east-2',
                'us-west-1',
                'us-west-2',
                'ap-south-1',
                'ap-northeast-3',
                'ap-northeast-2',
                'ap-southeast-1',
                'ap-southeast-2',
                'ap-northeast-1',
                'ca-central-1',
                'eu-central-1',
                'eu-west-1',
                'eu-west-2',
                'eu-west-3',
                'eu-north-1',
                'sa-east-1']

awss = aws("xxx", "xxx", "eu-west-1")
