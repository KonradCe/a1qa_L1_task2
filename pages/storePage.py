from selenium import webdriver
from selenium.webdriver.common.by import By


class StorePage:
    driver: webdriver.Chrome

    def __init__(self, driver):
        self.URL = "https://store.steampowered.com/"
        self.driver = driver
        self.driver.get(self.URL)

        self.about_btn_loc = "//div[@id='global_header']//a[contains(@href,'about') and @class='menuitem']"
        self.unique_element_loc = "//div[@class='home_page_content']"

    def is_unique_element_present(self):
        unique_element_list = self.driver.find_elements(
            By.XPATH, self.unique_element_loc
        )
        return len(unique_element_list) > 0

    def click_on_about_btn(self):
        about_page_btn = self.driver.find_element(By.XPATH, self.about_btn_loc)
        about_page_btn.click()
        # Import statement has to be here (and not in the top) to avoid circular dependency; I suspect adding models would resolve this issue
        from pages.aboutPage import AboutPage

        return AboutPage(self.driver)
