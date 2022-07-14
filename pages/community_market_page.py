from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import utility_methods
from singleton_webdriver import SingletonWebDriver as Swd


class CommunityMarketPage:
    UNIQUE_ELEMENT_LOC = By.XPATH, "//div[@id='myMarketTabs']"
    SHOW_ADV_OPT_BTN_LOC = By.XPATH, "//div[@class='market_search_advanced_button']"
    ADV_SEARCH_UNIQUE_ELEMENT_LOC = By.XPATH, "//div[@class='newmodal'  and not(contains(@style, 'display: none'))]"
    ADV_SEARCH_ALL_GAMES_LIST_LOC = By.XPATH, "//div[@id='app_option_0_selected']"
    ADV_SEARCH_SEARCH_BTN_LOC = By.XPATH, "//div[contains(@onclick, 'market_advanced_search')]"

    def __init__(self):
        self.wait_time = utility_methods.get_wait_time_data()

    def is_open(self):
        return bool(Swd.get_driver().find_elements(*self.UNIQUE_ELEMENT_LOC))

    def click_on_show_adv_opt_btn(self):
        adv_opt_btn = Swd.get_driver().find_element(*self.SHOW_ADV_OPT_BTN_LOC)
        adv_opt_btn.click()

    def is_adv_search_open(self):
        return bool(Swd.get_driver().find_elements(*self.ADV_SEARCH_UNIQUE_ELEMENT_LOC))

    def fill_advance_search_params(self):
        params: dict = utility_methods.get_advance_search_params()
        # select game from the list
        Swd.get_driver().find_element(*self.ADV_SEARCH_ALL_GAMES_LIST_LOC).click()
        game_id = params['Game']['Dota 2']
        adv_search_specific_game_loc = By.XPATH, f"//div[@id='app_option_{game_id}']"
        Swd.get_driver().find_element(*adv_search_specific_game_loc).click()

        # select hero
        wait = WebDriverWait(Swd.get_driver(), self.wait_time)
        hero_list_loc = By.XPATH, "//select[contains(@name, 'category_570_He')]"
        hero_list = wait.until(EC.element_to_be_clickable(hero_list_loc))
        hero_list.click()
        Swd.get_driver().find_element(*hero_list_loc).click()
        hero_loc = By.XPATH, "//option[@value='tag_npc_dota_hero_life_stealer']"
        Swd.get_driver().find_element(*hero_loc).click()

        # select rarity
        rarity_loc = By.XPATH, "//input[@id='tag_570_Rarity_Rarity_Immortal']"
        Swd.get_driver().find_element(*rarity_loc).click()

        # fill out search phrase
        adv_search_input_box_loc = By.XPATH, "//input[@id='advancedSearchBox']"
        adv_search_input_box = Swd.get_driver().find_element(*adv_search_input_box_loc)
        adv_search_input_box.send_keys(params["search_for"])


    def click_on_advance_search_btn(self):
        Swd.get_driver().find_element(*self.ADV_SEARCH_SEARCH_BTN_LOC).click()









