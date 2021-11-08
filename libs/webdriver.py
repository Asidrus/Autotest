from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class WebDriver:
    adaptive = False
    browser = 'Chrome'
    version = 'latest'
    remote = False
    remoteIP = "127.0.0.1"
    remotePort = 4444
    logs = False
    window_size = (1920, 1080)
    executablePath = "chromedriver"

    driver = None

    def __init__(self, **kwargs):
        """Generate driver

        @param kwargs:
        @param adaptive: default is False
        @param browser: 'Chrome', 'Opera' or 'FireFox'. 'Chrome' is default
        @param version: '0.95'. Latest is default
        """
        for key in kwargs.keys():
            if key == "adaptive":
                self.adaptive = kwargs["adaptive"]
            elif key == "remote":
                self.remote = not kwargs["local"]
            elif key == "invisible":
                self.invisible = kwargs["invisible"]
            elif key == "logs":
                self.logs = kwargs["logs"]
            elif key == "windowSize":
                self.window_size = kwargs["windowSize"]
            elif key == 'remoteIP':
                self.remoteIP = kwargs["remoteIP"]
            elif key == "remotePort":
                self.remotePort = kwargs["remotePort"]
            elif key == "executablePath":
                self.executablePath = key["executablePath"]

    def Chrome(self):
        options = webdriver.ChromeOptions()
        options.add_argument(f"--window-size={self.window_size[0]},{self.window_size[1]}")
        if self.logs:
            options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        if self.adaptive:
            options.add_argument(
                '--user-agent="Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166"')
        self.options = options

    def runDriver(self):
        if self.browser == 'Chrome':
            self.Chrome()
        elif self.browser == 'Opera':
            pass
        elif self.browser == 'FireFox':
            pass

        if self.remote:
            self.driver = webdriver.Remote(
                command_executor=f'http://{self.remoteIP}:{self.remotePort}',
                options=self.options)
        else:
            if self.browser == 'Chrome':
                self.driver = webdriver.Chrome(
                    service=Service(self.executablePath),
                    options=self.options)

    def __del__(self):
        if self.driver is not None:
            self.driver.close()
            self.driver.quit()