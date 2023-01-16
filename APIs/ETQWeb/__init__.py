from Browser import SupportedBrowsers
from Emerson.GeneralActions import GeneralActions
from Emerson.variables import std_60s_wait, root_directory
from RPA.Browser.Playwright import Playwright


class ETQWeb(Playwright):
    def __init__(self, *args, **kwargs):
        Playwright.__init__(self, *args, **kwargs)
        self.actions = GeneralActions()
        self.browser_instance = ""
        self.page_instance = ""
        self.config_file_path = None
        self.library_timeout = kwargs.pop("timeout", std_60s_wait)
        self.etq_elements = None

    def open_google_chrome(self):
        try:
            self.browser_instance = self.new_browser(
                                               browser=SupportedBrowsers.chromium, headless=False
            )
            self.new_context(acceptDownloads=True)
            self.page_instance = self.new_page()
        except Exception as ex:
            raise ex
        
    def etq_get_browser_ids(self):
        try:
            return self.get_browser_ids()
        except Exception as ex:
            raise ex

    def close_google_chrome(self):
        try:
            self.close_browser(browser='ALL')
        except Exception as ex:
            raise ex