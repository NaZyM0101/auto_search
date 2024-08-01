# -*- coding: utf-8 -*-

import boto3, time, requests
from database2 import postgresql

class aws:

    def __init__(self, access_key, secret_key, region):

        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region

        session = boto3.session.Session(aws_access_key_id=access_key, aws_secret_access_key=secret_key,region_name=region)
        self.ec2 = session.client('ec2')

    def getip(self):

        ipinf = {}

        response = self.ec2.describe_addresses()

        for address in response['Addresses']:
            
            elastic_ip = address['PublicIp']
            elastic_id = address['AllocationId']

            ipinf.update({elastic_ip: elastic_id})
            
        return ipinf

    def delip(self, elastic_id):

        self.ec2.release_address(AllocationId=elastic_id)

    def allocateip(self):

        self.ec2.allocate_address(Domain='vpc')

def timeIsUp(time_now):

    time_mid = time.time() - time_now
    time_of_check = []

    days = int(time_mid // (24*3600))
    time_mid %= (24*3600)
    time_of_check.append(days)
    hours = int(time_mid // 3600)
    time_mid %= 3600
    time_of_check.append(hours)
    minutes = int(time_mid // 60)
    time_mid %= 60
    time_of_check.append(minutes)
    seconds = int(time_mid)
    time_of_check.append(seconds)

    return time_of_check
    
def sendMessage(token, chat_id, text):
    
    try:

        url = f"https://api.telegram.org/bot{token}/sendMessage"
        params = {"chat_id": chat_id, "text": text}
        response = requests.get(url, params=params)
        return response.json()
    
    except:

        sendMessage(token, chat_id, text)


def countDown(time_sleep, mas, regions):

    accounts = []
    accounts_data = postgresql.getdata('agrosettings', 'default')

    for account in range(len(accounts_data)):

        accounts.append(postgresql.getdata('agrosettings', 'default')[account][1])
    
    if len(accounts) > 1:
        accounts = ', '.join(accounts)

    else:
        accounts = accounts[0]

    time_now = time.time()

    while True:

        time.sleep(time_sleep_list_numeration[time_sleep-1])
        message = f'Прошло {timeIsUp(time_now)[0]} дней | {timeIsUp(time_now)[1]} часов | {timeIsUp(time_now)[2]} минут | {timeIsUp(time_now)[3]} секунд\nСтатистика IP: {mas[2]} всего | {mas[0]} рабочих | {mas[1]} не рабочих\nПоиск продолжается на {len(accounts_data)} аккаунтах и {regions} регионах\nАккаунты: {accounts}'
        sendMessage(postgresql.getdata('mainsetting', 'default')[0][4], postgresql.getdata('mainsetting', 'default')[0][3], message)

time_sleep_list_numeration = [300, 600, 1800, 3600, 10800, 21600, 43200, 86400]