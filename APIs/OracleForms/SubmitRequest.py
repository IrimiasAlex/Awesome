from . import OracleForms
from Emerson.variables import std_15s_wait, std_60s_wait

class SubmitRequest(OracleForms):
    def __init__(self, *args, **kwargs):
        OracleForms.__init__(self, *args, **kwargs)
        self.oracle_forms_elements = self.actions.read_configuration("data/oracle_forms_config/oracle_submit_request_elements.json")
        
    def check_submit_request_screen_exists(self, timeout: int):
        element_exists = False
        try:
            oracle_forms_elements = self.oracle_forms_elements
            element_exists = self.wait_until_element_exists(
                oracle_forms_elements["window_submit_request"], timeout
            )
        except Exception as ex:
            raise ex
        return element_exists

    def click_button_by_name(self, window_title: str, button_name: str):
        """
        Clicks a button in 'Submit Request' screen by it's name
        @param window_title: The Oracle Forms application window title name
        @param button_name: Must be one of this possible values:
        "button_submit_request", "button_tab", "button_close_form"
        """
        try:
            window_title = window_title.strip()
            button_name = button_name.strip().lower()
            oracle_forms_elements = self.oracle_forms_elements
            if button_name not in oracle_forms_elements:
                raise Exception(
                    "The button with the name: "
                    + button_name
                    + " doesn't exists in 'Submit Request' screen"
                )
            element_exists = self.wait_until_element_exists(oracle_forms_elements['window_submit_request'], std_15s_wait)
            if(not element_exists):
               raise Exception("Cannot find 'Submit Request' screen")
            keys_combinations_button = self.actions.split_string_to_list(
                oracle_forms_elements[button_name], ","
            )
            self.java.select_window(
                title=window_title, bring_foreground=True, timeout=std_60s_wait
            )
            self.send_keys(*keys_combinations_button)
        except Exception as ex:
            raise ex

    def write_input_by_name(self, input_name: str, input_value: str):
        """
        Writes a custom value inside an element in 'Submit Request' screen by it's name
        @param input_name: Must be one of this possible values:
        "input_name"
        @param input_value: Must be the value to be written in the input field
        """
        try:
            input_name = input_name.strip().lower()
            oracle_forms_elements = self.oracle_forms_elements
            if input_name not in oracle_forms_elements:
                raise Exception(
                    "The input with the name: "
                    + input_name
                    + " doesn't exists in 'Submit Request' screen"
                )
            element_exists = self.wait_until_element_exists(oracle_forms_elements[input_name], std_15s_wait)
            if(not element_exists):
               raise Exception("The input with the name: "
                               + input_name
                               + " doesn't exists in 'Submit Request' screen")
            self.write_in_element(oracle_forms_elements[input_name], input_value)
        except Exception as ex:
            raise ex