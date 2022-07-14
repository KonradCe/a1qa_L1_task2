import pytest

import utility_methods
from browser_util import BrowserUtil
from singleton_webdriver import SingletonWebDriver as Swd


@pytest.fixture()
def driver_setup_teardown():
    chrome_parameters = utility_methods.get_chrome_parameters_data()
    Swd.get_driver(chrome_parameters)
    BrowserUtil.go_to_store_page()
    yield
    Swd.get_driver().quit()
    Swd.unassign_driver()
