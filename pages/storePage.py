from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import utility_methods
from singletonWebDriver import SingletonWebDriver as SWD


class StorePage:
    ABOUT_BTN_LOC = (
        By.XPATH,
        "//div[@id='global_header']//a[contains(@href,'about') and @class='menuitem']",
    )
    UNIQUE_ELEMENT_LOC = (By.XPATH, "//div[@class='home_page_content']")
    NOTEWORTHY_BTN_LOC = (By.XPATH, "//div[@id='noteworthy_tab']")
    TOPSELLERS_BTN_LOC = (By.XPATH, "//a[contains(@href,'topsellers')]")

    def __init__(self):
        self.wait_time = utility_methods.get_wait_time_data()

    def is_unique_element_present(self):
        unique_element_list = SWD.get_driver().find_elements(*self.UNIQUE_ELEMENT_LOC)
        # TODO: change comparing list length to bool(list)
        return len(unique_element_list) > 0

    def click_on_about_btn(self):
        about_page_btn = SWD.get_driver().find_element(*self.ABOUT_BTN_LOC)
        about_page_btn.click()

    def click_on_topsellers_from_noteworthy_pulldown(self):
        # Hover over button
        new_and_noteworthy_pulldown = SWD.get_driver().find_element(
            *self.NOTEWORTHY_BTN_LOC
        )
        hover_over_new_and_noteworthy = ActionChains(SWD.get_driver()).move_to_element(
            new_and_noteworthy_pulldown
        )
        hover_over_new_and_noteworthy.perform()

        wait = WebDriverWait(SWD.get_driver(), self.wait_time)
        topsellers_btn = wait.until(EC.element_to_be_clickable(self.TOPSELLERS_BTN_LOC))
        topsellers_btn.click()
