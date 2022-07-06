from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

import utility_methods


class GamePage:
    def __init__(self, driver):
        self.driver: WebDriver = driver
        self.unique_element_loc = "//div[@id='game_area_description']"
        self.game_title_loc = "//div[@id='appHubAppName']"
        self.game_release_date_loc = "//div[@class='date']"
        self.game_price_loc = (
            "//div[@class='game_area_purchase_game']//div[@data-price-final]"
        )

    def is_unique_element_present(self):
        return len(self.driver.find_elements(By.XPATH, self.unique_element_loc)) > 0

    def get_game_data(self) -> dict():
        game_title = self.driver.find_element(By.XPATH, self.game_title_loc).text
        game_release_date = self.driver.find_element(
            By.XPATH, self.game_release_date_loc
        ).text

        game_price_raw = self.driver.find_element(
            By.XPATH, self.game_price_loc
        ).get_attribute("data-price-final")
        game_price = utility_methods.calculate_game_price_from_attribute(game_price_raw)

        return utility_methods.create_dict_from_game_attr(
            title=game_title, release_date=game_release_date, price=game_price
        )
