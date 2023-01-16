from . import OracleForms
from Emerson.variables import std_15s_wait, std_60s_wait

class Attachments(OracleForms):
    def __init__(self, *args, **kwargs):
        OracleForms.__init__(self, *args, **kwargs)
        self.oracle_forms_elements = self.actions.read_configuration("data/oracle_forms_config/oracle_attachments_elements.json")

    def open_attachments_screen(self, window_title: str):
        try:
            oracle_forms_elements = self.oracle_forms_elements
            keys_combination_attachments = self.actions.split_string_to_list(
                oracle_forms_elements["keys_combination_attachments"], ","
            )
            self.java.select_window(
                title=window_title, bring_foreground=True, timeout=std_60s_wait
            )
            self.send_keys(*keys_combination_attachments)
            element_exists = self.wait_until_element_exists(
                oracle_forms_elements["window_attachments"], std_15s_wait
            )
            if not element_exists:
                raise Exception("Cannot find 'Attachments' screen")
        except Exception as ex:
            raise ex
        
    def click_button_by_name(self, window_title: str, button_name: str):
        """
        Clicks a button in 'Attachments' screen by it's name
        @param window_title: The Oracle Forms application window title name
        @param button_name: Must be one of this possible values:
        "button_open_document", "button_close_form"
        """
        try:
            window_title = window_title.strip()
            button_name = button_name.strip().lower()
            oracle_forms_elements = self.oracle_forms_elements
            if button_name not in oracle_forms_elements:
                raise Exception(
                    "The button with the name: "
                    + button_name
                    + " doesn't exists in 'Attachments' screen"
                )
            element_exists = self.wait_until_element_exists(oracle_forms_elements['window_attachments'], std_15s_wait)
            if(not element_exists):
               raise Exception("Cannot find 'Attachments' screen")
            keys_combinations_button = self.actions.split_string_to_list(
                oracle_forms_elements[button_name], ","
            )
            self.java.select_window(
                title=window_title, bring_foreground=True, timeout=std_60s_wait
            )
            self.send_keys(*keys_combinations_button)
        except Exception as ex:
            raise ex