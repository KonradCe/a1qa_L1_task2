import pytest
import pages
import pages.storePage
import utility_methods
from singletonWebDriver import SingletonWebDriver


@pytest.fixture()
def driver_setup_teardown():
    chrome_parameters = utility_methods.get_chrome_parameters_data()
    driver = SingletonWebDriver().get_driver(chrome_parameters)
    yield driver
    driver.quit()
    SingletonWebDriver().unassign_driver()


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


def test_case2(driver_setup_teardown):
    driver = driver_setup_teardown
    # STEP1 - Navigate to store page -> store page is open
    store_page = pages.storePage.StorePage(driver)
    error_message_step1 = "opening store page should result in store page being open"
    assert store_page.is_unique_element_present(), error_message_step1

    # STEP2 - Move pointer to 'New & Noteworthy' at page's menu. Using explicit waits wait until popup menu shows up.
    # Click 'Top Sellers' option in that menu -> Page with Top Sellers products is open
    top_sellers_page = store_page.click_on_topsellers_from_noteworthy_pulldown()
    error_message_step2 = (
        "opening top sellers page should result in top sellers page being open"
    )
    assert top_sellers_page.is_unique_element_present(), error_message_step2

    # STEP3 - In menu on the right choose 'Action', 'LAN Co-op' and 'SteamOS + Linux' checkboxes ->
    # All three checkboxes are checked
    # Number of results matching your search equals to number of games in games list
    top_sellers_page.display_all_checkboxes()
    checkboxes = utility_methods.get_filter_checkboxes_data()
    top_sellers_page.check_proper_checkboxes(checkboxes)
    error_message_step3a = "not all required checkboxes were checked"
    assert set((top_sellers_page.get_data_values_of_checked_checkboxes())).issubset(
        set(checkboxes.values())
    ), error_message_step3a

    print(top_sellers_page.get_number_of_results())
    print(top_sellers_page.count_number_of_results())
    assert (
        top_sellers_page.get_number_of_results()
        == top_sellers_page.count_number_of_results()
    )


if __name__ == "__main__":
    main_driver = SingletonWebDriver().get_driver(
        utility_methods.get_chrome_parameters_data()
    )
    test_case2(main_driver)
