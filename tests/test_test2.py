import pytest
from time import sleep


@pytest.fixture(scope="session")
def fixt1(request):
    with open(request.param, "w") as file:
        yield file


def pytest_generate_tests(metafunc):
    metafunc.parametrize("setup_driver_new", [{
        "remoteIP": "80.87.200.64",
        "remotePort": 4444,
        "browser": "Chrome"
    }], indirect=True)
    metafunc.parametrize("url", ["https://yandex.ru", "https://google.com"])


def test_test(url, setup_driver_new):
    Driver = setup_driver_new
    Driver.driver.get(url)
    Driver.driver.save_screenshot("screen.png")
    sleep(5)
    assert True