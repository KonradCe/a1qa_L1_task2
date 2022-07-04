import pytest
import pages
import pages.storePage
import utility_methods
from singletonWebDriver import SingletonWebDriver


@pytest.fixture()
def driver_setup_teardown():
    chrome_parameters = utility_methods.get_chrome_parameters()
    driver = SingletonWebDriver(chrome_parameters).driver
    yield driver
    driver.quit()


def test_case1(driver_setup_teardown):
    driver = driver_setup_teardown
    # STEP1 - Navigate to store page -> store page is open
    store_page = pages.storePage.StorePage(driver)
    error_message_step1 = "opening store page should result in store page being open"
    assert store_page.is_unique_element_present(), error_message_step1

    # STEP2 - Click on ABOUT button	-> About page is open
    about_page = store_page.click_on_about_btn()
    error_message_step2 = "opening about page should result in about page being open"
    assert about_page.is_unique_element_present(), error_message_step2

    # STEP3 - Compare number of players online and in-game -> Number of in-game players is less than number of players online
    players_online = about_page.get_players_online_nb()
    players_ingame = about_page.get_players_ingame_nb()
    error_message_step3 = (
        "Number of in-game players is larger than number of players online"
    )
    assert players_ingame < players_online, error_message_step3

    # STEP4 - Click on STORE button -> Store page is open
    store_page = about_page.click_on_store_btn()
    error_message_step4 = error_message_step1
    assert store_page.is_unique_element_present(), error_message_step4


if __name__ == "__main__":
    for d in driver_setup_teardown():
        test_case1(d)
