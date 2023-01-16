from . import Web, keyword
from robot.libraries.BuiltIn import BuiltIn
from Emerson.variables import std_max_retries, std_1s_wait, std_10s_wait
from Emerson.GeneralActions import GeneralActions

class Okta(Web):
    
    def __init__(self, *args, **kwargs):
        Web.__init__(self, *args, **kwargs)
        self.builtin = BuiltIn()
        self.okta_login_web_elements = self.actions.read_configuration("data/okta_web_config/okta_web_config_elements.json")
    
    @keyword    
    def login_okta(self,
                   user_name: str,
                   password: str) -> None:
        try:
            user_name = user_name.strip()
            password = password.strip()
            parameters = [self.okta_login_web_elements.get("user_name_input_locator"), std_10s_wait]
            login_screen_exists = GeneralActions.retry_function_and_ignore_error(std_max_retries,
                                                                                 std_1s_wait,
                                                                                 self.wait_until_element_is_visible,
                                                                                 *parameters)
            if login_screen_exists == None:
                self.input_text_when_element_is_visible(locator=self.okta_login_web_elements.get("user_name_input_locator"),
                                                        text=user_name)
                self.click_button_when_visible(locator=self.okta_login_web_elements.get("next_button_locator"))
                parameters = [self.okta_login_web_elements.get("sign_in_button_locator"), std_10s_wait]
                sign_in_button_exists = GeneralActions.retry_function_and_ignore_error(std_max_retries,
                                                                                       std_1s_wait,
                                                                                       self.wait_until_element_is_visible,
                                                                                       *parameters)
                if sign_in_button_exists == None:
                    self.input_password(locator=self.okta_login_web_elements.get("user_password_input_locator"),
                                        password=password,
                                        clear=True)
                    self.click_button_when_visible(locator=self.okta_login_web_elements.get("sign_in_button_locator"))
        except Exception as ex:
            raise ex