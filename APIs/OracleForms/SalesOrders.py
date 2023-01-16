
from time import sleep
from . import OracleForms
from Emerson.variables import std_60s_wait


class SalesOrders(OracleForms):
    def __init__(self, *args, **kwargs):
        OracleForms.__init__(self, *args, **kwargs)
        self.oracle_forms_elements = self.actions.read_configuration(
            "data/oracle_forms_config/oracle_sales_orders_elements.json")

    def read_main_table(self, scroll_down: bool = False, return_java_elements: bool = True):
        table_main_data = []
        try:
            oracle_forms_elements = self.oracle_forms_elements
            main_requests_fields = oracle_forms_elements["main_table_fields"]
            if scroll_down:
                table_main_key_column_name = list(
                    main_requests_fields[0].values()
                )[0].strip()
                keys_combinations_button_scroll_down = (
                    self.actions.split_string_to_list(
                        oracle_forms_elements["button_scroll_down"], ","
                    )
                )
                table_main_data = self.read_table_with_scroll_down(
                    main_requests_fields,
                    table_main_key_column_name,
                    *keys_combinations_button_scroll_down
                )
            else:
                table_main_data = self.read_table(
                    main_requests_fields, return_java_elements)
        except Exception as ex:
            raise ex
        return table_main_data

    def read_shipping_table(self, scroll_down: bool = False, return_java_elements: bool = True):
        table_shipping_data = []
        try:
            oracle_forms_elements = self.oracle_forms_elements
            shipping_requests_fields = oracle_forms_elements["shipping_table_fields"]
            if scroll_down:
                table_shipping_key_column_name = list(
                    shipping_requests_fields[0].values()
                )[0].strip()
                keys_combinations_button_scroll_down = (
                    self.actions.split_string_to_list(
                        oracle_forms_elements["button_scroll_down"], ","
                    )
                )
                table_shipping_data = self.read_table_with_scroll_down(
                    shipping_requests_fields,
                    table_shipping_key_column_name,
                    *keys_combinations_button_scroll_down
                )
            else:
                table_shipping_data = self.read_table(
                    shipping_requests_fields, return_java_elements)
        except Exception as ex:
            raise ex
        return table_shipping_data

    def read_attachments_table(self, scroll_down: bool = False, return_java_elements: bool = True):
        table_attachments_data = []
        try:
            oracle_forms_elements = self.oracle_forms_elements
            attachments_requests_fields = oracle_forms_elements["attachments_table_fields"]
            attachments_requests_fields1 = oracle_forms_elements["attachments_table_fields_1"]
            if scroll_down:
                table_attachments_key_column_name = list(
                    attachments_requests_fields[0].values()
                )[0].strip()
                keys_combinations_button_scroll_down = (
                    self.actions.split_string_to_list(
                        oracle_forms_elements["button_scroll_down"], ","
                    )
                )
                table_attachments_data = self.read_table_with_scroll_down(
                    attachments_requests_fields,
                    table_attachments_key_column_name,
                    *keys_combinations_button_scroll_down
                )
            else:
                table_attachments_data = self.read_table(
                    attachments_requests_fields, return_java_elements)
                table_attachments_data_1 = self.read_table(
                    attachments_requests_fields1, return_java_elements)
                if len(table_attachments_data) < 1:
                    table_attachments_data = table_attachments_data_1
        except Exception as ex:
            raise ex
        return table_attachments_data

    def read_returns_table(self, scroll_down: bool = False, return_java_elements: bool = True):
        table_returns_data = []
        try:
            oracle_forms_elements = self.oracle_forms_elements
            returns_requests_fields = oracle_forms_elements["returns_table_fields"]
            if scroll_down:
                table_returns_key_column_name = list(
                    returns_requests_fields[0].values()
                )[0].strip()
                keys_combinations_button_scroll_down = (
                    self.actions.split_string_to_list(
                        oracle_forms_elements["button_scroll_down"], ","
                    )
                )
                table_returns_data = self.read_table_with_scroll_down(
                    returns_requests_fields,
                    table_returns_key_column_name,
                    *keys_combinations_button_scroll_down
                )
            else:
                table_returns_data = self.read_table(
                    returns_requests_fields, return_java_elements)
        except Exception as ex:
            raise ex
        return table_returns_data

    def read_pricing_table(self, scroll_down: bool = False, return_java_elements: bool = True):
        table_pricing_data = []
        try:
            oracle_forms_elements = self.oracle_forms_elements
            returns_requests_fields = oracle_forms_elements["pricing_table_fields"]
            if scroll_down:
                table_pricing_key_column_name = list(
                    returns_requests_fields[0].values()
                )[0].strip()
                keys_combinations_button_scroll_down = (
                    self.actions.split_string_to_list(
                        oracle_forms_elements["button_scroll_down"], ","
                    )
                )
                table_pricing_data = self.read_table_with_scroll_down(
                    returns_requests_fields,
                    table_pricing_key_column_name,
                    *keys_combinations_button_scroll_down
                )
            else:
                table_pricing_data = self.read_table(
                    returns_requests_fields, return_java_elements)
        except Exception as ex:
            raise ex
        return table_pricing_data

    def read_others_table(self, scroll_down: bool = False, return_java_elements: bool = True):
        table_others_data = []
        try:
            oracle_forms_elements = self.oracle_forms_elements
            others_requests_fields = oracle_forms_elements["others_table_fields"]
            if scroll_down:
                table_others_key_column_name = list(
                    others_requests_fields[0].values()
                )[0].strip()
                keys_combinations_button_scroll_down = (
                    self.actions.split_string_to_list(
                        oracle_forms_elements["button_scroll_down"], ","
                    )
                )
                table_others_data = self.read_table_with_scroll_down(
                    others_requests_fields,
                    table_others_key_column_name,
                    *keys_combinations_button_scroll_down
                )
            else:
                table_others_data = self.read_table(
                    others_requests_fields, return_java_elements)
        except Exception as ex:
            raise ex
        return table_others_data

    def check_sales_order_screen_exists(self, timeout: int):
        element_exists = False
        try:
            oracle_forms_elements = self.oracle_forms_elements
            element_exists = self.wait_until_element_exists(
                oracle_forms_elements["window_sales_orders"], timeout
            )
        except Exception as ex:
            raise ex
        return element_exists

    def click_button_by_name_send_keys(self, window_title: str, button_name: str):
        """
        Clicks a button in 'Requests' screen by it's name
        @param window_title: The Oracle Forms application window title name
        @param button_name: Must be one of this possible values:
        "button_actions", "button_find", "button_save", "button_ok",
        "button_order_information_others", "button_order_information_main", "button_line_items", "button_release"
        """
        try:
            window_title = window_title.strip()
            button_name = button_name.strip().lower()
            oracle_forms_elements = self.oracle_forms_elements
            if button_name not in oracle_forms_elements:
                raise Exception(
                    "The button with the name: "
                    + button_name
                    + " doesn't exists in 'Sales Order' screen"
                )
            keys_combinations_button = self.actions.split_string_to_list(
                oracle_forms_elements[button_name], ","
            )
            self.java.select_window(
                title=window_title, bring_foreground=True, timeout=std_60s_wait
            )
            self.send_keys(*keys_combinations_button)
        except Exception as ex:
            raise ex

    def click_button_by_name(self, window_title: str, button_name: str):
        """
        Clicks a button in 'Requests' screen by it's name
        @param window_title: The Oracle Forms application window title name
        @param button_name: Must be one of this possible values:
        "button_actions", "button_find", "button_save", "button_ok",
        "button_order_information_others", "button_order_information_main", "button_line_items"
        """
        try:
            window_title = window_title.strip()
            button_name = button_name.strip().lower()
            oracle_forms_elements = self.oracle_forms_elements
            if button_name not in oracle_forms_elements:
                raise Exception(
                    "The button with the name: "
                    + button_name
                    + " doesn't exists in 'Sales Order' screen"
                )
            self.click_java_element(oracle_forms_elements[button_name])
        except Exception as ex:
            raise ex

    def read_field_by_name(self, window_title: str, field_name: str):
        """
        Clicks a button in 'Requests' screen by it's name
        @param window_title: The Oracle Forms application window title name
        @param button_name: Must be one of this possible values:
        "button_actions", "button_find", "button_save", "button_ok",
        "button_order_information_others", "button_order_information_main", "button_line_items"
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
                    + " doesn't exists in 'Sales Order' screen"
                )
            self.java.select_window(
                title=window_title, bring_foreground=True, timeout=std_60s_wait
            )
            element_value = self.java.get_element_text(
                oracle_forms_elements[field_name]).strip()
            return element_value
        except Exception as ex:
            raise element_value

    def write_field_by_name(self, window_title: str, field_name: str, value_name: str, verify: bool = False):
        """
        Clicks a button in 'Requests' screen by it's name
        @param window_title: The Oracle Forms application window title name
        @param button_name: Must be one of this possible values:
        "field_order_number", "field_find", "field_reason_for_value", "field_reason_release"
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
                    + " doesn't exists in 'Sales Order' screen"
                )
            # self.java.select_window(
            # title=window_title, bring_foreground=True, timeout=std_60s_wait
            # )
            self.write_in_element(
                oracle_forms_elements[field_name], value_name, verify)
        except Exception as ex:
            raise element_value

    def read_release_hold_table(self, scroll_down: bool = False):
        table_release_hold_data = []
        try:
            oracle_forms_elements = self.oracle_forms_elements
            release_hold_requests_fields = oracle_forms_elements["release_hold_table_fields"]
            if scroll_down:
                table_release_hold_key_column_name = list(
                    release_hold_requests_fields[0].values()
                )[0].strip()
                keys_combinations_button_scroll_down = (
                    self.actions.split_string_to_list(
                        oracle_forms_elements["button_scroll_down"], ","
                    )
                )
                table_release_hold_data = self.read_table_with_scroll_down(
                    release_hold_requests_fields,
                    table_release_hold_key_column_name,
                    *keys_combinations_button_scroll_down
                )
            else:
                table_release_hold_data = self.read_table(
                    release_hold_requests_fields)
        except Exception as ex:
            raise ex
        return table_release_hold_data
    
    def write_customer_number(self, window_title, customer_number) -> None:
        try:
            self.attach_oracle_forms(window_title)
            self.wait_until_element_exists("name:Customer NumberList of Values and role:text", 5)
            self.write_field_by_name(window_title, "field_customer_locator", customer_number)
            sleep(2)
            self.java.press_keys("tab") 
            self.refresh_application_elements_tree()
            customer_num = self.read_field_by_name(window_title, "field_customer_locator")
            if customer_num != customer_number:
                raise Exception("Error to write customer number: " + customer_number)
        except Exception as ex:
            raise ex
        
    def search_order_number(self, window_title, order_number: str):
        try:
            self.attach_oracle_forms(window_title)
            self.refresh_application_elements_tree()
            self.wait_until_element_exists("name:Find Orders/Quotes and role:internal frame",3)
            self.write_field_by_name(window_title, "field_order_number", order_number)
            self.java.press_keys("alt", "i")
            self.java.press_keys("alt", "o")
        except Exception as ex:
            raise ex
        
    def read_order_date(self, window_title):
        order_date = ""
        try:
            self.refresh_application_elements_tree()
            self.click_button_by_name(window_title, "button_order_information_others")
            self.wait_until_element_exists("name:Order Date TypeList of Values and role:text", 2)
            order_date = self.read_field_by_name(window_title, "field_order_date_type")
            return order_date
        except Exception as ex:
            raise ex
        
    def go_to_line_items(self, window_title):
        try:
            a = 0
            self.refresh_application_elements_tree()
            self.click_button_by_name(window_title, "button_line_items")
            exist = self.wait_until_element_exists("name:Availability and role:internal frame", 5)
            if exist:
                for i in range(3):
                    a = a+1
                    self.click_button_by_name(window_title, "button_order_item_availability")
                    sleep(2)
                    self.java.press_keys("ctrl", "f4")
                    sleep(2)
                    self.refresh_application_elements_tree()
                    exist = self.wait_until_element_exists("name:Availability and role:internal frame", 5)
                    if exist:
                        continue
                    else:
                        break
                if a >= 3:
                    raise "Error to close availability"
            else:
                raise "Error to close availability"
        except Exception as ex:
            raise ex
        
    def write_reson_for(self, window_title, reason_code):    
        try:
            self.refresh_application_elements_tree()
            visible = self.wait_until_element_exists("name:Enter Reason for..... and role:internal frame",5)
            if visible:
                self.refresh_application_elements_tree()
                self.write_field_by_name(window_title, "field_reason_for_value", reason_code)
                self.java.press_keys("alt", "o")
            return True
        except Exception as ex:
            self.builtin.log_to_console("kw: Save Changes - EXCEPTION - " + str(ex))
            raise ex
        
    def select_line_from_table(self, tablename, line, action_action=False):
        found = False
        last_number_is_smaller = False
        first_number_is_smaller = False
        smallest_seen = 0
        try:
            self.refresh_application_elements_tree()
            for _ in range(10):
                if tablename == "main":
                    table = self.read_main_table()
                else:
                    table = self.read_shipping_table()
                if table != []:
                    break
                sleep(5)
            smallest_seen = 2000
            for _ in range(100):
                for row in table:
                    if row["Line"] == line:
                        self.click_coordinates(row["LineElement"])
                        return row
                line_first_number = int(line.split(".")[0])
                table_first_number = int(table[0]["Line"].split(".")[0])
                table_last_number = int(table[-1]["Line"].split(".")[0])
                if table_last_number < line_first_number:
                    last_number_is_smaller = True
                if table_first_number < line_first_number:
                    first_number_is_smaller = True
                if table_first_number < smallest_seen:
                    smallest_seen = table_first_number
                
                if last_number_is_smaller or first_number_is_smaller or smallest_seen < line_first_number:
                    self.java.press_keys("page_down")
                    if action_action:
                        print("hi")
                else:
                    self.java.press_keys("page_up")
                if tablename == "main":
                    table = self.read_main_table()
                else:
                    table = self.read_shipping_table()
                action_action = False
            return False
        
        except Exception as ex:
            raise ex
        
    def handle_sales_order_process_messages(self):
        messages = []
        count = 0
        message_frame_locator = "name:Process Messages (Sales Order) and role:internal frame"
        try:
            self.refresh_application_elements_tree()
            visible = self.wait_until_element_exists(message_frame_locator, 2)
            if visible:
                lines = self.get_all_elements(message_frame_locator + "> name:Line and role:text")
                texts = self.get_all_elements(message_frame_locator + "> name:Message Text and role:text")
                for line in lines:
                    line_item = line.text
                    if line_item != "":
                        message= texts[count].text
                        msg = {"line":line_item, "message":message}
                        messages.append(msg)
                    count += 1
            self.java.press_keys("alt", "o")
            return messages
        except Exception as ex:
            raise ex
        
    def go_to_shipping(self, window_title):
        try:
            self.refresh_application_elements_tree()
            self.click_button_by_name(window_title, "tab_shipping")
        except Exception as ex:
            raise ex
        
    def change_date_shipping_tab(self, shipping_table, new_date, column_to_write):
        try:
            changes_made = False
            
            if column_to_write == "Arrival":
                self.click_coordinates(shipping_table["ArrivalDateElement"])
                self.type_text(new_date)
                changes_made = True
            elif column_to_write == "Ship":
                self.click_coordinates(shipping_table["ShipDateElement"])
                self.type_text(new_date)
                changes_made = True
            return changes_made
        except Exception as ex:
            raise ex
        
    def discard_pending_changes(self):
        try:
            self.wait_until_element_exists("name:Decision You have changes pending.", 2)
            self.java.press_keys("alt", "D")
        except Exception as ex:
            raise ex
        
    def go_to_main_tab(self, window_title):
        try:
            self.refresh_application_elements_tree()
            self.click_button_by_name(window_title, "tab_main")
        except Exception as ex:
            raise ex
        
    def press_override_atp(self, shipping_row):
        try:
            self.refresh_application_elements_tree()
            if shipping_row["OverrideATPElement"].checked == False:
                self.click_coordinates(shipping_row["OverrideATPElement"])
                return True
            return False
        except Exception as ex:
            raise ex