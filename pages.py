class StorePage:
    def __init__(self, driver):
        self.__about_btn_loc = None
        self.__unique_element_loc = None
        self.__driver = driver

    def is_unique_element_present(self):
        pass

    def click_on_about_btn(self):
        # return AboutPage(self.__driver)
        pass


class AboutPage:
    def __init__(self, driver):
        self.__unique_element_loc = None
        self.__players_online_loc = None
        self.__players_ingame_loc = None
        self.__store_btn_loc = None
        self.driver = driver

    def get_players_online_nb(self):
        pass

    def get_players_ingame_nb(self):
        pass

    def click_on_store_btn(self):
        pass



class TopSellersPage:
    pass

