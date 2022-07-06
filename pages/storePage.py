from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import utility_methods


class StorePage:
    def __init__(self, driver):
        self.driver: WebDriver = driver
        self.wait_time = utility_methods.get_wait_time_data()

        self.about_btn_loc = "//div[@id='global_header']//a[contains(@href,'about') and @class='menuitem']"
        self.unique_element_loc = "//div[@class='home_page_content']"
        self.noteworthy_btn_loc = "//div[@id='noteworthy_tab']"
        self.noteworthy_flyout_tab_loc = "//div[@id='noteworthy_tab']"
        self.topsellers_btn_loc = "//a[contains(@href,'topsellers')]"

    def is_unique_element_present(self):
        unique_element_list = self.driver.find_elements(
            By.XPATH, self.unique_element_loc
        )
        return len(unique_element_list) > 0

    def click_on_about_btn(self):
        about_page_btn = self.driver.find_element(By.XPATH, self.about_btn_loc)
        about_page_btn.click()

        # Import statement has to be here (and not at the top) to avoid circular dependency;
        from pages.aboutPage import AboutPage

        return AboutPage(self.driver)

    def click_on_topsellers_from_noteworthy_pulldown(self):
        # Hover over button
        new_and_noteworthy_pulldown = self.driver.find_element(
            By.XPATH, self.noteworthy_btn_loc
        )
        hover_over_new_and_noteworthy = ActionChains(self.driver).move_to_element(
            new_and_noteworthy_pulldown
        )
        hover_over_new_and_noteworthy.perform()

        wait = WebDriverWait(self.driver, self.wait_time)
        topsellers_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, self.topsellers_btn_loc))
        )
        topsellers_btn.click()

        from pages.topSellersPage import TopSellersPage

        return TopSellersPage(self.driver)
