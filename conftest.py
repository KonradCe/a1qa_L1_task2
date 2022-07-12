import pytest

import utility_methods
from singletonWebDriver import SingletonWebDriver


@pytest.fixture()
def driver_setup_teardown():
    chrome_parameters = utility_methods.get_chrome_parameters_data()
    driver = SingletonWebDriver().get_driver(chrome_parameters)
    driver.get("https://store.steampowered.com/")
    yield driver
    driver.quit()
    SingletonWebDriver().unassign_driver()
