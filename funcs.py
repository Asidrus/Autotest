def pytest_generate_tests(metafunc):
	# читаем документ и записываем пару данные валидация
	data = [("Тест1", False),("Тест", True)]
	metafunc.parametrize("data, valid", data)


@pytest.fixture(scope="session")
def setup_driver(request):
    try:
        chrome_options = Options()
        if request.config.getoption("--invisible"):
            display = Display(visible=0, size=(1920, 1080))
            display.start()
        if request.config.getoption("--adaptive"):
            chrome_options.add_argument(
                '--user-agent="Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166"')
        d = DesiredCapabilities.CHROME
        d['loggingPrefs'] = {'browser': 'ALL'}
        chrome_options.add_argument("--window-size=1920,1080")
        Driver = webdriver.Chrome(chromedriver, desired_capabilities=d, options=chrome_options)
    except Exception as e:
        raise e
    yield Driver
    try:
        Driver.close()
        Driver.quit()
        if request.config.getoption("--invisible"):
            display.stop()
    except Exception as e:
        raise e
        

def test_formSending(data, valid, setup_driver):
	driver = setup_driver
	url = "https://penta....
	if driver.current_url != "url:
		driver.get(url)
	#пулим данные, жмем кнопку, парсим ошибку
	assert (valid^result), f"данные {data} не правильно валидируются"