import utility_methods
from pages.aboutPage import AboutPage
from pages.gamePage import GamePage
from pages.storePage import StorePage
from pages.topSellersPage import TopSellersPage
from singletonWebDriver import SingletonWebDriver


def test_case1(driver_setup_teardown):
    driver = driver_setup_teardown

    # STEP1: Navigate to store page -> store page is open
    store_page = StorePage()
    error_message_step1 = "opening store page should result in store page being open"
    assert store_page.is_unique_element_present(), error_message_step1

    # STEP2: Click on ABOUT button -> About page is open
    store_page.click_on_about_btn()
    about_page = AboutPage()
    error_message_step2 = "opening about page should result in about page being open"
    assert about_page.is_unique_element_present(), error_message_step2

    # STEP3: Compare number of players online and in-game -> Number of in-game players is less than number of players online
    players_online = about_page.get_players_online_nb()
    players_ingame = about_page.get_players_ingame_nb()
    error_message_step3 = (
        "Number of in-game players is larger than number of players online"
    )
    assert players_ingame < players_online, error_message_step3

    # STEP4: Click on STORE button -> Store page is open
    about_page.click_on_store_btn()
    store_page = StorePage()
    error_message_step4 = error_message_step1
    assert store_page.is_unique_element_present(), error_message_step4


def test_case2(driver_setup_teardown):
    driver = driver_setup_teardown

    # STEP1: Navigate to store page -> store page is open
    store_page = StorePage()
    error_message_step1 = "opening store page should result in store page being open"
    assert store_page.is_unique_element_present(), error_message_step1

    # STEP2: Move pointer to 'New & Noteworthy' at page's menu. Using explicit waits wait until popup menu shows up.
    # Click 'Top Sellers' option in that menu -> Page with Top Sellers products is open
    store_page.click_on_topsellers_from_noteworthy_pulldown()
    top_sellers_page = TopSellersPage()
    error_message_step2 = (
        "opening top sellers page should result in top sellers page being open"
    )
    assert top_sellers_page.is_unique_element_present(), error_message_step2

    # STEP3: In menu on the right choose 'Action', 'LAN Co-op' and 'SteamOS + Linux' checkboxes ->
    # All three checkboxes are checked
    # Number of results matching your search equals to number of games in games list
    top_sellers_page.display_all_checkboxes()
    checkboxes = utility_methods.get_filter_checkboxes_data()
    top_sellers_page.check_required_checkboxes(checkboxes)
    error_message_step3a = "not all required checkboxes were checked"
    assert set((top_sellers_page.get_data_values_of_checked_checkboxes())).issubset(
        set(checkboxes.values())
    ), error_message_step3a

    error_message_step3b = (
        "number of results from text does not equal number of items in search results"
    )
    assert (
        top_sellers_page.get_number_of_results()
        == top_sellers_page.count_number_of_results()
    ), error_message_step3b

    # STEP6: From list get first game's name, release date and price
    game_data_from_search_results = (
        top_sellers_page.get_data_from_first_game_in_search_results()
    )

    # STEP7: click on the first game in the list ->
    # page with game's description is open
    # Game's data (name, release date and price) are equal to the ones from step #6
    top_sellers_page.click_on_first_game_in_search_results()
    garrys_game_page = GamePage()
    error_message_step7a = (
        "opening game details page should result in game details page being open"
    )
    assert garrys_game_page.is_unique_element_present(), error_message_step7a

    game_data_from_game_page = garrys_game_page.get_game_data()
    error_message_step7b = "one game should have the same title, release date and price on search results page and on game details page"
    assert (
        game_data_from_search_results == game_data_from_game_page
    ), error_message_step7b


# For debugging purpose only
if __name__ == "__main__":
    main_driver = SingletonWebDriver().get_driver(
        utility_methods.get_chrome_parameters_data()
    )
    main_driver.get("https://store.steampowered.com/")
    test_case1(main_driver)
