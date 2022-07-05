from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import utility_methods


class TopSellersPage:
    def __init__(self, driver):
        self.driver: WebDriver = driver
        # Locators relaying on text are not the best practice, but I could not find a better way,
        # especially since the site is so similar to https://store.steampowered.com/search/?term=
        self.unique_element_loc = (
            "//h2[contains(text(), Top) and contains(text(), Sellers)]"
        )
        self.collapsed_category_headers_loc = (
            "//div[contains(@class, 'block_content_inner') and contains(@style, 'none')]"
            "//preceding-sibling::div[@data-panel]"
        )
        self.search_result_text_loc = "//div[@class='search_results_count']"
        self.search_result_rows_loc = "//div[@id='search_resultsRows']//child::a"

    def is_unique_element_present(self):
        unique_element_list = self.driver.find_elements(
            By.XPATH, self.unique_element_loc
        )
        return len(unique_element_list) > 0

    def display_all_checkboxes(self):
        category_headers_to_click: list[WebElement] = self.driver.find_elements(
            By.XPATH, self.collapsed_category_headers_loc
        )
        # Unraveling categories from top to bottom, causes every category below the one being unravelled to shift down.
        # As a result the remaining clicks do not hit their targets, which throws an error. By reversing the list, we
        # unravel from the bottom to the top, which do not couses any shifts in the layout of categories yet to be clicked.
        category_headers_to_click.reverse()
        for header in category_headers_to_click:
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.element_to_be_clickable(header))
            header.click()

    def check_proper_checkboxes(self, checkboxes_to_check: dict):
        for chk in checkboxes_to_check.values():
            chk_loc = f"//span[@data-value='{chk}']"
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.element_to_be_clickable((By.XPATH, chk_loc))).click()
            # self.driver.find_element(By.XPATH, chk_loc).click()

    def get_data_values_of_checked_checkboxes(self):
        checked_checkboxes_loc = "//span[contains(@class, 'checked')]"
        checked_checkboxes = self.driver.find_elements(By.XPATH, checked_checkboxes_loc)
        return [element.get_attribute("data-value") for element in checked_checkboxes]

    def get_number_of_results(self):
        wait = WebDriverWait(self.driver, 10)
        number_of_results = wait.until(
            EC.presence_of_element_located((By.XPATH, self.search_result_text_loc))
        )

        return utility_methods.extract_nb_of_results(number_of_results.text)

    def count_number_of_results(self):
        search_result_rows = self.driver.find_elements(
            By.XPATH, self.search_result_rows_loc
        )
        return len(search_result_rows)
