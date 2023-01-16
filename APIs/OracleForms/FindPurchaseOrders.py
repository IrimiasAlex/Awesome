from . import OracleForms
from Emerson.variables import std_15s_wait, std_60s_wait

class FindPurchaseOrders(OracleForms):
    def __init__(self, *args, **kwargs):
        OracleForms.__init__(self, *args, **kwargs)
        self.oracle_forms_elements = self.actions.read_configuration("data/oracle_forms_config/oracle_find_purchase_orders_elements.json")
        
    def check_find_purchase_orders_screen_exists(self, timeout: int):
        element_exists = False
        try:
            oracle_forms_elements = self.oracle_forms_elements
            element_exists = self.wait_until_element_exists(
                oracle_forms_elements["window_find_purchase_orders"], timeout
            )
        except Exception as ex:
            raise ex
        return element_exists

    def click_button_by_name(self, window_title: str, button_name: str):
        """
        Clicks a button in 'Find Purchase Orders' screen by it's name
        @param window_title: The Oracle Forms application window title name
        @param button_name: Must be one of this possible values:
        "button_clear", "button_find", "button_close_form"
        """
        try:
            window_title = window_title.strip()
            button_name = button_name.strip().lower()
            oracle_forms_elements = self.oracle_forms_elements
            if button_name not in oracle_forms_elements:
                raise Exception(
                    "The button with the name: "
                    + button_name
                    + " doesn't exists in 'Find Purchase Orders' screen"
                )
            element_exists = self.wait_until_element_exists(oracle_forms_elements['window_find_purchase_orders'], std_15s_wait)
            if(not element_exists):
               raise Exception("Cannot find 'Find Purchase Orders' screen")
            keys_combinations_button = self.actions.split_string_to_list(
                oracle_forms_elements[button_name], ","
            )
            self.java.select_window(
                title=window_title, bring_foreground=True, timeout=std_60s_wait
            )
            self.send_keys(*keys_combinations_button)
        except Exception as ex:
            raise ex
    
    def click_combo_box_option(self, combo_box_name: str, combo_box_option_name: str):
        """
        Clicks an option of a combo box in 'Find Purchase Orders' screen
        @param combo_box_name: Must be one of this possible values:
        "combo_box_order_approval", "combo_box_control"
        @param combo_box_option_name: Must be one of this possible values:
        "combo_box_order_approval_option_approved", "combo_box_control_option_open"
        """
        try:
            combo_box_name = combo_box_name.strip().lower()
            combo_box_option_name = combo_box_option_name.strip().lower()
            oracle_forms_elements = self.oracle_forms_elements
            if combo_box_name not in oracle_forms_elements:
                raise Exception(
                    "The combo box with the name: "
                    + combo_box_name
                    + " doesn't exists in 'Find Purchase Orders' screen"
                )
            if combo_box_option_name not in oracle_forms_elements:
                raise Exception(
                    "The combo box option with the name: "
                    + combo_box_option_name
                    + " doesn't exists in 'Find Purchase Orders' screen"
                )
            element_exists = self.wait_until_element_exists(oracle_forms_elements[combo_box_name], std_15s_wait)
            if(not element_exists):
               raise Exception("The combo box with the name: "
                               + combo_box_name
                               + " doesn't exists in 'Find Purchase Orders' screen")
            self.click_java_element(oracle_forms_elements[combo_box_name])
            element_exists = self.wait_until_element_exists(oracle_forms_elements[combo_box_option_name], std_15s_wait)
            if(not element_exists):
                raise Exception("Cannot find the option '" 
                                + combo_box_option_name 
                                + "' to select in '" 
                                + combo_box_name 
                                + "' of 'Find Purchase Orders' screen")    
            self.click_java_element(oracle_forms_elements[combo_box_option_name])
        except Exception as ex:
            raise ex
        
    def click_tab_by_name(self, tab_name: str):
        """
        Clicks a tab in 'Find Purchase Orders' screen by it's name
        @param tab_name: Must be one of this possible values:
        "tab_status"
        """
        try:
            tab_name = tab_name.strip().lower()
            oracle_forms_elements = self.oracle_forms_elements
            if tab_name not in oracle_forms_elements:
                raise Exception(
                    "The tab with the name: "
                    + tab_name
                    + " doesn't exists in 'Find Purchase Orders' screen"
                )
            element_exists = self.wait_until_element_exists(oracle_forms_elements[tab_name], std_15s_wait)
            if(not element_exists):
               raise Exception("The tab with the name: "
                               + tab_name
                               + " doesn't exists in 'Find Purchase Orders' screen")
            self.click_java_element(oracle_forms_elements[tab_name])
        except Exception as ex:
            raise ex
        
    def write_input_by_name(self, input_name: str, input_value: str):
        """
         Writes a custom value inside an element in 'Find Purchase Orders' screen by it's name
        @param input_name: Must be one of this possible values:
        "input_number"
        @param input_value: Must be the value to be written in the input field
        """
        try:
            input_name = input_name.strip().lower()
            oracle_forms_elements = self.oracle_forms_elements
            if input_name not in oracle_forms_elements:
                raise Exception(
                    "The input with the name: "
                    + input_name
                    + " doesn't exists in 'Find Purchase Orders' screen"
                )
            element_exists = self.wait_until_element_exists(oracle_forms_elements[input_name], std_15s_wait)
            if(not element_exists):
               raise Exception("The input with the name: "
                               + input_name
                               + " doesn't exists in 'Find Purchase Orders' screen")
            self.write_in_element(oracle_forms_elements[input_name], input_value)
        except Exception as ex:
            raise ex