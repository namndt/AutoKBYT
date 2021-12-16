import requests
import logging
import json
import random
from datetime import datetime
from time import sleep
import schedule


USER_INFO = {
    'user1': {
        'id': 'VNW0014742',
        'name': 'TienNam',
        'password': 'p@ssw0rd',
        'position_id': 1,
        'position_detail_id': 2,
        'positionAreas': '99',
    },
    'user2': {
        'id': 'VNW0010805',
        'name': 'Giang',
        'password': '555666',
        'position_id': 1,
        'position_detail_id': 2,
        'positionAreas': '99',
    },
    'user3': {
        'id': 'VNW0011803',
        'name': 'TiểuLâm',
        'password': '123456',
        'position_id': 1,
        'position_detail_id': 2,
        'positionAreas': '99',
    },
    'user4': {
        'id': 'VNW0002643',
        'name': 'PyThông',
        'password': 'Th1791988@',
        'position_id': 1,
        'position_detail_id': 2,
        'positionAreas': 'FL',
    },
    'user5': {
        'id': 'VNW0001801',
        'name': 'A Thor',
        'password': 'A@09876',
        'position_id': 1,
        'position_detail_id': 2,
        'positionAreas': '99',
    },
    'user6': {
        'id': 'VNW0007441',
        'name': 'A Sỹ',
        'password': '888888',
        'position_id': 1,
        'position_detail_id': 2,
        'positionAreas': 'FL',
    },
    'user7': {
        'id': 'VNW0002008',
        'name': 'A Tiệp',
        'password': '19001520',
        'position_id': 1,
        'position_detail_id': 2,
        'positionAreas': '99',
    },
    'user8': {
        'id': 'VNW0002005',
        'name': 'A Hùng',
        'password': '888666',
        'position_id': 1,
        'position_detail_id': 2,
        'positionAreas': 'FL',
    },
    'user9': {
        'id': 'VNW0015858',
        'name': 'Thùy',
        'password': 'Thuy@0605',
        'position_id': 1,
        'position_detail_id': 2,
        'positionAreas': '99',
    },
    'user10': {
        'id': 'VNW0009883',
        'name': 'A Sáng',
        'password': '22446688',
        'position_id': 1,
        'position_detail_id': 2,
        'position_areas': '99',
    },
    'user11': {
        'id': 'VNW0008003',
        'name': 'C Hoài',
        'password': '333333',
        'position_id': 1,
        'position_detail_id': 2,
        'position_areas': '99',
    }
}


def line_notify(message):
    token = 'cQnS7ijpv0YqQrl7Fly7G3hvOMkuHD5IFDaRDHCmaLy'
    # token = '20yBTkYFBYUjp2OSxQI57KuLbuF4LEQd0jYGx2Wkkyy'
    headers = {'Authorization': f'Bearer {token}'}
    data = {'message': message}
    response = requests.post(url='https://notify-api.line.me/api/notify', data=data, headers=headers)
    logging.info(response.status_code)


def declare():
    dtNow = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    isWork = True if datetime.now().isoweekday() in (1, 2, 3, 4, 5, 6) else False
    body_temp = 0
    for idx, user in USER_INFO.items():
        if isWork:
            body_temp = random_temp()
            reasonId = None
            positionId = None
            positionDetailId = None
            positionAreas = None
            shifts = 'GO'
        else:
            body_temp = 0
            reasonId = 1
            positionId = user['position_id']
            positionDetailId = user['position_detail_id']
            positionAreas = user['position_areas']
            shifts = None
        payload = {
            'healthDate': dtNow,
            'measureMethodId': 2,
            'temperature': body_temp,
            'covids': None,
            'isWork': isWork,
            'reasonId': reasonId,
            'positionId': positionId,
            'positionDetailId': positionDetailId,
            "shifts": shifts,
            "holidayTypes": None,
            "quarantineAreas": None,
            "positionAreas": positionAreas
        }
        detail = f'Nhiệt độ {body_temp}, đi làm ca {shifts}.' if isWork else f'Nghỉ ở nhà tại {positionId}/{positionDetailId}/{positionAreas}'
        full_name, access_token = get_access_token(user=user['id'], password=user['password'])
        headers = {
            'Content-Type':'application/json',
            'Authorization': 'Bearer {}'.format(access_token)
        }
        covid_url = 'http://203.162.251.204/FHS_COVID/api/healths'
        try:
            response = requests.post(url=covid_url, data=json.dumps(payload), headers=headers)
            logging.info(response.json())
            line_notify('Khai báo cho {}: {}. Chi tiết: {}'.format(full_name, response.json(), detail))
        except:
            line_notify('Không thể khai báo cho {}'.format(full_name))


def get_access_token(user, password):
    url = 'http://203.162.251.204/FHS_COVID/token'
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
    access_token = None
    full_name = None
    try:
        response = requests.post(url=url, data=json.dumps(payload), headers=headers)
        json_response = response.json()
        access_token = json_response['access_token']
        full_name = json_response['user']['fullName']
        logging.info(f'{user} access token: {access_token}')
    except:
        line_notify(f'Không lấy được token của {user}')
    return full_name, access_token


def random_temp():
    temp = round(random.uniform(36, 36.5), 1)
    logging.info(f'Random body temp: {temp}')
    return temp


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] - %(message)s')
    logging.debug('Start')
    # declare()
    s = ''
    for idx, user in USER_INFO.items():
        s += '{}({}), '.format(user['name'], user['id'])
    logging.info('Danh sách khai báo: {}'.format(s))
    schedule.every().day.at('07:30').do(declare)
    while True:
        schedule.run_pending()
        sleep(30)
