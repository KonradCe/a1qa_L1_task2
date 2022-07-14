from singleton_webdriver import SingletonWebDriver as Swd
import utility_methods


class BrowserUtil:

    @staticmethod
    def go_to_store_page():
        store_url = utility_methods.get_store_url()
        Swd.get_driver().get(store_url)
