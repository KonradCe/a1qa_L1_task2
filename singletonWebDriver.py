from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


class Singleton(type):
    def __init__(cls, *args, **kwargs):
        cls.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if self.__instance is None:
            self.__instance = super().__call__(*args, **kwargs)
            return self.__instance
        else:
            return self.__instance


# This feels a bit 'hacky' but I don't know how get a new driver for every page in more elegant manner.
# (This could probably be solved by implementing Browser Factory)
class SingletonWebDriver(metaclass=Singleton):
    def __init__(self):
        self.__driver = None

    @staticmethod
    def create_new_driver(parameters):
        options = webdriver.ChromeOptions()
        if parameters is not None:
            for p in parameters:
                options.add_argument(p)
        return webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), options=options
        )

    def get_driver(self, parameters=None):
        if self.__driver is None:
            self.__driver = self.create_new_driver(parameters)
        return self.__driver

    def unassign_driver(self):
        self.__driver = None
