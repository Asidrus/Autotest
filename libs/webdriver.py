from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from config import downloads_path


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
        @param browser: 'Chrome', 'Opera' or 'Firefox'. 'Chrome' is default
        @param version: '0.95'. Latest is default
        """
        for key in kwargs.keys():
            if key == "adaptive":
                self.adaptive = kwargs["adaptive"]
            elif key == "remote":
                self.remote = kwargs["remote"]
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
                self.executablePath = kwargs["executablePath"]
            elif key == "browser":
                self.browser = kwargs["browser"]

    def setOptions(self):
        self.options.add_argument(f"--window-size={self.window_size[0]},{self.window_size[1]}")
        if self.logs:
            self.options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        if self.version != 'latest':
            self.options.set_capability("version", self.version)
        if self.adaptive:
            self.options.add_argument(
                '--user-agent="Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166"')
        # self.options.add_experimental_option('prefs', {'download.default_directory': downloads_path})

    def Chrome(self):
        self.options = webdriver.ChromeOptions()
        self.setOptions()

    def Firefox(self):
        self.options = webdriver.FirefoxOptions()
        self.setOptions()

    def Opera(self):
        pass

    def run(self):
        if self.browser == 'Chrome':
            self.Chrome()
        elif self.browser == 'Opera':
            self.Opera()
        elif self.browser == 'Firefox':
            self.Firefox()

        if self.remote:
            self.driver = webdriver.Remote(
                command_executor=f'http://{self.remoteIP}:{self.remotePort}/wd/hub/',
                options=self.options)
        else:
            if self.browser == 'Chrome':
                self.driver = webdriver.Chrome(
                    service=Service(self.executablePath),
                    options=self.options)
            elif self.browser == 'Firefox':
                print('start firefox')
                self.driver = webdriver.Firefox(
                    service=Service(self.executablePath),
                    options=self.options)

    def __del__(self):
        if self.driver is not None:
            self.driver.close()
            self.driver.quit()
