import pytest

import utility_methods
from singleton_webdriver import SingletonWebDriver as Swd
from browser_util import BrowserUtil


@pytest.fixture()
def driver_setup_teardown():
    chrome_parameters = utility_methods.get_chrome_parameters_data()
    driver = Swd.get_driver(chrome_parameters)
    BrowserUtil.go_to_store_page()
    yield driver
    driver.quit()
    Swd.unassign_driver()
