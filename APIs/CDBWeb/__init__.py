from Emerson.GeneralActions import GeneralActions
from Emerson.variables import std_60s_wait, root_directory
from RPA.Browser.Selenium import Selenium
from SeleniumLibrary.base import keyword


class CDBWeb(Selenium):
    def __init__(self, *args, **kwargs):
        Selenium.__init__(self, *args, **kwargs)
        self.actions = GeneralActions()
        self.instance_number = -1
        self.config_file_path = None
        self.oracle_login_web_elements = None
        self.library_timeout = kwargs.pop("timeout", std_60s_wait)
        
    def open_edge(self):
        try:
            # self.instance_number = self.open_available_browser(
            #     use_profile=True, maximized=True, headless=False, browser_selection="Edge,Edge,edge"
            # )
            self.instance_number = self.open_user_browser(
                url="http://web400/CustomerDB/"
            )
        except Exception as ex:
            raise ex

    def close_edge(self):
        try:
            self.close_browser(browser='ALL')
        except Exception as ex:
            raise ex