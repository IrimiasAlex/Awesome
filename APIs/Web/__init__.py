import os
from Emerson.GeneralActions import GeneralActions
from Emerson.variables import std_60s_wait, root_directory
from RPA.Browser.Selenium import Selenium
from SeleniumLibrary.base import keyword
from robot.libraries.BuiltIn import BuiltIn

class Web(Selenium):
    def __init__(self, *args, **kwargs):
        Selenium.__init__(self, *args, **kwargs)
        self.actions = GeneralActions()
        self.instance_number = -1
        self.config_file_path = None
        self.oracle_login_web_elements = None
        self.library_timeout = kwargs.pop("timeout", std_60s_wait)
        self.builtin = BuiltIn()

    @keyword
    def open_google_chrome(self,
                           preferences: dict = None) -> None:
        try:
            try:
                current_user = os.getlogin().strip()
                if preferences is None:
                    preferences = {
                        "download.default_directory" : f"C:/users/{current_user}/Downloads"
                    }
                elif preferences.get("download.default_directory") is None:
                    preferences["download.default_directory"] = f"C:/users/{current_user}/Downloads"
            except Exception as ex_preferences:
                self.builtin.log_to_console(f"kw: Open Google Chrome - Warning: Missing windows account user: {str(ex_preferences)}")
            self.instance_number = self.open_available_browser(
                url="about:blank", use_profile=True, maximized=True, headless=False, preferences=preferences
            )
        except Exception as ex:
            raise ex

    @keyword
    def close_google_chrome(self) -> None:
        try:
            self.close_all_browsers()
        except Exception as ex:
            raise ex
    
    @keyword
    def attach_google_chrome(self,
                             port: int,
                             alias: str = None) -> None:
        try:
            self.instance_number = self.attach_chrome_browser(
                port=port, alias=alias
                )
        except Exception as ex:
            raise ex