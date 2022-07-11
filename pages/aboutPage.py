from selenium.webdriver.common.by import By

import utility_methods
from singletonWebDriver import SingletonWebDriver as SWD


class AboutPage:
    UNIQUE_ELEMENT_LOC = By.XPATH, "//div[@id='about_greeting']"
    PLAYERS_ONLINE_LOC = (
        By.XPATH,
        "//div[contains(@class, 'gamers_online')]//parent::div[@class='online_stat']",
    )
    PLAYERS_INGAME_LOC = (
        By.XPATH,
        "//div[contains(@class, 'gamers_in_game')]//parent::div[@class='online_stat']",
    )
    STORE_BTN_LOC = (
        By.XPATH,
        "//div[@class='supernav_container']//a[@data-tooltip-content='.submenu_store']",
    )

    def is_unique_element_present(self):
        unique_element_list = SWD.get_driver().find_elements(*self.UNIQUE_ELEMENT_LOC)
        return len(unique_element_list) > 0

    def get_players_online_nb(self):
        players_online_obfuscated = SWD.get_driver().find_element(
            *self.PLAYERS_ONLINE_LOC
        )
        return utility_methods.extract_nb_of_players(players_online_obfuscated)

    def get_players_ingame_nb(self):
        players_ingame_obfuscated = SWD.get_driver().find_element(
            *self.PLAYERS_INGAME_LOC
        )
        return utility_methods.extract_nb_of_players(players_ingame_obfuscated)

    def click_on_store_btn(self):
        store_button = SWD.get_driver().find_element(*self.STORE_BTN_LOC)
        store_button.click()
