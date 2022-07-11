from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import utility_methods
from singletonWebDriver import SingletonWebDriver as SWD


class TopSellersPage:
    # Locators relaying on text are not the best practice, but I could not find a better way,
    # especially since the site is so similar to https://store.steampowered.com/search/?term=
    UNIQUE_ELEMENT_LOC = (
        By.XPATH,
        "//h2[contains(text(), 'Top') and contains(text(), 'Sellers')]",
    )
    COLLAPSED_CATEGORY_HEADERS_LOC = (
        By.XPATH,
        "//div[contains(@class, 'block_content_inner') and contains(@style, 'none')]//preceding-sibling::div[@data-panel]",
    )
    CHECKED_CHECKBOXES_LOC = (By.XPATH, "//span[contains(@class, 'checked')]")
    SEARCH_RESULT_TEXT_LOC = (By.XPATH, "//div[@class='search_results_count']")
    SEARCH_RESULT_ROWS_LOC = (By.XPATH, "//div[@id='search_resultsRows']//child::a")

    # What a nice variable name!
    # In all seriousness I just wanted to emphasize the logic behind the locator -
    # - when the container is still loading search results, it contains attribute style=opacity:0.5,
    # so when this attribute disappears, it means the search results are ready
    SEARCH_RESULT_CONTAINER_NOT_IN_LOADING_STATE_LOC = (
        By.XPATH,
        "//div[@id='search_result_container' and not(@style)]",
    )
    FIRST_GAME_IN_SEARCH_RESULTS_LOC = (
        By.XPATH,
        "//div[@id='search_resultsRows']/a[1]",
    )

    def __init__(self):
        self.wait_time = utility_methods.get_wait_time_data()

    def is_unique_element_present(self):
        unique_element_list = SWD.get_driver().find_elements(*self.UNIQUE_ELEMENT_LOC)
        return len(unique_element_list) > 0

    def display_all_checkboxes(self):
        category_headers_to_click: list[WebElement] = SWD.get_driver().find_elements(
            *self.COLLAPSED_CATEGORY_HEADERS_LOC
        )
        # Unraveling categories from top to bottom, causes every category below the one being unravelled to move down.
        # As a result the remaining clicks do not hit their targets, which throws an error. By reversing the list, we
        # unravel from the bottom to the top, which does not cause any shifts in the layout of categories yet to be clicked.
        category_headers_to_click.reverse()
        for header in category_headers_to_click:
            wait = WebDriverWait(SWD.get_driver(), self.wait_time)
            wait.until(EC.element_to_be_clickable(header))
            header.click()

    def check_required_checkboxes(self, required_checkboxes: dict):
        for chk in required_checkboxes.values():
            chk_loc = f"//span[@data-value='{chk}']"
            self.wait_for_search_results()
            SWD.get_driver().find_element(By.XPATH, chk_loc).click()

    def get_data_values_of_checked_checkboxes(self):
        checked_checkboxes = SWD.get_driver().find_elements(
            *self.CHECKED_CHECKBOXES_LOC
        )
        return [element.get_attribute("data-value") for element in checked_checkboxes]

    def get_number_of_results(self):
        self.wait_for_search_results()
        wait = WebDriverWait(SWD.get_driver(), self.wait_time)
        number_of_results = wait.until(
            EC.presence_of_element_located(self.SEARCH_RESULT_TEXT_LOC)
        )
        return utility_methods.extract_nb_of_results(number_of_results.text)

    def count_number_of_results(self):
        self.wait_for_search_results()
        search_result_rows = SWD.get_driver().find_elements(
            *self.SEARCH_RESULT_ROWS_LOC
        )
        return len(search_result_rows)

    def wait_for_search_results(self):
        wait = WebDriverWait(SWD.get_driver(), self.wait_time)
        # Using only one wait was insufficient,worked only around 50% of the time
        wait.until(
            EC.presence_of_element_located(
                self.SEARCH_RESULT_CONTAINER_NOT_IN_LOADING_STATE_LOC
            )
        )
        wait.until(
            EC.invisibility_of_element((By.XPATH, "//div[@class='LoadingWrapper']"))
        )

    def get_data_from_first_game_in_search_results(self):
        self.wait_for_search_results()  # You never know from where this method may be called
        first_game_from_search_results = SWD.get_driver().find_element(
            *self.FIRST_GAME_IN_SEARCH_RESULTS_LOC
        )
        return self.get_game_data_from_row(first_game_from_search_results)

    def get_game_data_from_row(self, game_item_node: WebElement) -> dict:
        game_title_loc = "//span[@class='title']"
        game_title = game_item_node.find_element(By.XPATH, game_title_loc).text

        game_release_date_loc = "//div[contains(@class, 'search_released')]"
        game_release_date = game_item_node.find_element(
            By.XPATH, game_release_date_loc
        ).text

        game_price_loc = "//div[@data-price-final]"
        game_price_raw = game_item_node.find_element(
            By.XPATH, game_price_loc
        ).get_attribute("data-price-final")
        game_price = utility_methods.calculate_game_price_from_attribute(game_price_raw)

        return utility_methods.create_dict_from_game_attr(
            title=game_title, release_date=game_release_date, price=game_price
        )

    def click_on_first_game_in_search_results(self):
        self.wait_for_search_results()
        first_game_from_search_results = SWD.get_driver().find_element(
            *self.FIRST_GAME_IN_SEARCH_RESULTS_LOC
        )
        first_game_from_search_results.click()
