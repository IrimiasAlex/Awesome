from . import OracleForms
from Emerson.variables import std_15s_wait, std_60s_wait

class DiscreteJobsSummary(OracleForms):
    def __init__(self, *args, **kwargs):
        OracleForms.__init__(self, *args, **kwargs)
        self.oracle_forms_elements = self.actions.read_configuration("data/oracle_forms_config/oracle_discrete_jobs_summary.json")


    def check_discrete_jobs_summary_screen_exists(self, timeout: int):
        element_exists = False
        try:
            oracle_forms_elements = self.oracle_forms_elements
            element_exists = self.wait_until_element_exists(
                oracle_forms_elements["window_discrete_jobs_summary"], timeout
            )
        except Exception as ex:
            raise ex
        return element_exists

    def click_button_by_name(self, window_title: str, button_name: str):
        try:
            window_title = window_title.strip()
            button_name = button_name.strip().lower()
            oracle_forms_elements = self.oracle_forms_elements
            if button_name not in oracle_forms_elements:
                raise Exception(
                    "The button with the name: "
                    + button_name
                    + " doesn't exists in 'Discrete Jobs Summary' screen"
                )
            self.click_java_element(oracle_forms_elements[button_name])
        except Exception as ex:
            raise ex

    def read_field_by_name(self, window_title: str, field_name: str):
        try:
            element_value = ""
            window_title = window_title.strip()
            field_name = field_name.strip().lower()
            oracle_forms_elements = self.oracle_forms_elements
            if field_name not in oracle_forms_elements:
                raise Exception(
                    "The field with the name: "
                    + field_name
                    + " doesn't exists in 'Discrete Jobs Summary' screen"
                )
            self.java.select_window(
            title=window_title, bring_foreground=True, timeout=std_60s_wait
            )
            element_value = self.java.get_element_text(oracle_forms_elements[field_name]).strip()
            return element_value
        except Exception as ex:
            raise element_value

    def write_field_by_name(self, window_title: str, field_name: str, value_name: str, verify: bool = False):
        try:
            element_value = ""
            window_title = window_title.strip()
            field_name = field_name.strip().lower()
            oracle_forms_elements = self.oracle_forms_elements
            if field_name not in oracle_forms_elements:
                raise Exception(
                    "The field with the name: "
                    + field_name
                    + " doesn't exists in 'Discrete Jobs Summary' screen"
                )
            #self.java.select_window(
            #title=window_title, bring_foreground=True, timeout=std_60s_wait
            #)
            self.write_in_element(oracle_forms_elements[field_name],value_name, verify)
        except Exception as ex:
            raise element_value

    