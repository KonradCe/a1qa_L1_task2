from selenium.webdriver.common.by import By

import utility_methods
from singleton_webdriver import SingletonWebDriver as Swd


class GamePage:
    UNIQUE_ELEMENT_LOC = (By.XPATH, "//div[@id='game_area_description']")
    GAME_TITLE_LOC = (By.XPATH, "//div[@id='appHubAppName']")
    GAME_RELEASE_DATE_LOC = (By.XPATH, "//div[@class='date']")
    GAME_PRICE_LOC = (
        By.XPATH,
        "//div[@class='game_area_purchase_game']//div[@data-price-final]",
    )

    def is_open(self):
        unique_element_list = Swd.get_driver().find_elements(*self.UNIQUE_ELEMENT_LOC)
        return bool(unique_element_list)

    def get_game_data(self) -> dict:
        game_title = Swd.get_driver().find_element(*self.GAME_TITLE_LOC).text
        game_release_date = (
            Swd.get_driver().find_element(*self.GAME_RELEASE_DATE_LOC).text
        )

        game_price_raw = (
            Swd.get_driver()
            .find_element(*self.GAME_PRICE_LOC)
            .get_attribute("data-price-final")
        )
        game_price = utility_methods.calculate_game_price_from_attribute(game_price_raw)

        return utility_methods.create_dict_from_game_attr(
            title=game_title, release_date=game_release_date, price=game_price
        )
