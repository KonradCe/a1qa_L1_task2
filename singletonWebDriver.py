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


class SingletonWebDriver(metaclass=Singleton):
    __driver = None

    @staticmethod
    def create_new_driver(parameters):
        options = webdriver.ChromeOptions()
        if parameters is not None:
            for p in parameters:
                options.add_argument(p)
        return webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), options=options
        )

    @classmethod
    def get_driver(cls, parameters=None):
        if cls.__driver is None:
            cls.__driver = cls.create_new_driver(parameters)
        return cls.__driver

    @classmethod
    def unassign_driver(cls):
        cls.__driver = None
