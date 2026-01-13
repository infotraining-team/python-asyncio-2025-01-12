import pytest
import asyncio
import unittest.mock as mock

async def adder(a, b):
    return a + b

async def waiting_adder(a, b):
    await asyncio.sleep(2)
    return a + b

@pytest.mark.asyncio
async def test_adder():
    res = await adder(3, 5)
    assert res == 8


@pytest.mark.asyncio
async def test_sleep_adder():
    with mock.patch('asyncio.sleep', mock.AsyncMock(return_value=None)):
        res = await waiting_adder(3, 5)
        assert res == 8