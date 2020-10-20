import base64
import json
from urllib import parse
from typing import Union

from aiohttp import ClientSession
from .properties import\
    OAUTH_DOMAIN,\
    PATH_GET_TOKEN,\
    ServiceType,\
    get_codef_domain
from .message import *


async def request_token(
        client_id: str,
        client_secret: str,
        session: ClientSession,
) -> Union[dict, None]:
    """
    액세스 토큰 요청
    :param client_id: 클라이언트 아이디
    :param client_secret: 클라이언트 시크릿
    :param session: 요청 세션
    :return: 토큰을 포함한 객체를 반환한다. 응답 코드 200이 아닐 경우 None을 반환한다.
    """
    url = OAUTH_DOMAIN + PATH_GET_TOKEN
    client_info = '{}:{}'.format(client_id, client_secret)
    b64_auth = base64.b64encode(client_info.encode('utf-8')).decode('utf-8')
    body = 'grant_type=client_credentials&scope=read'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic ' + b64_auth
    }
    async with session.post(url, data=body, headers=headers) as res:
        if res.status != 200:
            return None
        return await res.json()


async def request_product(
        url: str,
        token: str,
        body_str: str,
        session: ClientSession,
) -> dict:
    """
    상품 요청
    :param url: 요청 URL
    :param token: 액세스 토큰
    :param body_str: post 요청 바디
    :param session: 요청 세션
    :return:
    """
    headers = {
        'Accept': 'application/json',
    }
    if token != '' and token is not None:
        headers['Authorization'] = 'Bearer ' + token

    if body_str is not None and body_str != '':
        body_str = parse.quote(body_str)

    async with session.post(url, data=body_str, headers=headers) as res:
        s_code = res.status
        if s_code == 200:
            text = await res.text()
            data_str = parse.unquote_plus(text)
            return json.loads(data_str)
        elif s_code == 400:
            return MESSAGE_BAD_REQUEST
        elif s_code == 401:
            return MESSAGE_UNAUTHORIZED
        elif s_code == 403:
            return MESSAGE_FORBIDDEN
        elif s_code == 404:
            return MESSAGE_NOT_FOUND
        else:
            return MESSAGE_SERVER_ERROR


async def set_token(
        client_id: str,
        client_secret: str,
        codef,
        service_type: ServiceType,
):
    """
    코드에프 인스턴스에 액세스 토큰을 셋팅해준다.
    최대 3회까지 시도한다.
    :param client_id:
    :param client_secret:
    :param codef:
    :param service_type:
    :return:
    """
    repeat_cnt = 3
    i = 0
    if codef.get_access_token(service_type) == '':
        while i < repeat_cnt:
            token_dict = await request_token(
                client_id,
                client_secret,
                codef.get_session(),
            )
            if token_dict is None:
                i += 1
                continue
            token = token_dict['access_token']
            if token is not None and token != '':
                codef.set_access_token(token, service_type)
                break
            i += 1


async def execute(
        url_path: str,
        body: dict,
        codef,
        service_type: ServiceType,
) -> dict:
    """
    API 요청 실행 함수.
    실제 사용자에게 제공되는 함수 내부에서 이 함수를 호출해서 사용할 것을 권장한다.
    :param url_path: 요청 URL 경로
    :param body: post 요청 바디
    :param codef: codef 인스턴스
    :param service_type: 서비스 타입
    :return:
    """
    req_domain = get_codef_domain(service_type)
    client_id, client_secret = codef.get_client_info(service_type)
    await set_token(client_id, client_secret, codef, service_type)
    body = json.dumps(body, ensure_ascii=False)
    return await request_product(
        req_domain + url_path,
        codef.get_access_token(service_type),
        body,
        codef.get_session(),
    )
