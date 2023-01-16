from . import OracleForms
from Emerson.variables import std_15s_wait, std_60s_wait

class Journals(OracleForms):
    def __init__(self, *args, **kwargs):
        OracleForms.__init__(self, *args, **kwargs)
        self.oracle_forms_elements = self.actions.read_configuration("data/oracle_forms_config/oracle_journals_elements.json")

    def check_journals_screen_exists(self, 
                                     timeout: int) -> bool:
        """
        Checks if the 'Journals' screen exists
        @param timeout: The amount of seconds to wait
        """
        element_exists = False
        try:
            oracle_forms_elements = self.oracle_forms_elements
            element_exists = self.wait_until_element_exists(
                oracle_forms_elements["window_journals"], timeout
            )
        except Exception as ex:
            raise ex
        return element_exists

    def click_button_by_name(self, window_title: str, 
                             button_name: str) -> None:
        """
        Clicks a button in 'Journals' screen by it's name
        @param window_title: The Oracle Forms application window title name
        @param button_name: Must be one of this possible values:
        "button_post", "button_ok"
        """
        try:
            window_title = window_title.strip()
            button_name = button_name.strip().lower()
            oracle_forms_elements = self.oracle_forms_elements
            if button_name not in oracle_forms_elements:
                raise Exception(
                    "The button with the name: "
                    + button_name
                    + " doesn't exists in 'Journals' screen"
                )
            element_exists = self.wait_until_element_exists(oracle_forms_elements['window_journals'], 
                                                            std_15s_wait)
            if(not element_exists):
                raise Exception("Cannot find 'Journals' screen")
            keys_combinations_button = self.actions.split_string_to_list(
                oracle_forms_elements[button_name], ","
            )
            self.java.select_window(
                title=window_title, bring_foreground=True, timeout=std_15s_wait
            )
            self.send_keys(*keys_combinations_button)
        except Exception as ex:
            raise ex
    
    def read_field_by_name(self, 
                           window_title: str, 
                           field_name: str) -> str:
        """
        Reads an element value in 'Journals' screen by it's name
        @param window_title: The Oracle Forms application window title name
        @param field_name: Must be one of this possible values:
        "field_document_number", "field_concurrent_number"
        """
        try:
            element_value = ""
            window_title = window_title.strip()
            field_name = field_name.strip().lower()
            oracle_forms_elements = self.oracle_forms_elements
            if field_name not in oracle_forms_elements:
                raise Exception(
                    "The field with the name: "
                    + field_name
                    + " doesn't exists in 'Jourmals' screen"
                )
            self.java.select_window(
            title=window_title, bring_foreground=True, timeout=std_15s_wait
            )
            element_value = self.java.get_element_text(oracle_forms_elements[field_name]).strip()
            return element_value
        except Exception as ex:
            raise ex

    def write_field_by_name(self, 
                            window_title: str, 
                            field_name: str, 
                            value: str, 
                            verify: bool = False) -> None:
        """
        Clicks a button in 'Journals' screen by it's name
        @param window_title: The Oracle Forms application window title name
        @param field_name: Must be one of this possible values:
        "field_document_number"
        @param value: The value to type inside the element
        @param verify: Must be 'True' or 'False' accordingly if you want to check that the given value is the same as the typed in
        """
        try:
            window_title = window_title.strip()
            field_name = field_name.strip().lower()
            oracle_forms_elements = self.oracle_forms_elements
            if field_name not in oracle_forms_elements:
                raise Exception(
                    "The field with the name: "
                    + field_name
                    + " doesn't exists in 'Journals' screen"
                )
            self.java.select_window(
            title=window_title, bring_foreground=True, timeout=std_15s_wait
            )
            self.write_in_element(oracle_forms_elements[field_name],
                                  value, 
                                  verify)
        except Exception as ex:
            raise ex