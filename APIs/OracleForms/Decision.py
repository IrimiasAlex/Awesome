from . import OracleForms
from Emerson.variables import std_15s_wait, std_60s_wait


class Decision(OracleForms):
    def __init__(self, *args, **kwargs):
        OracleForms.__init__(self, *args, **kwargs)
        self.oracle_forms_elements = self.actions.read_configuration(
            "data/oracle_forms_config/oracle_decision_elements.json")
        self.error_element_locator = "role:internal frame"
        self.error_element_attribute = "name"

    def check_decision_screen_exists(self, timeout: int):
        element_exists = False
        element = None
        try:
            oracle_forms_elements = self.oracle_forms_elements
            element = self.get_element_by_attribute(
                self.error_element_locator, self.error_element_attribute,
                oracle_forms_elements["window_decision"], timeout
            )
            if element is not None:
                element_exists = True
        except Exception as ex:
            raise ex
        return element_exists

    def read_label_by_name(self, window_title: str, label_name: str) -> str:
        """
        Reads a label value in 'Decision' screen by it's name
        @param window_title: The Oracle Forms application window title name
        @param label_name: Must be one of this possible values:
        "label_request_id"
        """
        label_value = ""
        try:
            window_title = window_title.strip()
            label_name = label_name.strip().lower()
            oracle_forms_elements = self.oracle_forms_elements
            element = None
            if label_name not in oracle_forms_elements:
                raise Exception(
                    "The button with the name: "
                    + label_name
                    + " doesn't exists in 'Decision' screen"
                )
            element = self.get_element_by_attribute(
                self.error_element_locator, self.error_element_attribute,
                oracle_forms_elements["window_decision"], std_15s_wait
            )
            if element is None:
                raise Exception("Cannot find 'Decision' screen")
            element_label = self.get_element_by_attribute(
                "role:label", self.error_element_attribute,
                oracle_forms_elements["label_request_id"], std_15s_wait
            )
            label_value = element_label.virtual_accessible_name.strip()
        except Exception as ex:
            raise ex
        return label_value

    def click_button_by_name(self, window_title: str, button_name: str):
        """
        Clicks a button in 'Decision' screen by it's name
        @param window_title: The Oracle Forms application window title name
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
                    + " doesn't exists in 'Decision' screen"
                )
            element = self.get_element_by_attribute(
                self.error_element_locator, self.error_element_attribute,
                oracle_forms_elements["window_decision"], std_15s_wait
            )
            if element is None:
                raise Exception("Cannot find 'Decision' screen")
            keys_combinations_button = self.actions.split_string_to_list(
                oracle_forms_elements[button_name], ","
            )
            self.java.select_window(
                title=window_title, bring_foreground=True, timeout=std_60s_wait
            )
            self.send_keys(*keys_combinations_button)
        except Exception as ex:
            raise ex
