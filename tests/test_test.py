import pytest
import random


@pytest.fixture(scope="function", autouse=True)
def failure_tracking_fixture(request):
    tests_failed_before_module = request.session.testsfailed
    yield
    tests_failed_during_module = request.session.testsfailed - tests_failed_before_module
    # print(request.session.reruns)
    # with open("file.txt", "a+") as file:
    #     file.write(str(tests_failed_during_module)+"\n")


# @pytest.mark.parametrize("i", range(10))
@pytest.mark.flaky(reruns=2)
def test_test(failure_tracking_fixture):
    assert random.choice([True, False])
