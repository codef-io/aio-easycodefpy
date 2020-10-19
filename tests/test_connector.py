import pytest
import aiohttp
from .helper import *
from aio_easycodefpy.connector import *
from aio_easycodefpy.properties import\
    SANDBOX_CLIENT_ID,\
    SANDBOX_CLIENT_SECRET,\
    SANDBOX_DOMAIN,\
    PATH_CREATE_ACCOUNT
from aio_easycodefpy.easycodefpy import Codef


@pytest.mark.asyncio
async def test_request_token():
    async with aiohttp.ClientSession() as session:
        res = await request_token(
            SANDBOX_CLIENT_ID,
            SANDBOX_CLIENT_SECRET,
            session,
        )
        assert res is not None
        token = res['access_token']
        assert token is not None and token != ''


@pytest.mark.asyncio
async def test_request_product():
    param = create_param_for_create_cid()
    access_token = ''
    async with aiohttp.ClientSession() as session:
        # test for 404 error
        res = await request_product(
            SANDBOX_DOMAIN + "/failPath",
            access_token,
            json.dumps(param),
            session,
        )
        assert 'CF-00404' == res['result']['code']

        # test for success
        token_dict = await request_token(
            SANDBOX_CLIENT_ID,
            SANDBOX_CLIENT_SECRET,
            session,
        )
        access_token = token_dict['access_token']
        res = await request_product(
            SANDBOX_DOMAIN + PATH_CREATE_ACCOUNT,
            access_token,
            json.dumps(param),
            session,
        )
        assert exist_cid(res)


@pytest.mark.asyncio
async def test_set_token():
    codef = Codef()
    await set_token(
        SANDBOX_CLIENT_ID,
        SANDBOX_CLIENT_SECRET,
        codef,
        ServiceType.SANDBOX
    )
    token = codef.get_access_token(ServiceType.SANDBOX)
    assert token != ''


@pytest.mark.asyncio
async def test_excute():
    codef = Codef()
    param = create_param_for_create_cid()
    res = await execute(PATH_CREATE_ACCOUNT, param, codef, ServiceType.SANDBOX)
    assert res is not None
    assert exist_cid(res)


@pytest.mark.asyncio
async def test_excute_by_unicode():
    codef = Codef()
    param = create_param_for_create_cid()
    param['dummy'] = '한글'
    res = await execute(PATH_CREATE_ACCOUNT, param, codef, ServiceType.SANDBOX)
    assert res is not None
    assert exist_cid(res)
