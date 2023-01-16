from . import OracleForms
from Emerson.variables import std_15s_wait, std_60s_wait

class Requests(OracleForms):
    def __init__(self, *args, **kwargs):
        OracleForms.__init__(self, *args, **kwargs)
        self.oracle_forms_elements = self.actions.read_configuration("data/oracle_forms_config/oracle_requests_elements.json")

    def open_requests_screen(self, window_title: str):
        try:
            oracle_forms_elements = self.oracle_forms_elements
            keys_combination_requests = self.actions.split_string_to_list(
                oracle_forms_elements["keys_combination_requests"], ","
            )
            self.java.select_window(
                title=window_title, bring_foreground=True, timeout=std_60s_wait
            )
            self.send_keys(*keys_combination_requests)
            element_exists = self.wait_until_element_exists(
                oracle_forms_elements["window_requests"], std_15s_wait
            )
            if not element_exists:
                raise Exception("Cannot find 'Requests' screen")
        except Exception as ex:
            raise ex

    def check_requests_screen_exists(self, timeout: int):
        element_exists = False
        try:
            oracle_forms_elements = self.oracle_forms_elements
            element_exists = self.wait_until_element_exists(
                oracle_forms_elements["window_requests"], timeout
            )
        except Exception as ex:
            raise ex
        return element_exists

    def read_requests_table(self, scroll_down: bool = False):
        table_requests_data = []
        try:
            oracle_forms_elements = self.oracle_forms_elements
            element_exists = self.wait_until_element_exists(oracle_forms_elements['window_requests'], std_15s_wait)
            if(not element_exists):
               raise Exception("Cannot find 'Requests' screen")
            table_requests_fields = oracle_forms_elements["requests_table_fields"]
            if scroll_down:
                table_requests_key_column_name = list(
                    table_requests_fields[0].values()
                )[0].strip()
                keys_combinations_button_scroll_down = (
                    self.actions.split_string_to_list(
                        oracle_forms_elements["button_scroll_down"], ","
                    )
                )
                table_requests_data = self.read_table_with_scroll_down(
                    table_requests_fields,
                    table_requests_key_column_name,
                    *keys_combinations_button_scroll_down
                )
            else:
                table_requests_data = self.read_table(table_requests_fields)
        except Exception as ex:
            raise ex
        return table_requests_data

    def click_button_by_name(self, window_title: str, button_name: str):
        """
        Clicks a button in 'Requests' screen by it's name
        @param window_title: The Oracle Forms application window title name
        @param button_name: Must be one of this possible values:
        "button_refresh_data", "button_find_requests", "button_submit_a_new_request", "button_submit_new_request_set",
        "button_copy_single_request", "button_copy_request_set", "button_hold_request", "button_view_details",
        "button_re_run_request", "button_view_output", "button_diagnostics", "button_re_print_republish",
        "button_view_log", "button_scroll_down", "button_close_form"
        """
        try:
            window_title = window_title.strip()
            button_name = button_name.strip().lower()
            oracle_forms_elements = self.oracle_forms_elements
            if button_name not in oracle_forms_elements:
                raise Exception(
                    "The button with the name: "
                    + button_name
                    + " doesn't exists in 'Requests' screen"
                )
            element_exists = self.wait_until_element_exists(oracle_forms_elements['window_requests'], std_15s_wait)
            if(not element_exists):
               raise Exception("Cannot find 'Requests' screen")
            keys_combinations_button = self.actions.split_string_to_list(
                oracle_forms_elements[button_name], ","
            )
            self.java.select_window(
                title=window_title, bring_foreground=True, timeout=std_60s_wait
            )
            self.send_keys(*keys_combinations_button)
        except Exception as ex:
            raise ex