
import os

import pytest
from sanic_restful import json

from kakaopay.server.app import init_app
from kakaopay.constant.constant import ResponseCode

TEST_ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__)))


@pytest.yield_fixture
def app():
    app = init_app()
    yield app


@pytest.fixture
def test_cli(loop, app, sanic_client):
    return loop.run_until_complete(sanic_client(app))


@pytest.fixture
def remove_db():
    path = os.path.abspath("./data.sqlite")
    try:
        os.remove(path)
    except OSError:
        pass


#########
# Tests #
#########

@ pytest.mark.order1
async def test_fixture_test_client_signup(test_cli, remove_db):
    """
    POST request
    """

    data = {
        "id": "kakao",
        "pw": "1234"
    }
    resp = await test_cli.post('/signup', data=json.dumps(data))
    assert resp.status == 200
    resp_json = await resp.json()
    assert 'token' in resp_json


async def test_fixture_test_client_signup_already_exist_db(test_cli):
    """
    POST request
    """

    data = {
        "id": "kakao",
        "pw": "1234"
    }
    resp = await test_cli.post('/signup', data=json.dumps(data))
    assert resp.status == ResponseCode.RESPONSE_ERROR
    resp_json = await resp.json()
    assert resp_json == {"msg": "already exist account"}


async def test_fixture_test_client_signin(test_cli):
    """
    PUT request
    """
    data = {
        "id": "kakao",
        "pw": "1234"
    }
    resp = await test_cli.put('/signin', data=json.dumps(data))
    assert resp.status == 200
    resp_json = await resp.json()
    assert 'token' in resp_json


async def test_fixture_test_client_refreshtoken(test_cli):
    """
    PUT request
    """
    data = {
        "id": "kakao",
        "pw": "1234"
    }

    resp = await test_cli.put('/signin', data=json.dumps(data))
    assert resp.status == 200
    resp_json = await resp.json()
    token = resp_json['token']

    header = {
        "Authorization": f"bearer {token}"
    }

    resp = await test_cli.put('/refreshtoken', headers=header)
    assert resp.status == 200
    resp_json = await resp.json()
    assert 'token' in resp_json


@ pytest.mark.order2
async def test_fixture_test_client_api1(test_cli):
    """
    POST request
    """
    data = {
        "id": "kakao",
        "pw": "1234"
    }

    resp = await test_cli.put('/signin', data=json.dumps(data))
    assert resp.status == 200
    resp_json = await resp.json()
    token = resp_json['token']

    header = {
        "Authorization": f"basic {token}"
    }

    resp = await test_cli.post('/api1', headers=header)
    assert resp.status == 200
    resp_json = await resp.json()
    assert resp_json == {"msg": "init DB"}


async def test_fixture_test_client_api2(test_cli):
    """
    GET request
    """
    data = {
        "id": "kakao",
        "pw": "1234"
    }

    resp = await test_cli.put('/signin', data=json.dumps(data))
    assert resp.status == 200
    resp_json = await resp.json()
    token = resp_json['token']

    header = {
        "Authorization": f"basic {token}"
    }

    resp = await test_cli.get('/api2', headers=header)
    assert resp.status == 200
    resp_json = await resp.json()
    expect_res = {
        "bank": ['주택도시기금', '국민은행', '우리은행', '신한은행', '한국시티은행', '하나은행', '농협은행/수협은행', '외환은행', '기타은행']}
    assert resp_json == expect_res


async def test_fixture_test_client_api3(test_cli):
    """
    GET request
    """
    data = {
        "id": "kakao",
        "pw": "1234"
    }

    resp = await test_cli.put('/signin', data=json.dumps(data))
    assert resp.status == 200
    resp_json = await resp.json()
    token = resp_json['token']

    header = {
        "Authorization": f"basic {token}"
    }

    resp = await test_cli.get('/api3', headers=header)
    assert resp.status == 200
    resp_json = await resp.json()
    expect_res = {
        'name': '주택금융 공급현황',
        'content':
            [
                {'year': '2005', 'total_amount': 48016, 'detail_amount':
                    {'주택도시기금': 22247, '국민은행': 13231, '우리은행': 2303, '신한은행': 1815, '한국시티은행': 704,
                     '하나은행': 3122, '농협은행/수협은행': 1486, '외환은행': 1732, '기타은행': 1376}},
                {'year': '2006', 'total_amount': 41210, 'detail_amount':
                    {'주택도시기금': 20789, '국민은행': 5811, '우리은행': 4134, '신한은행': 1198, '한국시티은행': 288,
                     '하나은행': 3443, '농협은행/수협은행': 2299, '외환은행': 2187, '기타은행': 1061}},
                {'year': '2007', 'total_amount': 50893, 'detail_amount':
                    {'주택도시기금': 27745, '국민은행': 8260, '우리은행': 3545, '신한은행': 2497, '한국시티은행': 139,
                     '하나은행': 2279, '농협은행/수협은행': 3515, '외환은행': 2059, '기타은행': 854}},
                {'year': '2008', 'total_amount': 67603, 'detail_amount':
                    {'주택도시기금': 35721, '국민은행': 12786, '우리은행': 4290, '신한은행': 1701, '한국시티은행': 69,
                     '하나은행': 1706, '농협은행/수협은행': 9630, '외환은행': 941, '기타은행': 759}},
                {'year': '2009', 'total_amount': 96545, 'detail_amount':
                    {'주택도시기금': 44735, '국민은행': 8682, '우리은행': 13105, '신한은행': 3023, '한국시티은행': 40,
                     '하나은행': 1226, '농협은행/수협은행': 8775, '외환은행': 6908, '기타은행': 10051}},
                {'year': '2010', 'total_amount': 114903, 'detail_amount':
                    {'주택도시기금': 50554, '국민은행': 16017, '우리은행': 15846, '신한은행': 2724, '한국시티은행': 22,
                     '하나은행': 1872, '농협은행/수협은행': 10984, '외환은행': 11158, '기타은행': 5726}},
                {'year': '2011', 'total_amount': 206693, 'detail_amount':
                    {'주택도시기금': 69236, '국민은행': 29118, '우리은행': 29572, '신한은행': 11106, '한국시티은행': 13,
                     '하나은행': 9283, '농협은행/수협은행': 19847, '외환은행': 8192, '기타은행': 30326}},
                {'year': '2012', 'total_amount': 275591, 'detail_amount':
                    {'주택도시기금': 84227, '국민은행': 37597, '우리은행': 38278, '신한은행': 21742, '한국시티은행': 4,
                     '하나은행': 12534, '농협은행/수협은행': 27253, '외환은행': 19975, '기타은행': 33981}},
                {'year': '2013', 'total_amount': 265805, 'detail_amount':
                    {'주택도시기금': 89823, '국민은행': 33063, '우리은행': 37661, '신한은행': 21330, '한국시티은행': 50,
                     '하나은행': 15167, '농협은행/수협은행': 17908, '외환은행': 10619, '기타은행': 40184}},
                {'year': '2014', 'total_amount': 318771, 'detail_amount':
                    {'주택도시기금': 96184, '국민은행': 48338, '우리은행': 52085, '신한은행': 28526, '한국시티은행': 183,
                     '하나은행': 20714, '농협은행/수협은행': 20861, '외환은행': 11183, '기타은행': 40697}},
                {'year': '2015', 'total_amount': 374773, 'detail_amount':
                    {'주택도시기금': 82478, '국민은행': 57749, '우리은행': 67999, '신한은행': 39239, '한국시티은행': 37,
                     '하나은행': 37263, '농협은행/수협은행': 18541, '외환은행': 20421, '기타은행': 51046}},
                {'year': '2016', 'total_amount': 400971, 'detail_amount':
                    {'주택도시기금': 91017, '국민은행': 61380, '우리은행': 45461, '신한은행': 36767, '한국시티은행': 46,
                     '하나은행': 45485, '농협은행/수협은행': 23913, '외환은행': 5977, '기타은행': 90925}},
                {'year': '2017', 'total_amount': 295126, 'detail_amount':
                    {'주택도시기금': 85409, '국민은행': 31480, '우리은행': 38846, '신한은행': 40729, '한국시티은행': 7,
                     '하나은행': 35629, '농협은행/수협은행': 26969, '외환은행': 0, '기타은행': 36057}}
            ]}
    assert resp_json == expect_res


async def test_fixture_test_client_api4(test_cli):
    """
    GET request
    """
    data = {
        "id": "kakao",
        "pw": "1234"
    }

    resp = await test_cli.put('/signin', data=json.dumps(data))
    assert resp.status == 200
    resp_json = await resp.json()
    token = resp_json['token']

    header = {
        "Authorization": f"basic {token}"
    }

    resp = await test_cli.get('/api4', headers=header)
    assert resp.status == 200
    resp_json = await resp.json()
    expect_res = {'bank': '주택도시기금', 'year': 2014}
    assert resp_json == expect_res


async def test_fixture_test_client_api5(test_cli):
    """
    GET request
    """
    data = {
        "id": "kakao",
        "pw": "1234"
    }

    resp = await test_cli.put('/signin', data=json.dumps(data))
    assert resp.status == 200
    resp_json = await resp.json()
    token = resp_json['token']

    header = {
        "Authorization": f"basic {token}"
    }

    resp = await test_cli.get('/api5', headers=header)
    assert resp.status == 200
    resp_json = await resp.json()
    expect_res = {'bank': '외환은행', 'support_amount': [{'year': 2017, 'amount': 0.0}, {'year': 2015, 'amount': 1701.75}]}
    assert resp_json == expect_res