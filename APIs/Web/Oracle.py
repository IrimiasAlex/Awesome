from time import sleep
from . import Web, keyword
from Emerson.variables import std_2s_wait, std_5s_wait
from RPA.Windows import Windows

class Oracle(Web):
    def __init__(self, *args, **kwargs):
        Web.__init__(self, *args, **kwargs)
        self.oracle_login_web_elements = self.actions.read_configuration("data/oracle_web_config/oracle_login_elements.json")
        self.windows = Windows()

    @keyword
    def login_into_oracle_chrome(
        self, oracle_responsibility_link: str, oracle_logout_link: str, user_name: str, password: str, chrome_tab_title: str = None
    ) -> None:
        try:
            oracle_logout_link = oracle_logout_link.strip()
            oracle_responsibility_link = oracle_responsibility_link.strip()
            user_name = user_name.strip()
            password = password.strip()
            if chrome_tab_title is not None:
                chrome_tab_title = chrome_tab_title.strip()
                chrome_tab_title = f'name:"{chrome_tab_title}"'
            else:
                chrome_tab_title = self.oracle_login_web_elements.get("oracle_default_chrome_tab_title")
            self.go_to(oracle_logout_link)
            self.delete_all_cookies()
            self.go_to(oracle_responsibility_link)
            self.enter_oracle_credentials(user_name, password)
            sleep(std_5s_wait)
            self.go_to(oracle_responsibility_link)
            sleep(std_2s_wait)
            try:
                window_control = self.windows.get_element(locator=chrome_tab_title,
                                                          search_depth=self.oracle_login_web_elements.get("default_search_depth"))
                self.windows.foreground_window(window_control)
                keep_element = self.windows.get_element(locator=self.oracle_login_web_elements.get("keep_button_locator"), 
                                                        search_depth=self.oracle_login_web_elements.get("default_search_depth"),
                                                        timeout=std_5s_wait)
                self.windows.click(keep_element)
            except Exception:
                pass
        except Exception as ex:
            raise ex

    @keyword
    def enter_oracle_credentials(self, user_name: str, password: str):
        try:
            self.wait_until_element_is_visible(
                self.oracle_login_web_elements["user_name_input_locator"],
                self.library_timeout,
            )
            try:
                self.wait_until_element_is_enabled(
                    self.oracle_login_web_elements["user_name_input_locator"],
                    std_5s_wait,
                )
                self.input_text_when_element_is_visible(
                    self.oracle_login_web_elements["user_name_input_locator"], user_name
                )
            except:
                pass
            self.wait_until_element_is_visible(
                self.oracle_login_web_elements["password_input_locator"],
                self.library_timeout,
            )
            self.wait_until_element_is_enabled(
                self.oracle_login_web_elements["password_input_locator"],
                self.library_timeout,
            )
            self.input_text(
                self.oracle_login_web_elements["password_input_locator"], password
            )
            self.wait_until_element_is_visible(
                self.oracle_login_web_elements["login_button_locator"],
                self.library_timeout,
            )
            self.wait_until_element_is_enabled(
                self.oracle_login_web_elements["login_button_locator"],
                self.library_timeout,
            )
            self.click_element_when_visible(
                self.oracle_login_web_elements["login_button_locator"]
            )
        except Exception as ex:
            raise ex