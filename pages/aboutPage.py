from selenium.webdriver.common.by import By

import utility_methods


class AboutPage:
    def __init__(self, driver):
        self.driver = driver

        self.unique_element_loc = "//div[@id='about_greeting']"
        self.players_online_loc = "//div[contains(@class, 'gamers_online')]//parent::div[@class='online_stat']"
        self.players_ingame_loc = "//div[contains(@class, 'gamers_in_game')]//parent::div[@class='online_stat']"
        self.store_btn_loc = "//div[@class='supernav_container']//a[@data-tooltip-content='.submenu_store']"

    def is_unique_element_present(self):
        unique_element_list = self.driver.find_elements(
            By.XPATH, self.unique_element_loc
        )
        return len(unique_element_list) > 0

    def get_players_online_nb(self):
        players_online_obfuscated = self.driver.find_element(
            By.XPATH, self.players_online_loc
        )
        return utility_methods.extract_nb_of_players(players_online_obfuscated)

    def get_players_ingame_nb(self):
        players_ingame_obfuscated = self.driver.find_element(
            By.XPATH, self.players_ingame_loc
        )
        return utility_methods.extract_nb_of_players(players_ingame_obfuscated)

    def click_on_store_btn(self):
        store_button = self.driver.find_element(By.XPATH, self.store_btn_loc)
        store_button.click()
        # Import statement has to be here (and not at the top) to avoid circular dependency
        from pages.storePage import StorePage

        return StorePage(self.driver)
