from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


class Singleton(type):
    def __init__(self, *args, **kwargs):
        self.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if self.__instance is None:
            self.__instance = super().__call__(*args, **kwargs)
            return self.__instance
        else:
            return self.__instance


class SingletonWebDriver(metaclass=Singleton):
    __driver = None

    def get_driver(self, parameters=None):
        if self.__driver is None:
            options = webdriver.ChromeOptions()
            if parameters is not None:
                for p in parameters:
                    options.add_argument(p)
            self.__driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()), options=options
            )
        return self.__driver

    def unassign_driver(self):
        self.__driver = None
