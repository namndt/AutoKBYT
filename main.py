# "items": [
#     {
#         "id": 1,
#         "order": 1,
#         "code": "436",
#         "nameVi": "Tp. Hà Tĩnh",
#         "nameEn": "Tp. Hà Tĩnh",
#         "nameTw": "河靜市",
#     },
#     {
#         "id": 2,
#         "order": 2,
#         "code": "449",
#         "nameVi": "Tx. Kỳ Anh",
#         "nameEn": "Tx. Kỳ Anh",
#         "nameTw": "奇英市",
#     },
#     {
#         "id": 3,
#         "order": 3,
#         "code": "447",
#         "nameVi": "H. Kỳ Anh",
#         "nameEn": "H. Kỳ Anh",
#         "nameTw": "奇英縣",
#     },
#     {
#         "id": 4,
#         "order": 4,
#         "code": "446",
#         "nameVi": "Cẩm Xuyên",
#         "nameEn": "Cẩm Xuyên",
#         "nameTw": "錦川縣",
#     },
#     {
#         "id": 5,
#         "order": 5,
#         "code": "445",
#         "nameVi": "Thạch Hà",
#         "nameEn": "Thạch Hà",
#         "nameTw": "石河縣",
#     },
#     {
#         "id": 6,
#         "order": 6,
#         "code": "448",
#         "nameVi": "Lộc Hà",
#         "nameEn": "Lộc Hà",
#         "nameTw": "祿河縣",
#     },
#     {
#         "id": 7,
#         "order": 7,
#         "code": "437",
#         "nameVi": "Hồng Lĩnh",
#         "nameEn": "Hồng Lĩnh",
#         "nameTw": "鴻嶺市",
#     },
#     {
#         "id": 8,
#         "order": 8,
#         "code": "439",
#         "nameVi": "Hương Sơn",
#         "nameEn": "Hương Sơn",
#         "nameTw": "香山縣",
#     },
#     {
#         "id": 9,
#         "order": 9,
#         "code": "440",
#         "nameVi": "Đức Thọ",
#         "nameEn": "Đức Thọ",
#         "nameTw": "德壽縣",
#     },
#     {
#         "id": 10,
#         "order": 10,
#         "code": "441",
#         "nameVi": "Vũ Quang",
#         "nameEn": "Vũ Quang",
#         "nameTw": "羽光縣",
#     },
#     {
#         "id": 11,
#         "order": 11,
#         "code": "442",
#         "nameVi": "Nghi Xuân",
#         "nameEn": "Nghi Xuân",
#         "nameTw": "儀春縣",
#     },
#     {
#         "id": 12,
#         "order": 12,
#         "code": "443",
#         "nameVi": "Can Lộc",
#         "nameEn": "Can Lộc",
#         "nameTw": "幹祿縣",
#     },
#     {
#         "id": 13,
#         "order": 13,
#         "code": "444",
#         "nameVi": "Hương Khê",
#         "nameEn": "Hương Khê",
#         "nameTw": "香溪縣",
#     }
# ]
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
        'position_detail_id': 2
    },
    'user2': {
        'id': 'VNW0010805',
        'name': 'Giang',
        'password': '555666',
        'position_id': 1,
        'position_detail_id': 2
    },
    'user3': {
        'id': 'VNW0011803',
        'name': 'TiểuLâm',
        'password': '123456',
        'position_id': 1,
        'position_detail_id': 2
    },
    'user4': {
        'id': 'VNW0002643',
        'name': 'PyThông',
        'password': 'Th1791988@',
        'position_id': 1,
        'position_detail_id': 2
    },
    'user5': {
        'id': 'VNW0001801',
        'name': 'A Thor',
        'password': 'A@09876',
        'position_id': 1,
        'position_detail_id': 2
    },
    'user6': {
        'id': 'VNW0007441',
        'name': 'A Sỹ',
        'password': '888888',
        'position_id': 1,
        'position_detail_id': 2
    },
    'user7': {
        'id': 'VNW0002008',
        'name': 'A Tiệp',
        'password': '19001520',
        'position_id': 1,
        'position_detail_id': 2
    },
    'user8': {
        'id': 'VNW0002005',
        'name': 'A Hùng',
        'password': '888666',
        'position_id': 1,
        'position_detail_id': 2
    },
    'user8': {
        'id': 'VNW0015858',
        'name': 'Thùy',
        'password': 'Thuy@0605',
        'position_id': 1,
        'position_detail_id': 2
    },
    'user9': {
        'id': 'VNW0009883',
        'name': 'A Sáng',
        'password': '22446688',
        'position_id': 1,
        'position_detail_id': 2
    },
    'user10': {
        'id': 'VNW0002005',
        'name': 'A Hùng',
        'password': '888666',
        'position_id': 1,
        'position_detail_id': 2
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
    dtNow = datetime.now().strftime('%Y-%m-%d')
    isWork = True if datetime.now().isoweekday() in (1, 2, 3, 4, 5, 6) else False
    body_temp = 0
    for idx, user in USER_INFO.items():
        if isWork:
            body_temp = random_temp()
            reasonId = None
            positionId = None
            positionDetailId = None
        else:
            body_temp = 0
            reasonId = 1
            positionId = user['position_id']
            positionDetailId = user['position_detail_id']
        payload = {
            'healthDate': dtNow,
            'measureMethodId': 2,
            'temperature': body_temp,
            'covids': None,
            'isWork': isWork,
            'reasonId': reasonId,
            'positionId': positionId,
            'positionDetailId': positionDetailId
        }
        detail = f'Nhiệt độ {body_temp}, đi làm.' if isWork else f'Nghỉ ở nhà tại {positionDetailId}, {positionId}'
        access_token = get_access_token(user=user['id'], password=user['password'])
        headers = {
            'Content-Type':'application/json',
            'Authorization': 'Bearer {}'.format(access_token)
        }
        covid_url = 'http://203.162.251.204/FHS_COVID/api/healths'
        try:
            response = requests.post(url=covid_url, data=json.dumps(payload), headers=headers)
            logging.info(response.json())
            line_notify('Khai báo cho {}: {}. Chi tiết: {}'.format(user['name'], response.json(), detail))
        except:
            line_notify('Không thể khai báo cho {}'.format(user['name']))


def get_access_token(user, password):
    url = 'http://203.162.251.204/FHS_COVID/token'
    headers={
        'Content-type':'application/json', 
        'Accept':'application/json, text/plain, */*'
    }
    payload = {
        'username': user,
        'password': password,
        'appId': 1
    }
    access_token = None
    try:
        response = requests.post(url=url, data=json.dumps(payload), headers=headers)
        json_response = response.json()
        access_token = json_response['access_token']
        logging.info(f'{user} access token: {access_token}')
    except:
        line_notify(f'Không lấy được token của {user}')
    return access_token


def random_temp():
    temp = round(random.uniform(36, 36.5), 1)
    logging.info(f'Random body temp: {temp}')
    return temp


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] - %(message)s')
    logging.debug('Start')
    # declare()
    schedule.every().day.at('07:30').do(declare)
    while True:
        schedule.run_pending()
        sleep(30)
