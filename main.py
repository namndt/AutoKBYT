import requests
import logging
import json
import random
from datetime import datetime
from time import sleep
import schedule
import win32serviceutil
import servicemanager
import win32service
import win32event
import socket
from pathlib import Path, PurePath
import sys
from configparser import ConfigParser


# USER_INFO = {
#     'user1': {
#         'id': 'VNW0014742',
#         'name': 'TienNam',
#         'password': 'p@ssw0rd',
#         'position_id': 1,
#         'position_detail_id': 2,
#         'position_areas': '99',
#     },
#     'user2': {
#         'id': 'VNW0010805',
#         'name': 'Giang',
#         'password': '555666',
#         'position_id': 1,
#         'position_detail_id': 2,
#         'position_areas': '99',
#     },
#     'user3': {
#         'id': 'VNW0011803',
#         'name': 'TiểuLâm',
#         'password': '123456',
#         'position_id': 1,
#         'position_detail_id': 2,
#         'position_areas': '99',
#     },
#     'user4': {
#         'id': 'VNW0002643',
#         'name': 'PyThông',
#         'password': 'Th1791988@',
#         'position_id': 1,
#         'position_detail_id': 2,
#         'position_areas': 'FL',
#     },
#     'user5': {
#         'id': 'VNW0001801',
#         'name': 'A Thor',
#         'password': 'A@09876',
#         'position_id': 1,
#         'position_detail_id': 2,
#         'position_areas': '99',
#     },
#     'user6': {
#         'id': 'VNW0007441',
#         'name': 'A Sỹ',
#         'password': '888888',
#         'position_id': 1,
#         'position_detail_id': 2,
#         'position_areas': 'FL',
#     },
#     'user7': {
#         'id': 'VNW0002008',
#         'name': 'A Tiệp',
#         'password': '19001520',
#         'position_id': 1,
#         'position_detail_id': 2,
#         'position_areas': '99',
#     },
#     'user8': {
#         'id': 'VNW0002005',
#         'name': 'A Hùng',
#         'password': '888666',
#         'position_id': 1,
#         'position_detail_id': 2,
#         'position_areas': 'FL',
#     },
#     'user9': {
#         'id': 'VNW0015858',
#         'name': 'Thùy',
#         'password': 'Thuy@0605',
#         'position_id': 1,
#         'position_detail_id': 2,
#         'position_areas': '99',
#     },
#     'user10': {
#         'id': 'VNW0009883',
#         'name': 'A Sáng',
#         'password': '22446688',
#         'position_id': 1,
#         'position_detail_id': 2,
#         'position_areas': '99',
#     },
#     'user11': {
#         'id': 'VNW0008003',
#         'name': 'C Hoài',
#         'password': '555555',
#         'position_id': 1,
#         'position_detail_id': 2,
#         'position_areas': '99',
#     },
#     'user12': {
#         'id': 'VNW0003018',
#         'name': 'C Hoa TB',
#         'password': '05082035',
#         'position_id': 1,
#         'position_detail_id': 2,
#         'position_areas': '99',
#     },
#     'user13': {
#         'id': 'VNW0016002',
#         'name': 'E HaiBien',
#         'password': '123456',
#         'position_id': 1,
#         'position_detail_id': 2,
#         'position_areas': '99',
#     },
#     'user14': {
#         'id': 'VNW0007437',
#         'name': 'A Nguyên',
#         'password': '14695551',
#         'position_id': 1,
#         'position_detail_id': 2,
#         'position_areas': '99',
#     }
# }

class Configuration():
    INI_FILE_NAME = 'settings.ini'
    application_path = Path(sys.executable).parent

    def __init__(self):
        self.__config = ConfigParser()
        self.__ini_full_path = PurePath(self.application_path).joinpath(self.INI_FILE_NAME)

    def read(self, section, key):
        self.__config.read(self.__ini_full_path)
        value = self.__config.get(section=section, option=key)
        return value


class LineNotify():
    def __init__(self) -> None:
        self.apply_config()

    def apply_config(self):
        self.LINE_API_URL = iniconfig.read('LINE_NOTIFY', 'line_api_url')
        self.LINE_TOKEN = iniconfig.read('LINE_NOTIFY', 'line_token')

    def send_notify(self, message):
        # token = 'cQnS7ijpv0YqQrl7Fly7G3hvOMkuHD5IFDaRDHCmaLy'
        # token = '20yBTkYFBYUjp2OSxQI57KuLbuF4LEQd0jYGx2Wkkyy'
        headers = {'Authorization': f'Bearer {self.LINE_TOKEN}'}
        data = {'message': message}
        requests.post(url=self.LINE_API_URL, data=data, headers=headers)


class ServiceBase(win32serviceutil.ServiceFramework):
    _svc_name_ = 'AutoKBYT'
    _svc_display_name_ = 'Auto KBYT'
    _svc_description_ = 'Tu dong khai bao nhiet do'

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, *args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.line = LineNotify()
        self.is_alive = False
        self.apply_config()

    def apply_config(self):
        self.ACCESS_TOKEN_URL = iniconfig.read('SETTING', 'access_token_url')
        self.DECLARE_URL = iniconfig.read('SETTING', 'declare_url')
        self.DECLARE_TIME = iniconfig.read('SETTING', 'declare_submit_time')
        self.USERS_AMOUNT = int(iniconfig.read('SETTING', 'number_of_user'))

    def parse_command_line(cls):
        win32serviceutil.HandleCommandLine(cls)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.stop()
        win32event.SetEvent(self.hWaitStop)
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def SvcDoRun(self):
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        try:
            self.ReportServiceStatus(win32service.SERVICE_RUNNING)
            self.start()
            self.main()
            win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)
            servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, servicemanager.PYS_SERVICE_STARTED, (self._svc_name_, ''))
        except Exception:
            self.SvcStop()

    def random_temp(self):
        return round(random.uniform(36, 36.5), 1)

    def get_access_token(self, user, password):
        headers={
            'Content-type':'application/json', 
            'Accept':'application/json, text/plain, */*'
        }
        payload = {
            'username': user,
            'password': password,
            "remember": True,
            "mobile": True,
            "device": "android",
            "appId": 5
        }
        full_name, access_token = None, None
        try:
            response = requests.post(url=self.ACCESS_TOKEN_URL, data=json.dumps(payload), headers=headers)
            json_response = response.json()
            access_token = json_response['access_token']
            full_name = json_response['user']['fullName']
        except:
            self.line.send_notify(f'Không lấy được token của {user}')
        return full_name, access_token

    def declare(self):
        dtNow = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        isWork = True if datetime.now().isoweekday() in (1, 2, 3, 4, 5, 6) else False
        for i in range(self.USERS_AMOUNT):
            user = iniconfig.read(f'USER_{i + 1}', 'id')
            password = iniconfig.read(f'USER_{i + 1}', 'password')
            positionId = None if isWork else iniconfig.read(f'USER_{i + 1}', 'position_id')
            positionDetailId = None if isWork else iniconfig.read(f'USER_{i + 1}', 'position_detail_id')
            positionAreas = None if isWork else iniconfig.read(f'USER_{i + 1}', 'position_areas')
            temperature = self.random_temp() if isWork else 0
            payload = {
                'healthDate': dtNow,
                'measureMethodId': 2,  # Đo nhiệt độ ở trán
                'temperature': temperature,  # Ngày nghỉ không cần đo nhiệt độ
                'covids': None,
                'isWork': isWork,
                'reasonId': None if isWork else 1,  # Lý do nghỉ. 1 cho nghỉ chủ nhật
                'positionId': positionId,
                'positionDetailId': positionDetailId,
                "shifts": 'GO' if isWork else None,
                "holidayTypes": None,
                "quarantineAreas": None,
                "positionAreas": positionAreas
            }
            detail = f'Nhiệt độ {temperature}, đi làm ca GO.' if isWork else f'Nghỉ ở nhà tại {positionId}/{positionDetailId}/{positionAreas}'
            full_name, access_token = self.get_access_token(user=user, password=password)
            headers = {
                'Content-Type':'application/json',
                'Authorization': 'Bearer {}'.format(access_token)
            }
            try:
                response = requests.post(url=self.DECLARE_URL, data=json.dumps(payload), headers=headers)
                logging.info(response.json())
                self.line.send_notify('Khai báo cho {}: {}. Chi tiết: {}'.format(full_name, response.json(), detail))
            except:
                self.line.send_notify('Không thể khai báo cho {}({})'.format(full_name, user['name']))

    def start(self):
        self.is_alive = True

    def stop(self):
        self.is_alive = False

    def main(self):
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        # self.declare()
        schedule.every().day.at(self.DECLARE_TIME).do(self.declare)
        while self.is_alive:
            schedule.run_pending()
            sleep(10)


if __name__ == '__main__':
    iniconfig = Configuration()
    if len(sys.argv) == 1:  # by pass error 1503
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(ServiceBase)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        ServiceBase.parse_command_line(ServiceBase)
