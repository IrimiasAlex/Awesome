from . import OracleForms
from Emerson.variables import std_15s_wait, std_60s_wait

class Forms(OracleForms):
    def __init__(self, *args, **kwargs):
        OracleForms.__init__(self, *args, **kwargs)
        self.oracle_forms_elements = self.actions.read_configuration("data/oracle_forms_config/oracle_close_form_elements.json")
        self.error_element_locator = "role:internal frame"
        self.error_element_attribute = "name"
    
    def check_close_form_screen_exists(self, timeout: int):
        element_exists = False
        element = None
        try:
            oracle_forms_elements = self.oracle_forms_elements
            element = self.get_element_by_attribute(
                self.error_element_locator, self.error_element_attribute,
                oracle_forms_elements["label_close_form"], timeout
            )
            if element is not None:
                element_exists = True
        except Exception as ex:
            raise ex
        return element_exists

    def click_button_by_name(self, window_title: str, button_name: str):
        """
        Clicks a button in 'Close Form' screen by it's name
        @param window_title: The Oracle Close Form application window title name
        @param button_name: Must be one of this possible values:
        "button_yes", "button_no"
        """
        try:
            window_title = window_title.strip()
            button_name = button_name.strip().lower()
            oracle_forms_elements = self.oracle_forms_elements
            element = None
            if button_name not in oracle_forms_elements:
                raise Exception(
                    "The button with the name: "
                    + button_name
                    + " doesn't exists in 'Close Form' screen"
                )
            element = self.get_element_by_attribute(
                self.error_element_locator, self.error_element_attribute,
                oracle_forms_elements["label_close_form"], std_15s_wait
            )
            if element is None:
               raise Exception("Cannot find 'Close Form' screen")
            keys_combinations_button = self.actions.split_string_to_list(
                oracle_forms_elements[button_name], ","
            )
            self.java.select_window(
                title=window_title, bring_foreground=True, timeout=std_60s_wait
            )
            self.send_keys(*keys_combinations_button)
        except Exception as ex:
            raise ex
        
    
