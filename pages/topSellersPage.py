from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import utility_methods


class TopSellersPage:
    def __init__(self, driver):
        self.driver: WebDriver = driver
        self.wait_time = utility_methods.get_wait_time_data()

        # Locators relaying on text are not the best practice, but I could not find a better way,
        # especially since the site is so similar to https://store.steampowered.com/search/?term=
        self.unique_element_loc = (
            "//h2[contains(text(), 'Top') and contains(text(), 'Sellers')]"
        )
        self.collapsed_category_headers_loc = (
            "//div[contains(@class, 'block_content_inner') and contains(@style, 'none')]"
            "//preceding-sibling::div[@data-panel]"
        )
        self.checked_checkboxes_loc = "//span[contains(@class, 'checked')]"
        self.search_result_text_loc = "//div[@class='search_results_count']"
        self.search_result_rows_loc = "//div[@id='search_resultsRows']//child::a"

        # What a nice variable name!
        # In all seriousness I just wanted to emphasize the logic behind the locator -
        # - when the container is still loading search results, it contains attribute style=opacity:0.5,
        # so when this attribute disappears, it means the search results are ready
        self.search_result_container_not_in_loading_state_loc = (
            "//div[@id='search_result_container' and not(@style)]"
        )
        self.first_game_in_search_results_loc = "//div[@id='search_resultsRows']/a[1]"

    def is_unique_element_present(self):
        unique_element_list = self.driver.find_elements(
            By.XPATH, self.unique_element_loc
        )
        return len(unique_element_list) > 0

    def display_all_checkboxes(self):
        category_headers_to_click: list[WebElement] = self.driver.find_elements(
            By.XPATH, self.collapsed_category_headers_loc
        )
        # Unraveling categories from top to bottom, causes every category below the one being unravelled to move down.
        # As a result the remaining clicks do not hit their targets, which throws an error. By reversing the list, we
        # unravel from the bottom to the top, which does not cause any shifts in the layout of categories yet to be clicked.
        category_headers_to_click.reverse()
        for header in category_headers_to_click:
            wait = WebDriverWait(self.driver, self.wait_time)
            wait.until(EC.element_to_be_clickable(header))
            header.click()

    def check_required_checkboxes(self, required_checkboxes: dict):
        for chk in required_checkboxes.values():
            chk_loc = f"//span[@data-value='{chk}']"
            self.wait_for_search_results()
            self.driver.find_element(By.XPATH, chk_loc).click()

    def get_data_values_of_checked_checkboxes(self):
        checked_checkboxes = self.driver.find_elements(
            By.XPATH, self.checked_checkboxes_loc
        )
        return [element.get_attribute("data-value") for element in checked_checkboxes]

    def get_number_of_results(self):
        self.wait_for_search_results()
        wait = WebDriverWait(self.driver, self.wait_time)
        number_of_results = wait.until(
            EC.presence_of_element_located((By.XPATH, self.search_result_text_loc))
        )
        return utility_methods.extract_nb_of_results(number_of_results.text)

    def count_number_of_results(self):
        self.wait_for_search_results()
        search_result_rows = self.driver.find_elements(
            By.XPATH, self.search_result_rows_loc
        )
        return len(search_result_rows)

    def wait_for_search_results(self):
        wait = WebDriverWait(self.driver, self.wait_time)
        # Using only one wait was insufficient,worked only around 50% of the time
        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, self.search_result_container_not_in_loading_state_loc)
            )
        )
        wait.until(
            EC.invisibility_of_element((By.XPATH, "//div[@class='LoadingWrapper']"))
        )

    def get_data_from_first_game_in_search_results(self):
        self.wait_for_search_results()  # You never know from where this method may be called
        first_game_from_search_results = self.driver.find_element(
            By.XPATH, self.first_game_in_search_results_loc
        )
        return self.get_game_data_from_row(first_game_from_search_results)

    @staticmethod
    def get_game_data_from_row(game_item_node: WebElement) -> dict:
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
        first_game_from_search_results = self.driver.find_element(
            By.XPATH, self.first_game_in_search_results_loc
        )
        first_game_from_search_results.click()
        # Import statement has to be here (and not at the top) to avoid circular dependency;
        from pages.gamePage import GamePage

        return GamePage(self.driver)
