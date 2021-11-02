from config import *
from conftest import alarm, db_connection, allure_step
import allure
import pytest


async def test_alarm():
    with allure_step(f"Тестирование бота", _alarm="ошибка"):
        assert False
